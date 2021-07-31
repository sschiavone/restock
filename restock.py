import json
from square.client import Client

client = Client(
    access_token = 'EAAAEFv7_mfYuGUqCp8zYFqPQb5nPULMjLd7tNZa0qW4KgmN3oItAj-mrB1T25YR',
    environment='sandbox'
)


def get_catalog():
    catalog = client.catalog.list_catalog(types='ITEM')

    if catalog.is_success():
        for catalog_item in catalog.body['objects']:
    
            item_data   = catalog_item['item_data']
            try:
                item_category = item_data['category_id']
                item_name   = item_data['name']

                item_id     = item_data['variations'][0]['id']

                print(item_category)
            except:
                pass

            #for item in item_data['variations']:
                #print(item['id'])
            
    
            #print(item_name, item_id)
            #stock  = client.inventory.retrieve_inventory_count(item_id)
            #if stock.is_success():
            #    print(item_name, stock.body['counts'][0]['quantity'])
    
    elif catalog.is_error():
        print(catalog.errors)

get_catalog()

