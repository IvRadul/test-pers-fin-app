import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".finanace_tracker"
CONFIG_FILE = CONFIG_DIR / "config.json"

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}
    
def save_config(cfg):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(cfg, f)

def db_config():
    cfg = load_config()
    if db_config in cfg:
        return cfg["db_config"]
    default_path = str(Path.home() / "finance.db")
    user_input = input(f"Введите путь к файлу БД [По умолчанию {default_path}]: ")
    if not user_input:
        user_input = default_path
    cfg["db_config"] = user_input
    save_config(cfg)
    return user_input

def csv_config():
    cfg = load_config()
    if csv_config in cfg:
        return cfg["csv_config"]
    default_path = str(Path.home() / "finance.csv")
    user_input = input(f"Введите путь к файлу csv [По умолчанию {default_path}]: ")
    if not user_input:
        user_input = default_path
    cfg["csv_config"] = user_input
    save_config(cfg)
    return user_input