import os
from square.client import Client

PRINT = True

art_path  = 'C:/Users/Scott/Desktop/Art/Prints/'
list_path = 'C:/Users/Scott/Desktop/Scotts_Stuff/code/python/restock/8x10list.txt'
    
cat_print = '2VPZMNWFHYKEFVPM4L5EX6VW'
sizes = {'1) Print 5x7': '5x7',
        '2) Print 8x10': '8x10',
        '3) Print 11x14': '11x14'}

paper_sizes = {'5x7': 123, '8x10': 125}
                


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
            restock = {'5x7':[], '8x10':[], '11x14':[]}
            for catalog_item in catalog.body['objects']:
                item_data = catalog_item['item_data']
                try:
                    if item_data['category_id'] == category_id:
                        name = sizes[item_data['name']]
                        for item in item_data['variations']:
                            stock = self.check_item_stock(item)
                            if stock < min_stock:
                                sku = item['item_variation_data']['sku']
                                for i in range(min_stock-stock):
                                    restock[name].append(sku)
                except:
                    pass
            return restock

        elif catalog.is_error():
            print(catalog.errors)


stock = Stock()

low_stock = stock.get_low_stock(cat_print, 3)

if low_stock['8x10'] != 0:
    with open('8x10list.txt', 'w') as f:
        for item in low_stock['8x10']:
            f.write(art_path + '8x10/TIFS/' + item + '.tif\n')

if PRINT:
    os.system('2Printer -prn Canon -src "@' + list_path +'" -props papersize:125 -options alerts:no')
