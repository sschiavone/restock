import json
from   square.client import Client

client = Client(
    access_token = 'EAAAEFv7_mfYuGUqCp8zYFqPQb5nPULMjLd7tNZa0qW4KgmN3oItAj-mrB1T25YR',
    environment  = 'sandbox'
)

cat_print = '2VPZMNWFHYKEFVPM4L5EX6VW'

restock_list = []

def check_item_stock(item, min_stock):
    data = item['item_variation_data']
    stock = client.inventory.retrieve_inventory_count(item['id'])

    if stock.is_success():
        try:
            quantity = stock.body['counts'][0]['quantity']

            if int(quantity) <= min_stock:
                restock_list.append(item)
                #print(data['name'], data['sku'], quantity)
        except:
            pass


def get_catalog():
    catalog = client.catalog.list_catalog(types='ITEM')

    if catalog.is_success():
        for catalog_item in catalog.body['objects']:
    
            item_data = catalog_item['item_data']
            try:
                if item_data['category_id'] == cat_print:
                    for item in item_data['variations']:
                        check_item_stock(item, 1)

            except:
                pass

    elif catalog.is_error():
        print(catalog.errors)

get_catalog()

print(restock_list)



