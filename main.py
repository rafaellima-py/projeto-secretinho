import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

from pathlib import Path
import asyncio
import aiohttp
from aio_download_image import *
from aio_download_video import *

header1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'Cache-Control': 'no-cache' 
    }
header2 = {
        'Accept': '*/*',
        'Accept-Encoding': 'identity;q=1, *;q=0',
        'Accept-Language': 'pt-BR,pt;q=0.9',
        'Connection': 'keep-alive',
        'Dnt': '1',
        'Host': 'v92.erome.com',
        
        'Referer': 'https://www.erome.com/',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'video',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'Cache-Control': 'no-cache'  # Adicionando o cabeçalho para indicar que não deve ser usado em cache
    }
nome = 'MC Chinesa'
nome = quote(nome)
pasta = Path(nome)
if not pasta.is_dir():
        pasta.mkdir(parents=True)
        
        
        
        
async def search():     
    async with aiohttp.ClientSession() as sessao:
        request = await sessao.get(f'https://www.erome.com/search?q={nome}', headers=header1)
        existe = True
    soup = BeautifulSoup(await request.text(), 'html.parser')
    corpo = soup.find('body').text
    if 'No results' in corpo:
        existe = False
        print('Não existe')
    if existe:
        a = soup.find_all('a', class_='album-link')
        for link in a:
            await download_images(link.get('href'), pasta)
            await download_videos(link.get('href'), pasta)














async def main():
    
    await search()
if __name__ == '__main__':
    asyncio.run(main())