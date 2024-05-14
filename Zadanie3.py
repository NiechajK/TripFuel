import sys
import json
import googlemaps
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
import polyline
import folium
import webbrowser

with open('config.json') as f:
    config = json.load(f)
api_key = config['key']
gmaps = googlemaps.Client(key=api_key)


def remove_unit(text):
    result = ''
    dot_encountered = False
    for char in text:
        if char.isdigit():
            result += char
        elif char ==',':
            print("!!!")
        elif char == '.' and not dot_encountered:
            result += char
            dot_encountered = True
        else:
            break
    return result



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Google Maps with PyQt6")

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create line edits for location input
        self.location1_edit = QLineEdit()
        self.location1_edit.setPlaceholderText("Start")
        self.location2_edit = QLineEdit()
        self.location2_edit.setPlaceholderText("Finish")
        layout.addWidget(self.location1_edit)
        layout.addWidget(self.location2_edit)

        # Create line edits for fuel consumption
        self.fuel_consumption = QLineEdit()
        self.fuel_consumption.setPlaceholderText("Your car's fuel consumption per 100km")
        layout.addWidget(self.fuel_consumption)

        # Create button to update the map
        self.update_button = QPushButton("Update Map")
        self.update_button.clicked.connect(self.update_map)
        layout.addWidget(self.update_button)

        # Create a button to switch to SecondWindow
        self.draw_button = QPushButton("Different routes")
        self.draw_button.clicked.connect(self.draw_route_on_map)
        layout.addWidget(self.draw_button)


        # Create label to display distance
        self.distance_label = QLabel()
        layout.addWidget(self.distance_label)

        # Create label to display fuel consumption
        self.consumption_label = QLabel()
        layout.addWidget(self.consumption_label)

        # Create a WebEngineView to display Google Maps
        self.map_view = QWebEngineView()
        layout.addWidget(self.map_view)

        # Load Google Maps
        self.load_map()

    def draw_route_on_map(self):
        if self.location1_edit.text() and self.location2_edit.text():
            start = self.location1_edit.text()
            finish = self.location2_edit.text()
            try:
                # Pobierz dane trasy z Google Directions API
                response = gmaps.directions(start, finish, alternatives=True)



                # Utwórz mapę folium
                map_obj = folium.Map(
                    location=[response[0]['legs'][0]['start_location']['lat'], response[0]['legs'][0]['start_location']['lng']],
                    zoom_start=7)

                # Kolory dla różnych tras
                colors = ['blue', 'green', 'red', 'purple', 'orange', 'pink', 'black', 'gray']

                # Dla każdej trasy w odpowiedzi
                for i, route in enumerate(response):



                    # Pobierz punkty polyline dla trasy
                    points = polyline.decode(route['overview_polyline']['points'])

                    # Oblicz długość trasy
                    distance_text = route['legs'][0]['distance']['value']
                    fuel_consumed = "specify consumption first"
                    if self.fuel_consumption.text():
                        fuel_consumed = float((self.fuel_consumption.text())) * float((distance_text)) / 100000

                    # Dodaj linię na mapę z etykietą długości trasy
                    folium.PolyLine(locations=points, color=colors[i], tooltip=f"Route {i + 1} ({distance_text}m) Fuel estimated: ({fuel_consumed}l)").add_to(
                        map_obj)

                    # Oznacz punkt startowy
                    folium.Marker(
                       location=[route['legs'][0]['start_location']['lat'], route['legs'][0]['start_location']['lng']],
                       popup='Start', icon=folium.Icon(color='green')).add_to(map_obj)

                    # Oznacz punkt końcowy
                    folium.Marker(location=[route['legs'][0]['end_location']['lat'], route['legs'][0]['end_location']['lng']],
                                popup='Finish', icon=folium.Icon(color='red')).add_to(map_obj)



                # Zapisz mapę do pliku HTML
                map_obj.save('map.html')

                # Otwórz plik HTML w domyślnej przeglądarce
                webbrowser.open('map.html')
            except:
                print("INVALID START/FINISH")



    def load_map(self):
        # HTML content to embed Google Maps
        self.html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Google Maps</title>
            <style>
                /* Set the size of the map to fill the window */
                html, body, #map {{
                    height: 100%;
                    width: 100%;
                    margin: 0;
                    padding: 0;
                    overflow: hidden;
                }}
            </style>
        </head>
        <body>
            <!-- Display Google Maps within an iframe -->
            <iframe id="map" frameborder="0" allowfullscreen></iframe>
        </body>
        </html>
        """

        # Load the HTML content into the map view
        self.map_view.setHtml(self.html_content)

    def update_map(self):
        if self.location1_edit.text() and self.location2_edit.text():
            location1 = self.location1_edit.text()
            location2 = self.location2_edit.text()

            distance = self.distance(location1, location2)
            self.distance_label.setText(f"Distance: {distance/1000}km")
            self.map_view.page().runJavaScript(
                f"document.getElementById('map').src = 'https://www.google.com/maps/embed/v1/directions?key={api_key}&origin={location1}&destination={location2}'",
                self.on_map_updated)
        if self.fuel_consumption.text():
            fuel_consumed =  float((self.fuel_consumption.text()))*float(distance)/100000
            print(float((self.fuel_consumption.text())))
            print(float(distance))
            self.consumption_label.setText(f"Consumption {fuel_consumed}l")

    def on_map_updated(self, result):
        if result:
            print("Map updated successfully.")
        else:
            print("Failed to update map.")

    def distance(self, start, finish):

       #Napisz tu funkcję


def main():


    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec())




if __name__ == "__main__":
    main()



