def build(history:list,message:str)->str:
    lines = []

    lines.append("以下是提供給 Assistant 的資訊。")
    lines.append("HISTORY 是最近的聊天紀錄。")
    lines.append("CURRENT MESSAGE 是目前需要回答的訊息。")
    lines.append("")

    lines.append("===== HISTORY =====")
    if history:
        for chat in history:
            role = "User" if chat["role"] == "user" else "Assistant"
            lines.append(f"{role}: {chat['content']}")
    else:
        lines.append("(None)")

    lines.append("")
    lines.append("===== CURRENT MESSAGE =====")
    lines.append(f"User: {message}")
    return "\n".join(lines)