import json
from square.client import Client
    
client = Client(
  access_token='EAAAEFv7_mfYuGUqCp8zYFqPQb5nPULMjLd7tNZa0qW4KgmN3oItAj-mrB1T25YR',
  environment='sandbox'
)

cat_print = '2VPZMNWFHYKEFVPM4L5EX6VW'

def get_sku(item_list):
  sku_list = []
  for item in item_list:
    sku_list.append(item['item_variation_data']['sku'])
    
  return sku_list


def check_item_stock(item, min_stock):
  data = item['item_variation_data']
  stock = client.inventory.retrieve_inventory_count(item['id'])

  if stock.is_success():
    try:
      quantity = stock.body['counts'][0]['quantity']

      if int(quantity) <= min_stock:
        return True
      else:
        return False
    except:
      return False


def get_low_stock():
  catalog = client.catalog.list_catalog(types='ITEM')

  if catalog.is_success():
    restock_list = []
    for catalog_item in catalog.body['objects']:

      item_data = catalog_item['item_data']
      try:
        if item_data['category_id'] == cat_print:
          for item in item_data['variations']:
            if check_item_stock(item, 1):
              restock_list.append(item)

      except:
        pass
    return restock_list

  elif catalog.is_error():
    print(catalog.errors)


lowStock = get_sku(get_low_stock())

print(lowStock)

