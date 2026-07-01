import discord,asyncio
from playwright.async_api import async_playwright
from data import secret
from ai import model

def setup(tree):
    @tree.command(name="map",description="獲取神椿連邦帝國即時皇輿全覽圖")
    async def map(interaction):
        await interaction.response.defer()
        try:
            ai_task = asyncio.create_task(model.generate("想像一張記錄Minecraft伺服器最新樣貌的地圖","創作一句富有情感的短句，以一至三句自然完成。",temperature=0.7,num_predict=500,num_ctx=1024))
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page(viewport={"width":1440,"height":1440})
                await page.goto(secret.bluemap_url)
                await page.wait_for_timeout(15000)
                dl_task = page.wait_for_event("download")
                _, download = await asyncio.gather(page.evaluate("() => { if(window.bluemap) window.bluemap.takeScreenshot();}"), dl_task,)
                path = await download.path()

                try:
                    text = await ai_task
                except Exception:
                    text = "Someone tell StarShiningSnow there is a problem with my AI."
                file = discord.File(path, filename="map.png")
                embed = discord.Embed(title="神椿連邦帝國皇輿全覽圖",color=discord.Color.blue())
                embed.set_image(url="attachment://map.png")
                embed.set_footer(text=text)
                view = discord.ui.View().add_item(discord.ui.Button(label="網頁版皇輿全覽圖", url=secret.bluemap_url))
                await interaction.followup.send(file=file,embed=embed,view=view)
        except Exception:
            await interaction.followup.send(f"無法連接到地圖，請稍後再試。\n🔗：{secret.bluemap_url}")