import os
import re
from tqdm.auto import tqdm
from datetime import datetime
import discord
from dotenv import load_dotenv

from llm import vllm_endpoint
from crawler import crawling
from utils import save_json
import json

load_dotenv()

token = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
client = discord.Client(command_prefix='!',intents=intents)
ptn = re.compile(r"\d+번")
int_ptn = re.compile(r"(\d+)")

@client.event
async def on_ready():
    print(f'{client.user.name} 등장!')


@client.event
async def on_message(message):
    # bot이 스스로 보낸 메시지는 무시
    if message.author == client.user:
        return

    llm_exe = False
    today = datetime.today().strftime('%y%m%d')
    path = os.path.join(os.path.dirname(__file__), 'news', today + '.json')

    # 해외뉴스 명령어로 뉴스 요약
    if message.content.startswith('해외뉴스'):
        if os.path.isfile(path):
            with open(path, 'r', encoding="utf-8") as f:
                article = json.load(f)

            response = []
            text = f"""날짜 {today}, 기사 {len(article)}개
원하시는 기사의 번호를 입력해주세요.
아래 예시의 형식을 꼭 따라주세요.
예) 1번"""

            response.append(text)

        else:
            text_list, link_list = crawling()
            article = []

            for text, link in tqdm(zip(text_list, link_list), total = len(text_list), desc = 'generation'):
                article.append(vllm_endpoint(text).choices[0].message.content.rstrip() + '\n' + link)

            save_json(path, article)

            response = []
            text = f"""날짜 {today}, 기사 {len(article)}개
원하시는 기사의 번호를 입력해주세요.
아래 예시의 형식을 꼭 따라주세요.
예) 1번"""

            response.append(text)

    elif ptn.match(message.content):
        number = int_ptn.match(message.content).group()
        with open(path, 'r', encoding="utf-8") as f:
                article = json.load(f)
            
        response = []
        try:
            response.append(article[int(number)-1])
        except Exception as e:
            response.append(e)

    # LLM 일반 호출 
    else:
        response = [vllm_endpoint(message.content)]
        llm_exe = True

    for r in response:
        if llm_exe == True:
            await message.channel.send(r.choices[0].message.content)
        else:
            await message.channel.send(r)

client.run(token)
