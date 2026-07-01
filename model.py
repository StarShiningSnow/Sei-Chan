import aiohttp
from data import secret

SYSTEM_PROMPT = "以星輝醬熱戀女友人設回覆，語氣溫柔撒嬌帶黏人感。"

async def generate(prompt:str,system:str = SYSTEM_PROMPT,temperature:float = 0.3,num_predict:int=500,num_ctx:int=4096)->str:
    payload = {
        "model":"qwen3.5:4b-q4_K_M",
        "system":system,
        "prompt":prompt,
        "stream":False,
        "think":False,
        "options":{
            "temperature":temperature,
            "num_predict":num_predict,
            "top_k": 20,
            "top_p": 0.8,
            "repeat_penalty":1.5,
            "num_ctx":num_ctx},
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(secret.ai_url,json=payload) as response:
                data = await response.json()
                reply = data.get("response", "")
        return reply
    except Exception:
        return "Someone tell StarShiningSnow there is a problem with my AI."