import os
import json
import logging

import asyncio
from tqdm.auto import tqdm
import datetime
from datetime import datetime as dt

from zoneinfo import ZoneInfo

import discord
from discord.ext import tasks
from dotenv import load_dotenv

from llm import vllm_endpoint
from crawler import crawling
from utils import save_txt, load_txt, save_json

logging.basicConfig(level=logging.WARNING)
load_dotenv()

token = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    '''LLM 일반 대화'''
    # bot이 스스로 보낸 메시지는 무시
    if message.author == client.user:
        return

    # LLM 일반 호출
    response = vllm_endpoint(message.content, news=False)
    if response is None:
        pass
    else:
        await message.channel.send(response)

# @client.event
async def auto_crawler():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    # 공개 스레드 만들기
    thread_name = dt.now().strftime('%Y/%m/%d') + " CNN 해외 뉴스"
    threads = [thread for thread in channel.threads if thread.name == thread_name ]

    if threads:
        thread = threads[-1]
    else:
        thread = await channel.create_thread(name=thread_name, type=discord.ChannelType.public_thread)
        thread_link = thread.jump_url 
        await channel.send(f"{thread_link}")
        
    # 수집된 뉴스 링크
    file_path = os.path.join("news", "thread_name.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            news_link = json.load(file)
    else:
        news_link = dict()

    # 크롤링
    text_list, link_list = crawling()
    print(f"{len(link_list)}개 뉴스 크롤링 완료")

    cnt = 0
    for text, link in tqdm(zip(text_list, link_list), total = len(text_list), desc = 'generation'):
        # 수집되지 않은 link면 요약
        if link not in news_link and len(text)<2000:
            output = vllm_endpoint(text)
            news_link[link] = output
            if output is None:
                pass
            else:
                # 스레드에 메시지 전송
                message = output.rstrip() + '\n' + str(link)
                await thread.send(message)
                cnt += 1
        if cnt ==2: break
    
    save_json(file_path, news_link)
    print("저장 완료")

@client.event
async def on_ready():
    global is_first_run
    if is_first_run:
        is_first_run = False
        print(f'{client.user.name} 등장!')
        await auto_crawler()
        
        print("bot 종료")
    else:
        print('재연결')
    await client.close()
# 봇 실행
is_first_run = True
client.run(token)
