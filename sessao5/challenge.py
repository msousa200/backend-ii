import aiohttp
import asyncio
from datetime import datetime

async def fetch_html(session, url):
    """Fetch HTML content from a single URL"""
    try:
        start_time = datetime.now()
        async with session.get(url) as response:
            html = await response.text()
            end_time = datetime.now()
            return {
                'url': url,
                'html': html[:100] + '...',  
                'status': response.status,
                'time_taken': str(end_time - start_time)
            }
    except Exception as e:
        return {
            'url': url,
            'error': str(e),
            'status': 'failed'
        }

async def scrape_urls(urls):
    """Scrape multiple URLs concurrently"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_html(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def main():
    urls = [
        'https://python.org',
        'https://github.com',
        'https://stackoverflow.com',
        'https://fastapi.tiangolo.com',
        'https://docs.aiohttp.org'
    ]
    
    print(f"Starting scrape at {datetime.now()}")
    results = await scrape_urls(urls)
    
    print("\nScraping Results:")
    for result in results:
        print(f"\nURL: {result['url']}")
        print(f"Status: {result.get('status', 'N/A')}")
        if 'time_taken' in result:
            print(f"Time taken: {result['time_taken']}")
        if 'html' in result:
            print(f"HTML snippet: {result['html']}")
        if 'error' in result:
            print(f"Error: {result['error']}")

if __name__ == '__main__':
    asyncio.run(main())