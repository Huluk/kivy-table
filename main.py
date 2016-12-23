from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class TableView(ScrollView):
    # TODO how to do named args
    def __init__(self, size, pos_hint): # TODO pass row layout
        super(TableView, self).__init__(size_hint=(None, 1), size=size,
                pos_hint=pos_hint, do_scroll_x=False)

        layout = GridLayout(cols=1,
                size_hint=(None, None), width=size[0])

        # when we add children to the grid layout, its size doesn't change at
        # all. we need to ensure that the height will be the minimum required to
        # contain all the childs. (otherwise, we'll child outside the bounding
        # box of the childs)
        layout.bind(minimum_height=layout.setter('height'))
        # content
        for i in range(30):
            box = BoxLayout(orientation='horizontal')
            layout.add_widget(box)
            label = Label(text=str(2*i))
            box.add_widget(label)
            label = TextInput(text=str(2*i+1))
            box.add_widget(label)
        self.add_widget(layout)

class TableApp(App):
    def build(self):
        # create a default grid layout with custom width/height
        return TableView(size=(500,320),
                pos_hint={'x':0.1, 'center_y':.5})

if __name__ == '__main__':
    TableApp().run()
