# import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
import random
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from backend import *
from kivy.factory import Factory
from kivy.uix.tabbedpanel import TabbedPanel


# Builder.load_file('tripcostcalc.kv')

# kivy.require('1.9.0')


class MyRoot(BoxLayout):

    def __init__(self):
        super(MyRoot, self).__init__()
        self.test = None

    def press(self):
        self.test = PleaseWait(title="test", size_hint=(0.8, 0.8), auto_dismiss=True)
        self.test.open()

    def release(self):
        start = self.ids.start.text
        meta = self.ids.meta.text
        paliwo = self.paliwo
        consumption = self.ids.slider.value

        wynik = TripCost(start, meta, paliwo, consumption)

        info = f'Koszt przejazdu z: \n{start} \ndo: \n{meta} \nwynosi {round(wynik.trip_cost, 2)}zł. \n' \
               f'Potrwa {wynik.duration} i wyniesie {wynik.distance / 1000}km. \nKoszt {paliwo} to {wynik.price}zł/l.'
        print(info)

        layout = GridLayout(cols=1, padding=10)

        popup_label = Label(text=info, font_size=24, font_name="Arial")
        close_button = Button(text="Ok")

        layout.add_widget(popup_label)
        layout.add_widget(close_button)

        # Instantiate the modal popup and display
        popup = Popup(title='Dane przejazdu',
                      content=layout,
                      size_hint=(0.8, 0.8),
                      auto_dismiss=False)
        popup.open()

        # Attach close button press with popup.dismiss action
        close_button.bind(on_press=popup.dismiss)
        self.test.dismiss()


class PleaseWait(Popup):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout()

    def layout(self):
        self.add_widget(Label(text="Proszę czekać.."))


class TripCostCalcApp(App):

    def build(self):
        return MyRoot()


if __name__ == "__main__":
    TripCostCalc = TripCostCalcApp()
    TripCostCalc.run()
