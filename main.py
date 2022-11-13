import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from backend import *
from kivy.factory import Factory


class MyRoot(BoxLayout):

    def __init__(self):
        super(MyRoot, self).__init__()
        self.please_wait = None
        self.fuel_price = None
        self.paliwo = 'fuel'
        self.info = None

    def press(self):
        # Open temporary window while waiting for the result
        self.please_wait = PleaseWait(title="Please wait", size_hint=(0.8, 0.8), auto_dismiss=False)
        self.please_wait.open()

    def release(self):
        # Open result window with all parameters
        start = self.ids.start.text
        meta = self.ids.meta.text
        consumption = self.ids.slider.value

        # Check which tab is selected: select type of fuel or set fuel price
        if self.fuel_price == 'fuel':
            # if selected type of fuel set selected
            self.paliwo = self.paliwo
        elif self.fuel_price == 'price':
            # if selected fuel price get slider value
            self.paliwo = self.ids.price_slider.value

        # Error window if not filled required fields
        if start == "":
            return self.please_wait.dismiss(), self.layout("Podaj adres początkowy").open()
        elif meta == "":
            return self.please_wait.dismiss(), self.layout("Podaj cel podróży").open()
        elif self.paliwo == "fuel":
            return self.please_wait.dismiss(), self.layout("Wybierz rodzaj paliwa, lub ustaw cenę").open()

        try:
            wynik = TripCost(start, meta, self.paliwo, consumption)

            self.info = f'Koszt przejazdu z: \n{start} \ndo: \n{meta} \nwynosi {round(wynik.trip_cost, 2)}zł. \n' \
                        f'Potrwa {wynik.duration_text} i wyniesie {wynik.distance_value / 1000}km. \n' \
                        f'Koszt {self.paliwo if type(self.paliwo) == str else "paliwa"} to {wynik.price}zł/l.'

            result = Factory.Result()

            result.ids['a'].text = start.capitalize()
            result.ids['b'].text = meta.capitalize()
            result.ids['c'].text = str(round(wynik.trip_cost, 2)) + "zł"
            result.ids['d'].text = wynik.duration_text.replace('hours', 'godz.').replace('mins', 'min.')
            result.ids['e'].text = str(wynik.distance_value / 1000) + "km"
            result.ids['f'].text = str(wynik.price) + "zł/l"
            result.ids['g'].text = wynik.weather_description[0]
            result.ids['h'].text = 'widoczność: ' + str(wynik.weather_description[1]) + 'm'

            result.open()
            self.please_wait.dismiss()
            os.remove('map.jpg')
        except KeyError:
            self.please_wait.dismiss()
            self.layout("Sprawdź, czy adresy,\nktóre podałeś są prawidłowe.\nNie mogę znaleźć takiej trasy").open()

    def select_price(self):
        # Change the view to set fuel price by slider
        paliwa = self.ids.paliwa
        paliwa.height, paliwa.size_hint_y, paliwa.opacity, paliwa.disabled = 0, None, 0, True
        price_label = self.ids.price_label
        price_label.height, price_label.size_hint_y, price_label.opacity, price_label.disabled = 15, 0.5, 1, False
        price_slider = self.ids.price_slider
        price_slider.height, price_slider.size_hint_y, price_slider.opacity, price_slider.disabled = 1, 0.5, 1, False

    def select_fuel(self):
        # Change view to select type of fuel
        paliwa = self.ids.paliwa
        paliwa.height, paliwa.size_hint_y, paliwa.opacity, paliwa.disabled = 1, 1, 1, False
        price_label = self.ids.price_label
        price_label.height, price_label.size_hint_y, price_label.opacity, price_label.disabled = 0, None, 0, True
        price_slider = self.ids.price_slider
        price_slider.height, price_slider.size_hint_y, price_slider.opacity, price_slider.disabled = 0, None, 0, True

    def layout(self, text: str):
        # Create the error popup with adequate message
        layout = GridLayout(cols=1, padding=10)
        popup_label = Label(text=text, font_size=24, font_name="Arial")
        close_button = Button(text="Ok")
        layout.add_widget(popup_label)
        layout.add_widget(close_button)
        error_popup = Factory.ErrorPopup(content=layout)
        close_button.bind(on_press=error_popup.dismiss)
        return error_popup


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
