from ai import model,history,prompt
from .mode import AIMode,AIRole

async def chat(
    user_id:int,
    username:str,
    message:str,
    mode:AIMode,
) -> str:

    chat_history = history.load(user_id)
    prompt_text = prompt.build(history=chat_history,message=message,mode=mode,)
    reply = await model.generate(prompt_text)
    history.append(user_id,AIRole.USER,message)
    history.append(user_id,AIRole.ASSISTANT,reply)
    return reply