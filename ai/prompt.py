from .mode import AIMode,AIRole

def build(history:list,message:str,mode:AIMode,)->str:
    lines = []

    lines.append("===== MODE =====")
    lines.append(mode.value)
    lines.append("")

    lines.append("===== HISTORY =====")
    for chat in history:
        role = "User" if chat["role"] == AIRole.USER.value else "Assistant"
        lines.append(f"{role}: {chat['content']}")
    
    lines.append("")
    lines.append("===== CURRENT MESSAGE =====")
    lines.append(f"User: {message}")
    return "\n".join(lines)