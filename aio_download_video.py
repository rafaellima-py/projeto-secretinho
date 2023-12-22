import aiofiles
import httpx
import asyncio
from bs4 import BeautifulSoup
from pathlib import Path

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
    'Cache-Control': 'no-cache'
}

async def fetch_page(url, headers, timeout=10):
    async with httpx.AsyncClient() as session:
        try:
            response = await session.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.text
        except (httpx.HTTPError, httpx.TimeoutException) as e:
            print(f'Erro ao carregar a página: {e}')
            return None

async def extract_video_links(page_content):
    links = set()
    if page_content:
        soup = BeautifulSoup(page_content, 'html.parser')
        source_tags = soup.find_all('source')
        for tag in source_tags:
            try:
                link_src = tag['src']
                links.add(link_src)
            except KeyError:
                print(f'Aviso: A tag source não possui atributo src.')
    return links

async def download_single_video(client, link, pasta):
    nome = link.split('/')[-1]
    print(f'Baixando {nome}')
    
    try:
        response = await client.get(link, headers=header2, timeout=60*3)
        response.raise_for_status()

        async with aiofiles.open(Path(pasta) / nome, 'wb') as f:
            await f.write(response.content)

        print(f'Download de {nome} concluído')
    except (httpx.HTTPError, httpx.TimeoutException) as e:
        print(f'Erro ao baixar {nome}: {e}')

async def download_videos(url, pasta):
    page_content = await fetch_page(url, headers=header1)
    video_links = await extract_video_links(page_content)

    if video_links:
        print(f'Lista Carregada: {len(video_links)}')

        async with httpx.AsyncClient() as client:
            tasks = [download_single_video(client, link, pasta) for link in video_links]
            await asyncio.gather(*tasks)

async def main():
    await download_videos('https://www.erome.com/a/vgjdhL3k', 'teste')

if __name__ == '__main__':
    asyncio.run(main())
