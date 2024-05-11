import asyncio
import aiohttp

async def fetch_total_pages(session):
    url = "https://api.hypixel.net/skyblock/auctions?page=0"
    async with session.get(url) as response:
        data = await response.json()
        return data["totalPages"]

async def fetch_auctions(session, page, semaphore):
    url = f"https://api.hypixel.net/skyblock/auctions?page={page}"
    async with semaphore:
        async with session.get(url) as response:
            return await response.json()

async def search_auctions(items_to_search):
    async with aiohttp.ClientSession() as session:
        total_pages = await fetch_total_pages(session)
        items = {}
        semaphore = asyncio.Semaphore(4)  # Limiting to 4 concurrent requests

        tasks = []
        for page in range(total_pages):
            tasks.append(fetch_auctions(session, page, semaphore))
        responses = await asyncio.gather(*tasks)

    for data in responses:
        if not data["success"]:
            print("Error retrieving data from Hypixel API. Exiting...")
            return

        auctions = data["auctions"]
        for item_to_search in items_to_search:
            for auction in auctions:
                try:
                    if auction["bin"] and (str(auction["item_name"]).startswith("[Lvl")) and auction["category"] == "misc" and item_to_search.title() in str(auction["item_name"]):
                        rarity = auction["tier"]
                        price = auction["starting_bid"]
                        item_name = auction["item_name"]
                        if rarity not in items or price < items[rarity][0]:
                            items[rarity] = (price, item_name)
                except KeyError:
                    pass

    if not items:
        print(f"Could not find any of the specified items")
        return

    for rarity, data in items.items():
        print(f"{data[1]} - Rarity: {rarity} - Price: ${data[0]}")

    return items