import os
from square.client import Client
    
cat_print = '2VPZMNWFHYKEFVPM4L5EX6VW'

class Stock:
    def __init__(self):
        self.client = Client(
            access_token='EAAAEFv7_mfYuGUqCp8zYFqPQb5nPULMjLd7tNZa0qW4KgmN3oItAj-mrB1T25YR',
            environment='sandbox')

    def get_sku(self, item_list):
        sku_list = []
        for item in item_list:
            sku_list.append(item['item_variation_data']['sku'])
          
        return sku_list

    def check_item_stock(self, item, min_stock):
        data = item['item_variation_data']
        stock = self.client.inventory.retrieve_inventory_count(item['id'])
    
        if stock.is_success():
            try:
                quantity = stock.body['counts'][0]['quantity']
    
                if int(quantity) <= min_stock:
                    return True
                else:
                    return False
            except:
                return False

    def get_low_stock(self, category_id, min_stock):
        catalog = self.client.catalog.list_catalog(types='ITEM')

        if catalog.is_success():
            restock_list = []
            for catalog_item in catalog.body['objects']:
                item_data = catalog_item['item_data']
                try:
                    if item_data['category_id'] == cat_print:
                        for item in item_data['variations']:
                            if self.check_item_stock(item, min_stock):
                                restock_list.append(item)
                except:
                    pass
            return self.get_sku(restock_list)

        elif catalog.is_error():
            print(catalog.errors)


stock = Stock()

low_stock = stock.get_low_stock(cat_print, 1)

#lowStock = get_sku(get_low_stock())

print(low_stock)

