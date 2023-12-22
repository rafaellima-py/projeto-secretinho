import aiofiles
import httpx
import asyncio
from bs4 import BeautifulSoup
from pathlib import Path
import re

header1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Cache-Control': 'no-cache'
}

links_image = []

async def download_single_image(client, link, pasta):
    match = re.search(r'/([^/]+)\.\w+\?v=(\d+)', link)

    if match:
        filename = match.group(1) + '.jpg'
        print(f'Baixando {filename}')

        response = await client.get(link, headers=header1)
        response.raise_for_status()

        async with aiofiles.open(pasta / filename, 'wb') as f:
            await f.write(response.content)
            print(f'Download de {filename} concluído')

async def download_images(url, pasta):
    pasta = Path(pasta)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=header1)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            img = soup.find_all('img')

            if img:
                for link in img:
                    src = link.get('data-src')
                    if src not in links_image and src is not None:
                        links_image.append(src)

                print(f'Lista Carregada: {len(links_image)}')

                tasks = [download_single_image(client, link, pasta) for link in links_image]
                await asyncio.gather(*tasks)

        except (httpx.HTTPError, aiofiles.OSFError, asyncio.CancelledError) as e:
            print(f'Erro durante o processo: {e}')

async def main():
    try:
        await download_images(url='https://www.erome.com/a/kTbDwMJ0', pasta='teste')
    except Exception as e:
        print(f'Erro durante a execução do script: {e}')

if __name__ == '__main__':
    asyncio.run(main())
