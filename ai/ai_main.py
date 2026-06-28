from ai import mode,model 

async def chat(
    user_id:int,
    username:str,
    message:str,
    mode:mode.AIMode,
) -> str:
    
    prompt = message
    reply = await model.generate(prompt)
    return reply