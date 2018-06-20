import kivy
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as C
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, FadeTransition, Screen
from kivy.uix.widget import Widget
import sqlite3
kivy.require('1.10.0')
__version__ = '0.1'
Config.set('graphics', 'resizable', '0')
Window.size = (288, 512)
file = 'tasks.json'
class UI(FloatLayout):
    pass
class BaseScreen(Screen):

    td_list_view = ObjectProperty()
    def update(self):
        conn = sqlite3.connect('Tasks.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT do FROM tasks')
        while True:
            row = []
            row = cursor.fetchone()
            if row == None:
                break
            for task in row:
                task = str(task)
                self.td_list_view.adapter.data.extend([task])
                self.td_list_view._trigger_reset_populate()
        cursor.close()
        conn.close()

    def task_done(self):
        if self.td_list_view.adapter.selection:
            selection = self.td_list_view.adapter.selection[0].text
            conn = sqlite3.connect('Tasks.sqlite')
            print(selection)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE do == ("%s")'%selection)
            conn.commit()
            cursor.close()
            conn.close()
            self.td_list_view.adapter.data.remove(selection)
            self.td_list_view._trigger_reset_populate()



class AddTaskScreen(Screen):
    text_input = ObjectProperty()
    bs = BaseScreen
    def add_task(self):
       # with open(file, 'w') as fileObject:
        #    fileObject.write(self.text_input.text+"\n")
        conn = sqlite3.connect('Tasks.sqlite')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (do) VALUES ("%s")'%(self.text_input.text))
        conn.commit()
        cursor.close()
        conn.close()

class ToDoListButton(ListItemButton):
    pass

Builder.load_file('main.kv')

class TodoApp(App):
    title = "To do"

    def on_start(self):
        BaseScreen.update

    def build(self):
        sm = ScreenManager()
        sm.add_widget(BaseScreen(name="base"))
        sm.add_widget(AddTaskScreen(name="task"))
        return sm

if __name__ == "__main__":
    TodoApp().run()
