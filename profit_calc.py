import requests
import pet_auction_search
import asyncio

# Request API Data
def get_quick_status(products_list):
    url = "https://api.hypixel.net/v2/skyblock/bazaar"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            products_quick_status = {}
            products = data["products"]
            for product_id in products_list:
                if product_id in products:
                    quick_status = products[product_id]["quick_status"]
                    products_quick_status[product_id] = quick_status
                else:
                    print(f"Product '{product_id}' not found.")
            return products_quick_status
        else:
            print("Request was not successful.")
    else:
        print("Failed to retrieve data from the API.")


# Lvl 300 Arachne (Callings)
async def t1(number_callings):
    # Get bazaar prices
    products_list = ["ENCHANTED_STRING", "ENCHANTED_SPIDER_EYE", "ARACHNE_KEEPER_FRAGMENT", "ESSENCE_SPIDER", "ARACHNE_FRAGMENT", "ARACHNE_FANG"]
    products_quick_status = get_quick_status(products_list)
    if products_quick_status:
        for product_id, quick_status in products_quick_status.items():
            if product_id == "ENCHANTED_STRING":
                string_sell = quick_status["sellPrice"]
            elif product_id == "ENCHANTED_SPIDER_EYE":
                eye_sell = quick_status["sellPrice"]
            elif product_id == "ARACHNE_KEEPER_FRAGMENT":
                calling_price = quick_status["buyPrice"]
            elif product_id == "ESSENCE_SPIDER":
                essence_sell = round(quick_status["sellPrice"],2)
            elif product_id == "ARACHNE_FRAGMENT":
                frag_sell = quick_status["sellPrice"]
            elif product_id == "ARACHNE_FANG":
                fang_sell = quick_status["sellPrice"]
        
        # Initial calculations
        number_runs = int(number_callings / 4) # Rounds down
        total_price = round(number_callings * calling_price, 2)
        
        # Tara pet profit calc
        items_to_search = ["Tarantula"]
        pet_auctions = await pet_auction_search.search_auctions(items_to_search)
        ah_pet_sell = pet_auctions['EPIC'][0]
        if ah_pet_sell == None:
            ah_pet_sell = 0
        npc_pet_sell = 2000
        if ah_pet_sell > npc_pet_sell: # Setting baseline profit
            pet_sell = ah_pet_sell
        else:
            pet_sell = npc_pet_sell

        pet_profit = 0.02 * number_runs * pet_sell # 2% droprate (1/50) * numruns * sell

        # Arachne fang profit calc
        fang_profit = 0.1 * number_runs * fang_sell # 10% droprate (1/10) * numruns * sell

        # E eye profit calc
        eye_craft_num = round(15 * number_runs / 160, 0) # 15 * numruns / craftamount (10-20 eyes/run = avg 15)
        avg_eye_profit = eye_sell * (number_runs + eye_craft_num) # 0-2 e eyes/run = avg 1 (numruns == e eyedrop/run)

        # E string profit calc
        string_craft_num = round(15 * number_runs / 160, 0) # 15 * numruns / craftamount (10-20 string/run = avg 15)
        avg_string_profit = string_sell * (number_runs + string_craft_num) # 0-2 e string/run = avg 1 (numruns == e stringdrop/run)

        # Essence profit calc
        armor_essence = 1.2 * 0.1 * number_runs * 4 * 5  # 20% chance to double essence, 10% chance, 4 armor pieces, 5 essence per
        total_essence = armor_essence + (8 * number_runs) # 8 essence/run
        essence_profit = total_essence * essence_sell

        # Soul string profit calc
        soulstring_profit = 9.5 * number_runs * 5000 # 5-6/run (avg 5.5) + 4 (assuming 4 callings placed) * numruns * npcsell

        # Arachne frag profit calc
        frag_profit = frag_sell * number_runs # 1 frag/run

        # Killcoins / boss estimate
        kill_coins = 1300 * 15 * number_runs # coins/kill * 15 kills (assuming you get kill credit for half the brood - 30 total) * numruns

        total_profit = round((pet_profit + avg_eye_profit + avg_string_profit + essence_profit + soulstring_profit + fang_profit + frag_profit + kill_coins) - total_price, 2) # round to 2dp
        return number_runs, total_profit, total_price, essence_sell, pet_sell # essencesell, petsell & numruns are included in the output for more info to user

