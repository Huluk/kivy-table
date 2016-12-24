import sys
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ObjectProperty

class TableColumn(Widget):
    title = StringProperty()
    hint_text = StringProperty()

    # TODO different widths
    def __init__(self, title, key,
            update_function=(lambda row, new_value: None),
            hint_text=''):
        self.title = title
        self.key = key
        self.update_function = update_function
        self.hint_text = hint_text

    def get_cell(self, row):
        return TableCell(self, row)

    def on_cell_edit(self, row, new_value):
        self.update_function(row, new_value)


class TableRow(BoxLayout):
    def __init__(self, table, index):
        super(TableRow, self).__init__(orientation='horizontal')
        self.table = table
        self.index = index
        for col in table.columns:
            self.add_widget(col.get_cell(self))

    def data(self, key):
        return self.table.data_rows[self.index][key]

    def set_data(self, key, value):
        self.data_rows[self.index][key] = value

    def update(self):
        for cell in self.children:
            cell.update()

    def move_focus(self, index_diff, column):
        self.table.set_focus(self.index + index_diff, column)

    def focus_on_cell(self, column):
        for cell in self.children:
            if cell.column == column:
                cell.focus = True
                break

    def scroll_into_view(self):
        self.table.scroll_to(self)


class TableCell(TextInput):
    row = ObjectProperty(None, True)
    column = ObjectProperty(None, True)

    MOVEMENT_KEYS = {'up': -1, 'down': 1,
            'pageup': -sys.maxsize, 'pagedown': sys.maxsize }

    def __init__(self, column, row):
        self.column = column
        self.row = row
        super(TableCell, self).__init__()
        self.update()
    
    def update(self):
        self.text = str(self.row.data(self.column.key))

    def on_text_validate(self):
        self.column.on_cell_edit(self.row, self.text)

    def on_focus(self, instance, value, *largs):
        if value:
            self.row.scroll_into_view()
        else:
            self.update()

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] in self.MOVEMENT_KEYS:
            self.on_text_validate()
            self.focus = False
            self.row.move_focus(self.MOVEMENT_KEYS[keycode[1]], self.column)
        else:
            super(TableCell, self).keyboard_on_key_down(window, keycode, text, modifiers)


class TableView(ScrollView):
    # TODO overscroll background color
    def __init__(self, size, pos_hint):
        super(TableView, self).__init__(size_hint=(None, 1), size=size,
                pos_hint=pos_hint, do_scroll_x=False)

        self.layout = GridLayout(cols=1,
                size_hint=(None, None), width=size[0])
        self.layout.bind(width=self.setter('width')) # TODO test size changes
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.columns = []
        self.data_rows = []
        self.layout_rows = []
        self.add_widget(self.layout)

    def add_column(self, column):
        self.columns.append(column)
        # TODO test row update
        for row in self.layout_rows:
            # TODO update column widths
            row.add_widget(column.get_cell(row))

    def add_row(self, data):
        self.data_rows.append(data)
        row = TableRow(self, len(self.data_rows)-1)
        self.layout_rows.append(row)
        self.layout.add_widget(row)

    def set_focus(self, row_index, column):
        if len(self.layout_rows) == 0:
            return
        row_index = min(max(row_index, 0), len(self.layout_rows)-1)
        self.layout_rows[row_index].focus_on_cell(column)
