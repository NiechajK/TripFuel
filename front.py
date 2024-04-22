import sys
import json
from PyQt6.QtCore import QSize, Qt, QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView

with open('config.json') as f:
    config = json.load(f)
api_key = config['key']

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
        self.location2_edit = QLineEdit()
        layout.addWidget(self.location1_edit)
        layout.addWidget(self.location2_edit)

        # Create button to update the map
        self.update_button = QPushButton("Update Map")
        self.update_button.clicked.connect(self.update_map)
        layout.addWidget(self.update_button)

        # Create a WebEngineView to display Google Maps
        self.map_view = QWebEngineView()
        layout.addWidget(self.map_view)

        # Load Google Maps
        self.load_map()

    def load_map(self):

        # Replace YOUR_GOOGLE_MAPS_API_KEY with your actual API key

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
        location1 = self.location1_edit.text()
        location2 = self.location2_edit.text()
        self.map_view.page().runJavaScript(
            f"document.getElementById('map').src = 'https://www.google.com/maps/embed/v1/directions?key={api_key}&origin={location1}&destination={location2}'",
            self.on_map_updated)

    def on_map_updated(self, result):
        if result:
            print("Map updated successfully.")
        else:
            print("Failed to update map.")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
