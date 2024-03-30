# TO DO
# wybieranie typu pojazdu
# aplikacja okienkowa

import googlemaps
import pandas as pd
import json

## importowanie klucza z config.json
with open('config.json') as f:
    config = json.load(f)
akey = config['key']

gmaps = googlemaps.Client(key=akey)



point1 = "ORLEN Paczka Automat Paczkowy, przy chodniku, Podedworze 10, 30-686 Kraków"
point2 = "Podedworze 9, 30-686 Kraków"

#fuel_consumption = input("Your fuel consumption in city")
#point1 = input()+' Kraków'
#point2 = input()+' Kraków'

# Request directions via driving
def distance(point1, point2):
    return gmaps.distance_matrix(point1,
                                    point2,
                                    mode = "driving")['rows'][0]['elements'][0]['distance']['text']

def MPGtoKMPL(milesPerGalon):
    return milesPerGalon*0.425143707

df = pd.read_excel('DataBase/2024.xlsx')
print(df)

print(distance(point1,point2))

