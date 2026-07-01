from ai import model,history,prompt,memory,remember
from .mode import AIMode,AIRole

async def chat(
    user_id:int,
    message:str,
    mode:AIMode,
) -> str:

    chat_history = history.load(user_id)[-50:]
    memory_list = memory.load(user_id)[-100:]
    prompt_text = prompt.build(history=chat_history,memory=memory_list,message=message,mode=mode,)

    reply = await model.generate(prompt_text,temperature=0.6,num_predict=500)

    history.append(user_id,AIRole.USER,message)
    history.append(user_id,AIRole.ASSISTANT,reply)

    try:
        memories = await remember.extract(message)
        for item in memories:
            memory.append(user_id,item)
    except Exception:
        pass
    return reply