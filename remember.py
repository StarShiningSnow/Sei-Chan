from ai import model

REMEMBER_SYSTEM = "你是一個精準的長期記憶提取器。你的唯一任務是從 User 最新輸入的訊息中，提取具有長期保存價值的資訊。"

async def extract(message:str)->list[str]:
    try:
        response = await model.generate(message,REMEMBER_SYSTEM,temperature=0.0,num_predict=100)
        memories = []
        for line in response.splitlines():
            line = line.strip()
            if line.startswith("User:"):
                line = "User " + line[5:].strip()
            if line.startswith("User "):
                content = line[5:].strip()
                if content:
                    memory = f"User {content}"
                    if memory not in memories:
                        memories.append(memory)
        return memories
    except Exception:
        return []