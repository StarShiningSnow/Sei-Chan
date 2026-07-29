from ai import model

def setup(tree):
    @tree.command(name="intro",description="想更了解星輝醬嗎？人家來跟親愛的自我介紹囉～")
    async def intro(interaction):
        await interaction.response.defer()
        PROMPT = "自我介紹，大概三至五句話。"
        try:
            text = await model.generate(prompt=PROMPT, temperature=0.7, num_predict=300, num_ctx=1024)
        except Exception:
            text = "Someone tell StarShiningSnow there is a problem with my AI."
        await interaction.followup.send(text)