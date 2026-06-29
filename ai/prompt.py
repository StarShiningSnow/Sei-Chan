from ai.mode import AIMode

def build(history:list,mode:AIMode,)->str:
    lines = []
    for chat in history:
        role = "User" if chat["role"] == "user" else "Sei-Chan"
        lines.append(f"{role}: {chat['content']}")
    return "\n".join(lines)