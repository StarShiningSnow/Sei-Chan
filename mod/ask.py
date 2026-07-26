from ai import model,history,prompt

def setup(tree):
    @tree.command(name="ask",description="直接和星輝醬對話吧！")
    async def ask(interaction,question:str):
        await interaction.response.defer()

        user_id = interaction.user.id

        prompt_text = prompt.build(history=history.load(user_id)[-50:],message=question)

        reply = await model.generate(prompt_text,temperature=0.6,num_predict=500,
        )

        history.append(user_id,"user",question)
        history.append(user_id,"assistant",reply)

        await interaction.followup.send(reply)