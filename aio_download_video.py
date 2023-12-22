import aiohttp
from bs4 import BeautifulSoup
import asyncio
import aiofiles
from pathlib import Path
import httpx
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

links = []


async def download_video(url, pasta):
    pasta = Path(pasta)
    async with httpx.AsyncClient() as session:
        try:
            response = await session.get(url, headers=header1, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup( response.text, 'html.parser')
            source = soup.find_all('source')
            
            for link in source:
                try:
                    link_src = link['src']
                    if link_src not in links:
                        links.append(link_src)
                except KeyError:
                    print(f'Aviso: A tag source não possui atributo src.')

            print(f'Lista Carregada: {len(links)}')

            for link in links:
                nome = link.split('/')[-1]
                print(f'Baixando {nome}')
                
                try:
                    response = await session.get(link, headers=header2, timeout=60*3)

                    async with aiofiles.open(pasta / nome, 'wb') as f:
                            await f.write(response.content)
                    
                    print(f'Download de {nome} concluído')
                    
                except (aiohttp.ClientError, aiohttp.ClientResponseError) as e:
                    print(f'Erro ao baixar {nome}: {e}')

        except (aiohttp.ClientError, aiohttp.ClientResponseError) as e:
            print(f'Erro ao carregar a página: {e}')

async def main():
    await download_video('https://www.erome.com/a/vgjdhL3k', 'teste')

if __name__ == '__main__':
    asyncio.run(main())
