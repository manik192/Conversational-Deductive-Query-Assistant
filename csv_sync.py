import sqlite3
import threading
from pathlib import Path
import pandas as pd
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

CSV_DIR = Path("data/csv")
DB_PATH = Path("data/sample/mydata.db")

def csv_to_table_name(csv_path):
    return csv_path.stem.lower().replace(" ", "_")

def sync_all_csvs():
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    try:
        for csv_file in CSV_DIR.glob("*.csv"):
            table = csv_to_table_name(csv_file)
            print(f"[AUTO-UPDATE] Importing {csv_file.name} → table '{table}'")

            df = pd.read_csv(csv_file)
            df.to_sql(table, conn, if_exists="replace", index=False)

        print("[AUTO-UPDATE] ✔ SQL database updated.")
    finally:
        conn.close()

class CSVHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".csv"):
            sync_all_csvs()

    def on_modified(self, event):
        if event.src_path.endswith(".csv"):
            sync_all_csvs()

observer = None

def start_csv_watcher():
    global observer
    if observer:
        return

    sync_all_csvs()

    handler = CSVHandler()
    observer = Observer()
    observer.schedule(handler, str(CSV_DIR), recursive=False)

    thread = threading.Thread(target=observer.start, daemon=True)
    thread.start()

    print("[WATCHER] ✔ Watching data/csv for new or updated CSV files...")
