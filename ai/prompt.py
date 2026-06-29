from .mode import AIMode,AIRole

def build(history:list,memory:list,message:str,mode:AIMode,)->str:
    lines = []

    lines.append("以下是提供給 Assistant 的資訊。")
    lines.append("MEMORY 是長期記憶。")
    lines.append("HISTORY 是最近的聊天紀錄。")
    lines.append("CURRENT MESSAGE 是目前需要回答的訊息。")
    lines.append("")

    lines.append("===== MODE =====")
    lines.append(mode.value)
    lines.append("")

    lines.append("===== MEMORY =====")
    if memory:
        for item in memory:
            lines.append(item)
    else:
        lines.append("(None)")
    lines.append("")

    lines.append("===== HISTORY =====")
    if history:
        for chat in history:
            role = "User" if chat["role"] == AIRole.USER.value else "Assistant"
            lines.append(f"{role}: {chat['content']}")
    else:
        lines.append("(None)")

    lines.append("")
    lines.append("===== CURRENT MESSAGE =====")
    lines.append(f"User: {message}")
    return "\n".join(lines)