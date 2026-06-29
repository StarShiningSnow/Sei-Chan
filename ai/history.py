from pathlib import Path
import json
from .mode import AIRole

HISTORY_DIR = Path("data/history")

def get_path(user_id:int)->Path:
    return HISTORY_DIR / f"{user_id}.json"

def load(user_id:int)->list:
    HISTORY_DIR.mkdir(parents=True,exist_ok=True)
    path = get_path(user_id)
    if not path.exists():
        with open(path,"w",encoding="utf-8") as f:
            json.dump(
                {"history":[]},
                f,
                ensure_ascii=False,
                indent=4,)
    with open(path,"r",encoding="utf-8") as f:
        data = json.load(f)
    return data["history"]

def save(user_id:int,history:list)->None:
    path = get_path(user_id)
    with open(path,"w",encoding="utf-8") as f:
        json.dump(
            {"history":history},
            f,
            ensure_ascii=False,
            indent=4,)

def append(user_id:int,role:AIRole,content:str)->None:
    history = load(user_id)
    history.append(
        {
            "role": role.value,
            "content": content,
        }
    )
    save(user_id,history)