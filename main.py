# import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import PopupException
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from backend import *


# kivy.require('1.9.0')


class MyRoot(BoxLayout):

    def __init__(self):
        super(MyRoot, self).__init__()
        self.please_wait = None
        self.fuel_price = None
        self.paliwo = 'fuel'

    def press(self):
        self.please_wait = PleaseWait(title="Please wait", size_hint=(0.8, 0.8), auto_dismiss=False)
        self.please_wait.open()

    def release(self):
        start = self.ids.start.text
        meta = self.ids.meta.text
        consumption = self.ids.slider.value
        if self.fuel_price == 'fuel':
            self.paliwo = self.paliwo
        elif self.fuel_price == 'price':
            self.paliwo = self.ids.price_slider.value

        if start == "" or meta == "":
            return self.please_wait.dismiss(), Factory.ErrorPopup(content=Label(text="pusto")).open()

        try:
            wynik = TripCost(start, meta, self.paliwo, consumption)

            info = f'Koszt przejazdu z: \n{start} \ndo: \n{meta} \nwynosi {round(wynik.trip_cost, 2)}zł. \n' \
                   f'Potrwa {wynik.duration} i wyniesie {wynik.distance / 1000}km. \n' \
                   f'Koszt {self.paliwo if type(self.paliwo) == str else "paliwa"} to {wynik.price}zł/l.'
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
            self.please_wait.dismiss()
        except KeyError:
            self.please_wait.dismiss()
            # Popup layout
            layout = GridLayout(cols=1, padding=10)
            popup_label = Label(text="Wybierz rodzaj paliwa lub cenę!", font_size=24, font_name="Arial")
            close_button = Button(text="Ok")
            layout.add_widget(popup_label)
            layout.add_widget(close_button)
            # Call Popup
            error = Factory.ErrorPopup(content=layout)
            error.open()
            close_button.bind(on_press=error.dismiss)

    def select_price(self):
        paliwa = self.ids.paliwa
        paliwa.height, paliwa.size_hint_y, paliwa.opacity, paliwa.disabled = 0, None, 0, True
        price_label = self.ids.price_label
        price_label.height, price_label.size_hint_y, price_label.opacity, price_label.disabled = 15, 0.5, 1, False
        price_slider = self.ids.price_slider
        price_slider.height, price_slider.size_hint_y, price_slider.opacity, price_slider.disabled = 1, 0.5, 1, False

    def select_fuel(self):
        paliwa = self.ids.paliwa
        paliwa.height, paliwa.size_hint_y, paliwa.opacity, paliwa.disabled = 1, 1, 1, False
        price_label = self.ids.price_label
        price_label.height, price_label.size_hint_y, price_label.opacity, price_label.disabled = 0, None, 0, True
        price_slider = self.ids.price_slider
        price_slider.height, price_slider.size_hint_y, price_slider.opacity, price_slider.disabled = 0, None, 0, True


class PleaseWait(Popup):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout()

    def layout(self):
        self.add_widget(Label(text="Proszę czekać.."))


# class ErrorPopup(Popup):
#
#     error_msg = 'test'
#
#     def __init__(self, **kwargs):
#         super().__init__()
#         # self.layout()
#
#     def layout(self):
#         pass
        # layout = GridLayout(cols=1, padding=10)
        #
        # popup_label = Label(text='Wybierz rodzaj lub cenę paliwa!', font_size=24, font_name="Arial")
        # # close_button = Button(text="Ok", on_release=self.dismiss())
        #
        # layout.add_widget(popup_label)
        # # layout.add_widget(close_button)

        # self.add_widget(Label(text='paliwo'))


class TripCostCalcApp(App):

    def build(self):
        return MyRoot()


if __name__ == "__main__":
    TripCostCalc = TripCostCalcApp()
    TripCostCalc.run()
