# TO DO
# wybieranie typu pojazdu
# aplikacja okienkowa
from PyQt6.QtWidgets import *
import sys
import googlemaps
import json

## importowanie klucza z config.json
with open('config.json') as f:
    config = json.load(f)
akey = config['key']

gmaps = googlemaps.Client(key=akey)


point1 = "ORLEN Paczka Automat Paczkowy, przy chodniku, Podedworze 10, 30-686 Kraków"
point2 = "Podedworze 9, 30-686 Kraków"
user_input = ['','']

#avarage fuel consumption per 1 km
AFC_hatchback = 0.07
AFC_fiatDucato = 0.08
AFC_suv = 0.1
AFC_deliveryTruck = 0.2
AFC_tir = 0.3

#fuel_consumption = input("Your fuel consumption in city")
#point1 = input()+' Kraków'
#point2 = input()+' Kraków'

# Request directions via driving
def distance(start, finnish):
    return gmaps.distance_matrix(start,
                                    finnish,
                                    mode = "walking")['rows'][0]['elements'][0]['distance']['text']



## WINDOWED APPLICATION
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QHBoxLayout Example")
        # Create a QHBoxLayout instance
        layout = QVBoxLayout()

            #INPUT 1
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Start")
        #input1.setReadOnly(True) # uncomment this to make readonly
        layout.addWidget(self.input1)

            #INPUT 2
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("Finish")
        # input2.setReadOnly(True) # uncomment this to make readonly

            #CAR TYPES LIST WEZ TO KURWA ZMIEN NA WPISYWANIE WLASNEJ WARTOSCI BO TOP 2 KIEROWCOW TAK POWEIDZALO
        #typeList = QListWidget
        #typeList.addItems(['Skoda Octavia','Fiat Ducato','SUV','Delivery Truck','TIR'])

            #BUTTON_SEND
        button_send = QPushButton("Send", self)
        button_send.clicked.connect(self.retrieveText)



            #LAYOUT.ADD
        layout.addWidget(self.input1)
        layout.addWidget(self.input2)
        #layout.addWidget(typeList)
        layout.addWidget(button_send)

        # Set the layout on the application's window
        self.setLayout(layout)
        print(self.children())

    def retrieveText(self):
        print(distance(str(self.input1.text()),str(self.input2.text())))

    def retrieveText2(self):
        return (str(self.input1.text()),str(self.input2.text()))


app = QApplication(sys.argv)



window = Window()
window.show()
sys.exit(app.exec())
