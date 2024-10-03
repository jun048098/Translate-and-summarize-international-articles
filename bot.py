import os
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
from utils import save_txt, load_txt


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


# 수집 시간 00:01
@tasks.loop(time=datetime.time(hour=12, minute=49, tzinfo=ZoneInfo('America/New_York')))
async def auto_crawler():
    '''
    매일 00:01분에 디스코드 스레드 생성
    1시간 간격 뉴스 크롤링
    스레드에 뉴스 요약 정보를 보내기
    '''
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    # 하루동안 수집된 뉴스 링크
    news_link = set()

    # 공개 스레드 만들기
    thread_name = dt.now().strftime('%Y/%m/%d') + " CNN 해외 뉴스"
    thread = await channel.create_thread(name=thread_name, type=discord.ChannelType.public_thread)
    thread_link = thread.jump_url  
    await channel.send(f"{thread_link}")

    # 생성된 스레드 링크에 뉴스 요약
    for _ in range(10):
        text_list, link_list = crawling()
        for text, link in tqdm(zip(text_list, link_list), total = len(text_list), desc = 'generation'):
            # 수집되지 않은 link면 요약
            if link not in news_link:
                news_link.add(link)
                output = vllm_endpoint(text)
                if output is None:
                    pass
                else:
                    # 스레드에 메시지 전송
                    message = output.rstrip() + '\n' + str(link)
                    await thread.send(message)

        # 1 시간마다 수집
        await asyncio.sleep(3600)


@client.event
async def on_ready():
    print(f'{client.user.name} 등장!')
    auto_crawler.start()


# 봇 실행
client.run(token)