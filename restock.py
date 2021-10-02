import os
from tkinter import Tk, Button 
from tkinter.ttk import Treeview 
from square.client import Client

PRINT = False 

art_path  = 'C:\\Users\\Scott\\Desktop\\Art\\Prints\\'
list_path = 'C:\\Users\\Scott\\Desktop\\Scotts_Stuff\\code\\python\\restock\\8x10list.txt'
    
cat_print = '2VPZMNWFHYKEFVPM4L5EX6VW'
sizes = {'1) Print 5x7': '5x7',
        '2) Print 8x10': '8x10',
        '3) Print 11x14': '11x14'}

paper_sizes = {'5x7': 123, '8x10': 125}


class App:
    def __init__(self, master):
        self.master = master

        # configure the root window
        master.title("Restock App")
        master.geometry('605x500')
        
        # create the "Get Stock" button
        self.stock_button = Button(master, text='Get Stock', width=1)
        self.stock_button['command'] = self.stock_button_callback
        self.stock_button.grid(row=0, column=0, sticky='nsew')

        # create the "Print" button
        self.print_button = Button(master, text='Print', width=1)
        self.print_button['command'] = self.print_button_callback
        self.print_button.grid(row=0, column=2, sticky='nsew')

        # table
        columns = ('#1', '#2', '#3')

        self.tree = Treeview(master, columns=columns, show='headings', height=30)

        self.tree.heading('#1', text='Name')
        self.tree.heading('#2', text='SKU')
        self.tree.heading('#3', text='Stock')

        inventory = []
        for n in range(1, 20):
            inventory.append((f'Name {n}', f'SKU {n}', f'Stock {n}'))

        self.tree.grid(row=1, column=0, columnspan = 3, sticky='nsew')


    def stock_button_callback(self):
        stock = Stock()
        inventory = stock.get_inventory(cat_print)
        self.load_table(inventory)


    def print_button_callback(self):
        pass


    def load_table(self, inventory):
        for item in inventory:
            self.tree.insert('', 'end', values=item)


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


    def get_inventory(self, category_id):
        inventory = []
        catalog = self.client.catalog.list_catalog(types='ITEM')

        if catalog.is_success():
            restock = {'5x7':[], '8x10':[], '11x14':[]}
            for catalog_item in catalog.body['objects']:
                item_data = catalog_item['item_data']
                try:
                    if item_data['category_id'] == category_id:
                        size = sizes[item_data['name']]
                        for item in item_data['variations']:
                            stock     = self.check_item_stock(item)
                            sku       = item['item_variation_data']['sku']
                            item_name = item['item_variation_data']['name']
                            inventory.append((item_name, sku, stock))
                except:
                    pass
            return inventory 

        elif catalog.is_error():
            print(catalog.errors)

#stock = Stock()

#low_stock = stock.get_low_stock(cat_print, 3)

#if low_stock['8x10'] != 0:
#    with open('8x10list.txt', 'w') as f:
#        for item in low_stock['8x10']:
#            f.write(art_path + '8x10/TIFS/' + item + '.tif\n')
#
#if PRINT:
#    os.system('2Printer -prn Canon -src "@' + list_path +'" -props papersize:125 -options alerts:no')
#
#os.remove(list_path)

#top.mainloop()

if __name__ == '__main__':
    #window = ThemedTk(theme='black')
    root = Tk()
    app = App(root)

    #ttk.Button(window, text='Quit', command=window.destroy).pack()
    root.mainloop()
    #app = App()
    #app.mainloop()