## Droprates/t1 boss
    # Epic tara pet 2%
    # 0-2 e string
    # 10-20 string
    # 0-2 e eye
    # 10-20 eye
    # Arachne Frag
    # Arachne Fang 10%
    # Arachne Armor 10% / Piece (4 total)
    # Essence 8
    # 5-6 + (num callings placed) soulstring
    # 1300 coins/brood kill


# Lvl 500 Arachne (Crystals)
async def t2(number_crystals):
    # Get bazaar prices
    products_list = ["ARACHNE_FRAGMENT", "ENCHANTED_STRING", "ENCHANTED_SPIDER_EYE", "ESSENCE_SPIDER"]
    products_quick_status = get_quick_status(products_list)
    if products_quick_status:
        for product_id, quick_status in products_quick_status.items():
            if product_id == "ARACHNE_FRAGMENT":
                frag_price = quick_status["buyPrice"]
            elif product_id == "ENCHANTED_STRING":
                string_price = quick_status["buyPrice"]
                string_sell = quick_status["sellPrice"]
            elif product_id == "ENCHANTED_SPIDER_EYE":
                eye_price = quick_status["buyPrice"]
                eye_sell = quick_status["sellPrice"]
            elif product_id == "ESSENCE_SPIDER":
                essence_sell = quick_status["sellPrice"]

        # Calculate price/crystal
        total_string = number_crystals * 30
        total_eye = number_crystals * 8
        total_frag = number_crystals * 3
        total_price = round(total_string * string_price + total_eye * eye_price + total_frag * frag_price, 2)

        # Tara pet profit calc
        items_to_search = ["Tarantula"]
        pet_auctions = await pet_auction_search.search_auctions(items_to_search)
        ah_pet_sell = pet_auctions['LEGENDARY'][0]
        if ah_pet_sell == None:
            ah_pet_sell = 0
        npc_pet_sell = 100000
        if ah_pet_sell > npc_pet_sell: # Setting baseline profit
            pet_sell = ah_pet_sell
        else:
            pet_sell = npc_pet_sell

        pet_profit = 0.02 * number_crystals * pet_sell # 2% droprate (1/50) * numruns * sell

        # E eye profit calc
        eye_craft_num = round(35 * number_crystals / 160, 0) # 35 * numruns / craftamount (10-60 eyes/run = avg 35)
        avg_eye_profit = eye_sell * (3 * number_crystals + eye_craft_num) # 0-6 e eyes/run = avg 3

        # E string profit calc
        string_craft_num = round(35 * number_crystals / 160, 0) # 35 * numruns / craftamount (10-60 string/run = avg 35)
        avg_string_profit = string_sell * (3 * number_crystals + string_craft_num) # 0-6 e string/run = avg 3

        # Essence profit calc
        armor_essence = 1.2 * 0.25 * number_crystals * 5 * 5  # 20% chance to double essence, 25% drop chance, 5 armor pieces, 5 essence per
        total_essence = armor_essence + (30 * number_crystals) # 30 essence/run
        essence_profit = total_essence * essence_sell

        # Soul string profit calc
        soulstring_profit = 43 * number_crystals * 5000 # 42-44/run (avg 43) * numruns * npcsell

        # Dark Queen's Soul profit calc
        dark_queen_profit = 5000 * number_crystals # The ah price never moves :strong:

        # Killcoins / boss estimate
        kill_coins = 2400 * 15 * number_crystals # coins/kill * 15 kills (assuming you get kill credit for half the brood - 30 total) * numruns


        total_profit = round((pet_profit + avg_eye_profit + avg_string_profit + essence_profit + soulstring_profit + dark_queen_profit + kill_coins) - total_price, 2) # round to 2dp

        return number_crystals, total_profit, total_price, essence_sell, pet_sell # essencesell, petsell & numcrystals are included in the output for more info to user

## Droprates/t2 boss
    # Leg tara pet 2%
    # 0-6 e string
    # 10-60 string
    # 0-6 e eye
    # 10-60 eye
    # Arack 25%
    # Armor 25% / Piece
    # Essence 30
    # Dark Queen's Soul
    # 42-44 soulstring
    # 2500 coins/brood kill