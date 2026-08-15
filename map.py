import requests,discord,secret,io
from PIL import Image

def setup(tree):
    @tree.command(description="皇帝陛下、総理閣下、並びに高官の皆様へ報告です。連邦省情報局により最新の帝国領土測量図が更新されました。広大な我が帝国の威光と栄華を、どうぞご覧くださいませ！ (⁠✧⁠ω⁠✧⁠)")
    async def map(interaction):
        await interaction.response.defer()
        output = Image.new("RGBA",(2505,2505))
        for x in range(-2, 3):
            for z in range(-2, 3):
                url = f"http://127.0.0.1:8100/maps/world/tiles/1/x{x}/z{z}.png"
                img = Image.open(io.BytesIO(requests.get(url).content))
                output.paste(img.crop((0,0,501,501)),((x+2)*501,(z+2)*501))
        buffer = io.BytesIO()
        output.save(buffer,"PNG")
        buffer.seek(0)
        file = discord.File(buffer,"map.png")
        embed = discord.Embed(title="🗺️ 帝国領土全域図 閲覧報告",color=discord.Color.pink(),url=f"http://{secret.wan_ip}:8100")
        embed.set_image(url="attachment://map.png")
        embed.set_footer(text="⚙️ 連邦省情報局管轄システム • 天皇陛下万歳！")
        await interaction.followup.send(file=file,embed=embed)