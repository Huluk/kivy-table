from kivy.app import App

from table import TableView, TableColumn

class TableApp(App):
    def build(self):
        # create a default grid layout with custom width/height
        table = TableView(size=(500,320),
                pos_hint={'x':0.1, 'center_y':.5})
        # columns
        table.add_column(TableColumn("Col1", key="1", hint_text='0'))
        table.add_column(TableColumn("Col2", key="2", hint_text='0'))
        # content
        for i in range(30):
            row = {'1': str(2*i+1), '2': str(2*i+0)}
            table.add_row(row)
        return table

if __name__ == '__main__':
    TableApp().run()
