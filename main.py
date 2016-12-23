from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ObjectProperty

class TableColumn(Widget):
    title = StringProperty()
    hint_text = StringProperty()

    def __init__(self, title, key, weight=1, hint_text='0'):
        self.title = title
        self.key = key
        self.weight = weight
        self.hint_text = hint_text

    def get_cell(self, row):
        return TableCell(self, row)


class TableRow(BoxLayout):
    def __init__(self, table, index):
        super(TableRow, self).__init__(orientation='horizontal')
        self.table = table
        self.index = index
        for col in table.columns:
            self.add_widget(col.get_cell(self))

    def data(self, key):
        return self.table.rows[self.index][key]


class TableCell(TextInput):
    row = ObjectProperty(None, True)
    column = ObjectProperty(None, True)

    def __init__(self, column, row):
        self.column = column
        self.row = row
        super(TableCell, self).__init__(text=str(row.data(column.key)))


class TableView(ScrollView):
    def __init__(self, size, pos_hint):
        super(TableView, self).__init__(size_hint=(None, 1), size=size,
                pos_hint=pos_hint, do_scroll_x=False)

        self.layout = GridLayout(cols=1,
                size_hint=(None, None), width=size[0])
        self.layout.bind(width=self.setter('width')) # TODO test size changes
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.columns = []
        self.rows = []
        self.add_widget(self.layout)

    def add_column(self, column):
        self.columns.append(column)
        # TODO update existing rows

    def add_row(self, data):
        self.rows.append(data)
        row = TableRow(self, len(self.rows)-1)
        self.layout.add_widget(row)

class TableApp(App):
    def build(self):
        # create a default grid layout with custom width/height
        table = TableView(size=(500,320),
                pos_hint={'x':0.1, 'center_y':.5})
        # columns
        table.add_column(TableColumn("Col1", "1"))
        table.add_column(TableColumn("Col2", "2"))
        # content
        for i in range(30):
            row = {'1': str(2*i+1), '2': str(2*i+0)}
            table.add_row(row)
        return table

if __name__ == '__main__':
    TableApp().run()
