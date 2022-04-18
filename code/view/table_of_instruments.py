
import tkinter as tk

class Table_Of_Instuments:
    def __init__(self, gui_frame):
        frame = tk.Frame(gui_frame, padx=5, pady=5)
        frame.pack(side=tk.LEFT)
        #scrollbar
        game_scroll = tk.Scrollbar(frame)
        game_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ('country', 'leverage')

        self.table = tk.ttk.Treeview(frame,
                                            yscrollcommand=game_scroll.set,
                                            columns=columns,
                                            selectmode="extended")
        self.table.heading('#0', text='Text')
        self.table.heading('country', text='Country')
        self.table.heading('leverage', text='Leverage')
        self.table.pack()
        self.table.bind('<<TreeviewSelect>>',gui_frame.update_table_item_focused)


        # Define the row colors with a tag
        self.table.tag_configure("selected_row", background="green")
        self.table.tag_configure("not_selected_row", background="white")

        self.rows_unfolded = []


    def set_table(self, names, countries):
        print("TRACE: table_of_instruments: set_table")

        all_item_values = self.get_all_item_values()
        all_item_texts = self.get_all_item_texts()

        added_new_item = False

        for market_name, country in zip(names, countries):
            #only add if market not in table
            if market_name not in all_item_texts:

                added_new_item = True

                self.table.insert(parent='', index=tk.END, iid=market_name, text=market_name, values=(country,1))
                for i in range(2,4): #leverage span
                    self.table.insert(parent=market_name, index=tk.END, text=market_name, values=(country,i))

        if added_new_item:
            self.update_unfolding_status()


    def get_table_item_focused(self):
        print("TRACE: table_of_instruments: get_table_item_focused")
        curItem = self.table.focus()
        item = self.table.item(curItem)

        return [item['text'], item['values'][1]] #market index and leverage


    def update_item_color(self):
        print("TRACE: table_of_instruments: update_item_color")

        curItem = self.table.focus()
        current_item_tag = self.table.item(curItem)["tags"]

        if current_item_tag != ['selected_row']:
            self.table.item(curItem, tag="selected_row")
        else:
            self.table.item(curItem, tag="not_selected_row")


    def get_all_item_texts(self):
        print("TRACE: table_of_instruments: get_all_item_texts")

        all_item_texts = []

        for item in self.table.get_children():
            item_text = self.table.item(item)['text']
            all_item_texts.append(item_text)

        return all_item_texts


    def get_all_item_values(self):
        print("TRACE: table_of_instruments: get_all_item_values")

        all_item_values = []

        for item in self.table.get_children():
            item_value = self.table.item(item)['values']
            all_item_values.append(item_value[0]) # TODO update when adding bull > 1

        return all_item_values


    def update_unfolding_status(self):
        print("TRACE: View: update_unfolding_status")

        rows_folding_status = []
        for item in self.table.get_children():
            item =  self.table.item(item)['open']

            rows_folding_status.append(item)
        self.rows_unfolded = rows_folding_status


    def only_did_unfolding(self):
        rows_folding_status = []
        for item in self.table.get_children():
            item =  self.table.item(item)['open']

            rows_folding_status.append(item)


        if rows_folding_status == self.rows_unfolded:
            # Folding sattus unchanged, action was no unfolding
            self.rows_unfolded = rows_folding_status
            return False
        else:
            # Folding sattus changed, action was an unfolding
            self.rows_unfolded = rows_folding_status
            return True

