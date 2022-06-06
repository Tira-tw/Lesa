import discord
import json
import os
from discord import Webhook, RequestsWebhookAdapter
import random, string


print("--------------------------------------------------------")
print("開發者已獲得源代碼作者修改 | 發布許可 , 請勿修改 | 公開")
print("源代碼作者 :")
print("https://github.com/HansHans135")
print("--------------------------------------------------------")
print("源代碼 :")
print("https://github.com/HansHans135/across_guild")
print("--------------------------------------------------------")
print("開發者Discord :")
print("天然呆幻月#1314")
print("--------------------------------------------------------")
print("開發者Discord支援區 :")
print("https://discord.gg/3S5BgMTx47")
print("--------------------------------------------------------")



with open ("config.json",mode="r",encoding="utf-8") as filt:
    data = json.load(filt)
前輟 = data["prefix"]
TOKEN = data["token"]
OWNER_ID = data["owner"]


client = discord.Client()

@client.event   
async def on_ready():
    print('BOT已上線，Botname：',client.user)
    status_w = discord.Status.online
    activity_w = discord.Activity(type=discord.ActivityType.watching, name=f"{前輟}help")
    await client.change_presence(status= status_w, activity=activity_w)


@client.event
async def on_message(message):
    if message.content == f"{前輟}help":
        await message.delete()
        embed = discord.Embed(title="指令", description="***全部指令只限於群組管理員使用***\n 你也可以連別人的群組 , 只需要對方給你跨群連結代碼就好\n就很像Connections Bot\n官方的跨群連結代碼 : `dGrJC`\n開發者Discord :\n[天然呆幻月#1314](https://top.gg/user/212975187460038656)\n官方Discord群組 :\n https://discord.gg/3S5BgMTx47", color=0x04f108)
        embed.add_field(name=f"{前輟}help", value="指令功能查詢")
        embed.add_field(name=f"{前輟}new", value="創建一個跨群連結代碼")
        embed.add_field(name=f"{前輟}start", value=f"{前輟}start `webhook網址` `跨群連結代碼`")
        embed.add_field(name=f"{前輟}now", value="查看有幾個頻道連線")
        embed.add_field(name=f"{前輟}dlt", value="取消連線")
        await message.channel.send(content=None, embed=embed)

#群組數量
    if message.content == f'{前輟}now':
        await message.delete()
        with open (f"server/{message.channel.id}.json",mode="r",encoding="utf-8") as filt:
            data = json.load(filt)
        with open(f'code/{data["code"]}.txt') as myfile:
            total_lines = sum(1 for line in myfile)
        await message.channel.send(f"目前有`{total_lines}`個頻道連線")

#斷開連接
    if message.content == f'{前輟}dlt':
        if message.author.guild_permissions.manage_messages:
            with open (f"server/{message.channel.id}.json",mode="r",encoding="utf-8") as filt:
                data = json.load(filt)
            fileTest = f"server/{message.channel.id}.json"
            os.remove(fileTest)
            with open(f'code/{data["code"]}.txt','r') as r:
                lines=r.readlines()
            with open(f'code/{data["code"]}.txt','w') as w:
                for l in lines:
                    if f'{data["wh"]}\n' not in l:
                        w.write(l) 
            await message.channel.send("已取消連線")
        else:
            await message.channel.send("需要有管理權限才可取消連接")

#強制斷聯
    if message.content == f'{前輟}opdlt':
        if message.author.id == int(OWNER_ID):
            with open (f"server/{message.channel.id}.json",mode="r",encoding="utf-8") as filt:
                data = json.load(filt)
            fileTest = f"server/{message.channel.id}.json"
            os.remove(fileTest)
            with open(f'code/{data["code"]}.txt','r') as r:
                lines=r.readlines()
            with open(f'code/{data["code"]}.txt','w') as w:
                for l in lines:
                    if f'{data["wh"]}\n' not in l:
                        w.write(l) 
            await message.channel.send("已取消連線")
        else:
            await message.channel.send("您必須是擁有者才可取消連接")

#連接碼
    if message.content == f'{前輟}new':
        if message.author.guild_permissions.manage_messages:
            代碼 = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
            filepath = f"code/{代碼}.txt"
            if os.path.isfile(filepath):
                return
            else:
                await message.delete()
                tmp = message.content.split(" ",2)
                with open (f"code/{代碼}.txt",mode="w",encoding="utf-8") as filt:
                    await message.channel.send("建立成功!,請查看私訊")
                await message.author.send(f'您的跨群連結代碼:`{代碼}`')
        else:
            await message.channel.send("你需要有管理權限才可創建跨群連結代碼")

#連接
    if message.content.startswith(f'{前輟}start'):
        if message.author.guild_permissions.manage_messages:
            await message.delete()
            tmp = message.content.split(" ",2)
            wh網址 = tmp[1]
            if len(tmp) == 1:
              await message.channel.send(f"`{前輟}start` `webhook網址` `跨群連結代碼`")
            tmp = message.content.split(f"{wh網址} ",2)
            代碼 = tmp[1]
            #亨哥0126
            if len(tmp) == 1:
              await message.channel.send(f"`{前輟}start` `webhook網址` `跨群連結代碼`")
            else:
                filepath = f"code/{代碼}.txt"
                if os.path.isfile(filepath):
                    filepath = f"server/{message.channel.id}.json"
                    if os.path.isfile(filepath):
                        await message.channel.send("您已經連線了")
                    else:
                        with open (f"server/{message.channel.id}.json",mode="w",encoding="utf-8") as filt:
                          data = {"code":代碼,"wh":wh網址}
                          json.dump(data,filt)
                        with open(f"code/{代碼}.txt", 'a') as filt:
                            filt.write(f'{wh網址}\n')
                        await message.channel.send("連線成功!")
                else:
                    await message.channel.send(f"未找到跨群連結代碼:`{代碼}`")
        else:
            await message.channel.send("需要有管理權限才可連接跨群")
                    
#訊息
    if message.author.bot:
        return
    else:
        filepath = f"server/{message.channel.id}.json"
        if os.path.isfile(filepath):
            if "@everyone" in message.content :
                return
            else:
                if "@here" in message.content :
                    return
                else:
                    with open (f"server/{message.channel.id}.json",mode="r",encoding="utf-8") as filt:
                        data = json.load(filt)
                        use_code = data["code"]
                    await message.delete()
                    f = open(f"code/{use_code}.txt") 
                    lines = f.readlines()#讀取全部內容 
                    for line in lines :
        #print (line)
                        webhook = Webhook.from_url(line, adapter=RequestsWebhookAdapter()) 
                        webhook.send(username=f"{message.guild.name} | {message.author}", avatar_url=message.author.avatar_url, content=message.content)

client.run(TOKEN)
