from pathlib import Path
import json

MEMORY_DIR = Path("data/memory")

def get_path(user_id:int)->Path:
    return MEMORY_DIR / f"{user_id}.json"

def load(user_id:int)->list[str]:
    MEMORY_DIR.mkdir(parents=True,exist_ok=True)
    path = get_path(user_id)
    if not path.exists():
        with open(path,"w",encoding="utf-8") as f:
            json.dump(
                {"memory":[]},
                f,ensure_ascii=False,indent=4,
            )
    with open(path,"r",encoding="utf-8") as f:
        data = json.load(f)
    return data["memory"]

def save(user_id:int,memory:list[str])->None:
    path = get_path(user_id)
    with open(path,"w",encoding="utf-8") as f:
        json.dump(
            {"memory":memory},
            f,ensure_ascii=False,indent=4,
        )

def append(user_id:int,content:str)->None:
    content = content.strip()
    if not content:
        return
    memory = load(user_id)
    if content not in memory:
        memory.append(content)
        save(user_id,memory)