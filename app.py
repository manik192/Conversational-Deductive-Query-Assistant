import streamlit as st

from helpers import chart, db, model, prompt, response, schema
from csv_sync import start_csv_watcher
import streamlit as st

if "csv_watch_started" not in st.session_state:
    start_csv_watcher()
    st.session_state["csv_watch_started"] = True



# Sidebar - Application title
st.sidebar.title("CDQ Assistant")


# Sidebar - Database Selection
st.sidebar.subheader("🛢️ Database")


# Load databases
databases = db.load_databases()
db_names = [db["name"] for db in databases]
selected_db_name = st.sidebar.selectbox("Select Database:", db_names)


# Retrieve the full configuration for the selected database
selected_db = next((db for db in databases if db["name"] == selected_db_name), None)

# Initialize database connection
if selected_db:
    db_type = selected_db["type"]
    db_path = selected_db["connection_string"]

    try:
        db_conn = db.create_database(db_type, db_path)
    except ValueError as e:
        st.sidebar.error(str(e))
        st.stop()
else:
    st.sidebar.error("❌ Database configuration not found.")
    st.stop()


# Generate schema file
schema_file = selected_db.get("schema")


# Dialogs
@st.dialog("⚠️ Confirm Schema Overwrite", width="small")
def confirm_overwrite():
    st.write(
        "This will overwrite the existing schema if it exists. Do you want to continue?"
    )
    if st.button("Yes, overwrite"):
        # Generate schema
        success, message = db.generate_schema(selected_db, databases, db_conn)

        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)


# Sidebar - Schema Management
st.sidebar.subheader("📝 Database Schema")

if schema_file:
    st.sidebar.success(f"✅ Schema was generated: {schema_file}")

    if st.sidebar.button("Regenerate Database Schema"):
        confirm_overwrite()
else:
    if st.sidebar.button("Generate Database Schema"):
        confirm_overwrite()


# Load database schema
schema_info, schema_warning = schema.load_schema(schema_file)

if schema_warning:
    st.sidebar.warning(schema_warning)


# Sidebar - AI Model Selection
st.sidebar.subheader("🤖 AI Model")

models = model.load_models()

if not models:
    st.sidebar.error("❌ No models available, please add models.")
    st.stop()

model_names = [model.name() for model in models]
default_index = model_names.index("Gemini") if "Gemini" in model_names else 0

selected_model_name = st.sidebar.selectbox("Select AI Model:", model_names, index=default_index)
selected_model = next((m for m in models if m.name() == selected_model_name), None)

model_variants = selected_model.get_variants()

if model_variants:
    variant_keys = list(model_variants.keys())
    default_variant = selected_model.get_default_variant()

    # Pre-select the default variant if available
    selected_model_variant = st.sidebar.selectbox(
        "Select Model Variant:",
        variant_keys,
        format_func=lambda key: model_variants[key],
        index=(
            variant_keys.index(default_variant)
            if default_variant in variant_keys
            else 0
        ),
    )
else:
    selected_model_variant = selected_model.get_default_variant()


# Sidebar - Chart Options
st.sidebar.subheader("📊 Chart Options")
generate_chart = st.sidebar.checkbox("Enable Chart Generation", value=False)


# Load list of charts
chart_classes = chart.load_charts()
chart_names = [chart_class.name for chart_class in chart_classes]

selected_chart = (
    st.sidebar.selectbox("Select Chart Type:", chart_names) if generate_chart else None
)


# Sidebar - Options
st.sidebar.subheader("⚙️ Options")
show_query = st.sidebar.checkbox("Show Query After Execution", value=False)


# Main Area - User prompt
st.header("💬 Ask Something About the Database")
user_prompt = st.text_input("Enter your question below:")

if st.button("🚀 Generate"):
    if not user_prompt:
        st.warning("⚠️ Please enter a prompt.")
    else:
        chart_class = None
        chart_prompt = None

        if generate_chart and selected_chart:
            chart_class = next(
                (cls for cls in chart_classes if cls.name == selected_chart), None
            )

            if chart_class:
                chart_prompt = chart_class.prompt

        # Build prompt with chart-specific prompt, if available
        messages = prompt.build(
            db_conn.get_driver_name(),
            schema_info,
            user_prompt,
            chart_prompt,
        )

        # Generate query using the selected model
        try:
            query = selected_model.run(
                messages,
                variant=selected_model_variant,
            )

            query = response.clean(query)

            # Validate the generated query
            if query.lower().startswith("error:"):
                st.error(query)
            else:
                # Show query
                if show_query:
                    st.divider()

                    with st.expander("🔍 Generated Query"):
                        st.code(
                            query,
                            language=db_conn.get_code_language(),
                        )

                # Execute query
                df = db_conn.run_query(query)

                if df is None or df.empty:
                    st.warning("⚠️ No results found.")
                else:
                    st.divider()
                    st.subheader("📊 Query Results")
                    st.dataframe(df)

                    # Generate chart if enabled
                    if generate_chart:
                        if chart_class:
                            st.divider()
                            st.subheader("📈 Generated Chart")

                            # Pass DataFrame directly to the chart class
                            chart_instance = chart_class()
                            chart_instance.render(df)

        except ValueError as e:
            st.error(f"❌ Error: {str(e)}")
