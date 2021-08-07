import os
from square.client import Client
    
cat_print = '2VPZMNWFHYKEFVPM4L5EX6VW'

class Stock:
    def __init__(self):
        self.client = Client(
            access_token='EAAAEFv7_mfYuGUqCp8zYFqPQb5nPULMjLd7tNZa0qW4KgmN3oItAj-mrB1T25YR',
            environment='sandbox')

    def check_item_stock(self, item):
        stock = self.client.inventory.retrieve_inventory_count(item['id'])
    
        if stock.is_success():
            return  int(stock.body['counts'][0]['quantity'])

    def get_low_stock(self, category_id, min_stock):
        catalog = self.client.catalog.list_catalog(types='ITEM')

        if catalog.is_success():
            restock_list = []
            for catalog_item in catalog.body['objects']:
                item_data = catalog_item['item_data']
                try:
                    if item_data['category_id'] == cat_print:
                        for item in item_data['variations']:
                            stock = self.check_item_stock(item)
                            if stock < min_stock:
                                sku = item['item_variation_data']['sku']
                                restock_list.append([sku, (min_stock-stock)])
                except:
                    pass
            return restock_list

        elif catalog.is_error():
            print(catalog.errors)


stock = Stock()

low_stock = stock.get_low_stock(cat_print, 3)

print(low_stock)

