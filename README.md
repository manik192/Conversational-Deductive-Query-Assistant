<p align="center">
    <a href="https://github.com/paulocoutinhox/db-talk-ai" target="_blank" rel="noopener noreferrer">
        <img width="180" src="extras/images/logo.png" alt="Logo">
    </a>
</p>

# Conversational Deductive Query Assistant

**Conversational Deductive Query Assistant** is an interactive application built with **Python** and **Streamlit**, allowing users to query databases using **AI-generated SQL**. It supports **local AI models** or **cloud-based models** (such as **OpenAI GPT**) and provides results as **tables** and **charts**.


## 📞 Installation

### **1. Clone the Repository**


### **2. Create a Virtual Environment**
```sh
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### **3. Install Dependencies**
```sh
pip install -r requirements.txt
```

If you want use local GGUF models install it too:
```sh
pip install -r requirements-gguf.txt
```

### **4. Download Local AI Models (Optional)**
If you prefer to use a **local AI model** instead of a **cloud-based model** (e.g., OpenAI GPT), follow these steps:

#### **Step 1: Download a Local AI Model**
You can download **GGUF format** models from Hugging Face:
- [Hugging Face - GGUF Models](https://huggingface.co/models)

#### **Step 2: Place the Model in the `models/` Directory**

#### **Step 3: Select the Model in the Streamlit App**
The model selector will automatically list `.gguf` files in `models/`. Choose one in the UI.

#### **Step 4: Run the Application**
```sh
streamlit run app.py
```

