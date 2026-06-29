from ai import model,history,prompt
from ai.mode import AIMode,AIRole

async def chat(
    user_id:int,
    username:str,
    message:str,
    mode:AIMode,
) -> str:

    history.append(user_id,AIRole.USER,message,)
    chat_history = history.load(user_id)
    prompt_text = prompt.build(history=chat_history,mode=mode,)
    reply = await model.generate(prompt_text)
    history.append(user_id,AIRole.ASSISTANT,reply,)
    return reply