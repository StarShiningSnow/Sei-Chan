from ai import model

REMEMBER_SYSTEM = """
你是一個記憶整理器。

你的工作只有一個：
從 User 的訊息中找出值得永久保存的資訊。

規則：

1. 只分析 User，不分析 Assistant。
2. 只保留長期有效的資訊，例如姓名、喜好、生日、職業、專案、習慣。
3. 不要保存短期資訊，例如「今天好熱」、「我剛吃飽了」。
4. 每一行代表一筆記憶。
5. 每一筆記憶都必須以 User 為主詞。
6. 6. 如果沒有需要記住的內容，就完全不要輸出任何文字，也不要輸出「沒有」、「無」、「None」等內容。
"""

async def extract(message:str)->list[str]:
    try:
        response = await model.generate(message,REMEMBER_SYSTEM)
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