from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ObjectProperty, ListProperty

class Column(Widget):
    title = StringProperty()
    key = StringProperty()
    hint_text = StringProperty()

    def __init__(self, title, key, weight=1, hint_text='0'):
        self.title = title
        self.key = key
        self.weight = weight
        self.hint_text = hint_text

    def get_cell(self, row):
        return TableCell(self, row)


class Row(BoxLayout):
    def __init__(self, data, columns):
        super(Row, self).__init__(orientation='horizontal')
        self.data = data
        for col in columns:
            self.add_widget(col.get_cell(self))


class TableCell(TextInput):
    row = ObjectProperty(None, True)
    column = ObjectProperty(None, True)

    def __init__(self, column, row):
        self.row = row
        self.column = column
        super(TableCell, self).__init__(text=str(row.data[column.key]))


class TableView(ScrollView):
    def __init__(self, size, pos_hint):
        super(TableView, self).__init__(size_hint=(None, 1), size=size,
                pos_hint=pos_hint, do_scroll_x=False)

        self.layout = GridLayout(cols=1,
                size_hint=(None, None), width=size[0])
        self.layout.bind(width=self.setter('width')) # TODO test size changes
        self.layout.bind(minimum_height=self.layout.setter('height'))
        # content
        column = Column("Column", "1")
        column2 = Column("Column", "2")
        for i in range(30):
            row = {'1': str(2*i+1), '2': str(2*i+0)}
            row = Row(row, [column, column2])
            self.layout.add_widget(row)
        self.add_widget(self.layout)

class TableApp(App):
    def build(self):
        # create a default grid layout with custom width/height
        return TableView(size=(500,320),
                pos_hint={'x':0.1, 'center_y':.5})

if __name__ == '__main__':
    TableApp().run()
