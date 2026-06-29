from ai import model,history,prompt,memory,remember
from .mode import AIMode,AIRole

async def chat(
    user_id:int,
    message:str,
    mode:AIMode,
) -> str:

    chat_history = history.load(user_id)[-50:]
    memory_list = memory.load(user_id)
    prompt_text = prompt.build(history=chat_history,memory=memory_list,message=message,mode=mode,)

    print("========== PROMPT ==========")
    print(prompt_text)
    print("============================")

    reply = await model.generate(prompt_text)

    history.append(user_id,AIRole.USER,message)
    history.append(user_id,AIRole.ASSISTANT,reply)

    try:
        memories = await remember.extract(message)
        for item in memories:
            memory.append(user_id,item)
    except Exception:
        pass
    return reply