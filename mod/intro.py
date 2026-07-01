from ai import model

def setup(tree):
    @tree.command(name="intro",description="讓星輝醬自我介紹")
    async def intro(interaction):
        await interaction.response.defer()
        PROMPT = "自我介紹，大概一至三句話。"
        try:
            text = await model.generate(prompt=PROMPT, temperature=0.7, num_predict=300, num_ctx=1024)
        except Exception:
            text = "Someone tell StarShiningSnow there is a problem with my AI."
        await interaction.followup.send(text)