import sys
import json
import requests

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class MusicAPI(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Music Information Retrieval")
        self.resize(600, 450)
        
        self.setStyleSheet("""
            QWidget{background:#1E1E1E; color:white;font-size:13px;
            }
            QLineEdit,QTextEdit{ background:#2E2E2E; color:white; border:1px solid gray;border-radius:5px;padding:5px;
            }
            QPushButton{ background:#1DB954; color:black; font-weight:bold; border-radius:5px;padding:6px;
            }
            QPushButton:hover{background:#1ED760;
            }
        """)
        
        heading = QLabel("Music Information Retrieval")
        heading.setStyleSheet(
            "font-size:20px;font-weight:bold;color:#1DB954;"
        )
        search_label = QLabel("Enter Song Name")
        self.song_input = QLineEdit()
        # self.song_input.setPlaceholderText("Example : Believer")
        self.search_button = QPushButton("Search Song")
        result_label = QLabel("Search Result")
        self.output = QTextEdit()
        self.output.setReadOnly(True)   #make output read only
        layout = QVBoxLayout()   #main layout
        layout.addWidget(heading)
        layout.addWidget(search_label)
        layout.addWidget(self.song_input)
        layout.addWidget(self.search_button)
        layout.addWidget(result_label)
        layout.addWidget(self.output)
        
        self.setLayout(layout)  #set layout
        
        self.search_button.clicked.connect(self.search_song)
        
    def search_song(self):
        song = self.song_input.text().strip()

        if song == "":

            QMessageBox.warning(
                self,
                "Input Error",  #if text box is empty
                "Please enter a song name."
            )

            return

        # creating api url
        url = f"https://itunes.apple.com/search?term={song}"   #itunes api

        try:
            
            response = requests.get(url)   #send request to api
            data = response.json()  #convert response to json
            with open("song_data.json", "w") as file:  #save json as local file
                json.dump(data, file, indent=4)

            with open("song_data.json", "r") as file:  #open json
                song_data = json.load(file)

            if song_data.get("resultCount") == 0:
                QMessageBox.information(
                    self,   #if song not founf
                    "Song Not Found",
                    "No matching song was found."
                )
                self.output.clear()
                return

            result = song_data.get("results")[0]   #first result from the api

            track = result.get("trackName", "Not Available")
            artist = result.get("artistName", "Not Available")
            album = result.get("collectionName", "Not Available")
            genre = result.get("primaryGenreName", "Not Available")
            price = result.get("trackPrice", "Not Available")
            release = result.get("releaseDate", "Not Available")   #dictionary's get function to get meaningful info from response
            preview = result.get("previewUrl", "Not Available")

            keys = result.keys()   #dictio keys
            values = result.values()  #dictio values
            items = result.items()  #dictio items

            total_keys = len(result)   #rotal number of keys
            
            output_text = f"""
Music Information Retrieval Result

Song Name      : {track}

Artist         : {artist}

Album          : {album}

Genre          : {genre}

Track Price    : {price}

Release Date   : {release[:10]}

Preview URL

{preview}


Dictionary Functions Used

Total Keys : {total_keys}

First 10 Keys

{list(keys)[:10]}


First 5 Key - Value Pairs

"""

            # adding the first 5 dictionary items
            for key, value in list(items)[:5]:

                # appending every key-value pair
                output_text += f"{key} : {value}\n"

            self.output.setPlainText(output_text)
            QMessageBox.information(
                self,
                "Success",
                "Song information fetched and JSON processed successfully."
            )

        # handling network errors
        except requests.exceptions.RequestException:

            QMessageBox.critical(
                self,
                "Connection Error",
                "Unable to connect to the API."
            )

        # handling json errors
        except json.JSONDecodeError:

            QMessageBox.critical(
                self,
                "JSON Error",
                "Unable to read the JSON file."
            )

        # handling any other errors
        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )

if __name__ == "__main__":

    app = QApplication(sys.argv)   #object
    window = MusicAPI() #window
    window.show()
    sys.exit(app.exec())