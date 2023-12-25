import httpx
import asyncio
import logging
from bs4 import BeautifulSoup
from elastic import index_scraped_item
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

async def fetch(link, client):
    try:
        resp = await client.get(link, headers=header)
        resp.raise_for_status()  # Raise HTTPError for bad responses
    except httpx.HTTPError as e:
        logger.error(f"Error fetching {link}: {e}")
        return None

    logger.info(f'Scraping data from: {link} - {resp.status_code}')
    soup = BeautifulSoup(resp.text, 'lxml')
    item = {}
    item['url'] = link
    item['title'] = soup.select_one('span.hero__primary-text').text
    item['image'] = soup.select_one('img.ipc-image')['src']

    main = soup.select('li.ipc-metadata-list__item')
    for dat in main:
        if 'Director' in str(dat):
            item['director'] = dat.select_one('a').text

        if 'Stars' in str(dat):
            item['cast'] = [x.text for x in dat.select('a') if x.text != 'Stars' and x.text != '']

    logger.info(item)
    return item

async def fetch_all(links, delay_seconds=1):
    async with httpx.AsyncClient(timeout=5) as client:
        for link in links:
            await asyncio.sleep(delay_seconds)  # Introduce the delay
            task = fetch(link, client)
            scraped_item = await task

            # Index non-None scraped items
            if scraped_item is not None:
                index_scraped_item(scraped_item)

def scrape_data():
    url = "https://www.imdb.com/chart/top/"
    with httpx.Client(timeout=10) as client:
        try:
            resp = client.get(url, headers=header)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            logger.error(f"Error fetching IMDb top chart page: {e}")
            return

        logger.info(f'Successfully fetched IMDb top chart page - {resp.status_code}')
        soup = BeautifulSoup(resp.text, 'lxml')
        links = ['https://www.imdb.com' + x['href'] for x in soup.select('a.ipc-title-link-wrapper')]

    asyncio.run(fetch_all(links))

# if __name__ == '__main__':
#     start = time.time()
#     scraper()
#     end = time.time()
#     print(f'**** time elapsed {round(end-start,2)} seconds ****')
