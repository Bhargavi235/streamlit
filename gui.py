from PyQt6.QtWidgets import (
    QApplication,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
import sys
import client


class MusicGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Music Insights API")
        self.resize(900, 700)

        main_layout = QVBoxLayout()
        heading = QLabel("Music Insights")
        heading.setStyleSheet(
            "font-size:22px;"
            "font-weight:bold;"
            "padding:10px;"
        )
        main_layout.addWidget(heading)

        form_layout = QFormLayout()
        self.id_input = QLineEdit()
        form_layout.addRow("Song ID", self.id_input)

        self.track_input = QLineEdit()
        form_layout.addRow("Track Name", self.track_input)

        self.artist_input = QLineEdit()
        form_layout.addRow("Artist", self.artist_input)

        self.genre_input = QLineEdit()
        form_layout.addRow("Genre", self.genre_input)

        self.danceability_input = QLineEdit()
        form_layout.addRow("Danceability", self.danceability_input)

        self.energy_input = QLineEdit()
        form_layout.addRow("Energy", self.energy_input)

        self.acousticness_input = QLineEdit()
        form_layout.addRow("Acousticness", self.acousticness_input)

        self.tempo_input = QLineEdit()
        form_layout.addRow("Tempo", self.tempo_input)

        self.valence_input = QLineEdit()
        form_layout.addRow("Valence", self.valence_input)

        self.popularity_input = QLineEdit()
        form_layout.addRow("Popularity", self.popularity_input)

        main_layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.get_button = QPushButton("Get Songs")
        self.add_button = QPushButton("Add Song")
        self.update_button = QPushButton("Update Song")
        self.delete_button = QPushButton("Delete Song")

        button_layout.addWidget(self.get_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)

        main_layout.addLayout(button_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Track",
            "Artist",
            "Genre",
            "Popularity",
        ])
        main_layout.addWidget(self.table)

        self.get_button.clicked.connect(self.load_all_songs)
        self.add_button.clicked.connect(self.add_song)
        self.update_button.clicked.connect(self.update_song)
        self.delete_button.clicked.connect(self.delete_song)
        self.table.cellClicked.connect(self.load_selected_song)

        self.setLayout(main_layout)

    def clear_inputs(self):
        self.id_input.clear()
        self.track_input.clear()
        self.artist_input.clear()
        self.genre_input.clear()
        self.danceability_input.clear()
        self.energy_input.clear()
        self.acousticness_input.clear()
        self.tempo_input.clear()
        self.valence_input.clear()
        self.popularity_input.clear()

    def load_selected_song(self, row, column):
        song_id = int(self.table.item(row, 0).text())
        song = client.get_song(song_id)

        if song is None:
            QMessageBox.warning(self, "Error", "Unable to retrieve song.")
            return

        self.id_input.setText(str(song["id"]))
        self.track_input.setText(song["track_name"])
        self.artist_input.setText(song["artist"])
        self.genre_input.setText(song["genre"])
        self.danceability_input.setText(str(song["danceability"]))
        self.energy_input.setText(str(song["energy"]))
        self.acousticness_input.setText(str(song["acousticness"]))
        self.tempo_input.setText(str(song["tempo"]))
        self.valence_input.setText(str(song["valence"]))
        self.popularity_input.setText(str(song["popularity"]))

    def load_all_songs(self):
        songs = client.get_all_songs()

        if songs is None:
            QMessageBox.warning(self, "Error", "Unable to retrieve songs.")
            return

        self.table.setRowCount(0)
        self.table.setRowCount(len(songs))
        for row, song in enumerate(songs):
            self.table.setItem(row, 0, QTableWidgetItem(str(song["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(song["track_name"]))
            self.table.setItem(row, 2, QTableWidgetItem(song["artist"]))
            self.table.setItem(row, 3, QTableWidgetItem(song["genre"]))
            self.table.setItem(row, 4, QTableWidgetItem(str(song["popularity"])))

    def add_song(self):
        if self.track_input.text().strip() == "":
            QMessageBox.warning(self, "Input Error", "Track Name cannot be empty.")
            return

        try:
            song_data = {
                "track_name": self.track_input.text(),
                "artist": self.artist_input.text(),
                "genre": self.genre_input.text(),
                "danceability": float(self.danceability_input.text()),
                "energy": float(self.energy_input.text()),
                "acousticness": float(self.acousticness_input.text()),
                "tempo": int(self.tempo_input.text()),
                "valence": float(self.valence_input.text()),
                "popularity": int(self.popularity_input.text()),
            }
        except ValueError:
            QMessageBox.warning(
                self,
                "Input Error",
                "Please enter valid numeric values.",
            )
            return

        response = client.add_song(song_data)

        if response:
            QMessageBox.information(self, "Success", "Song added successfully.")
            self.load_all_songs()
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Error", "Unable to add song.")

    def update_song(self):
        if self.id_input.text().strip() == "":
            QMessageBox.warning(self, "Error", "Select a song first.")
            return

        try:
            song_id = int(self.id_input.text())
            updated_data = {
                "track_name": self.track_input.text(),
                "artist": self.artist_input.text(),
                "genre": self.genre_input.text(),
                "danceability": float(self.danceability_input.text()),
                "energy": float(self.energy_input.text()),
                "acousticness": float(self.acousticness_input.text()),
                "tempo": int(self.tempo_input.text()),
                "valence": float(self.valence_input.text()),
                "popularity": int(self.popularity_input.text()),
            }
        except ValueError:
            QMessageBox.warning(
                self,
                "Input Error",
                "Please enter valid numeric values.",
            )
            return

        response = client.update_song(song_id, updated_data)

        if response:
            QMessageBox.information(self, "Success", "Song updated successfully.")
            self.load_all_songs()
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Error", "Update failed.")

    def delete_song(self):
        if self.id_input.text().strip() == "":
            QMessageBox.warning(self, "Error", "Please select a song first.")
            return

        song_id = int(self.id_input.text())
        reply = QMessageBox.question(
            self,
            "Delete Song",
            "Are you sure you want to delete this song?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.No:
            return

        success = client.delete_song(song_id)

        if success:
            QMessageBox.information(self, "Success", "Song deleted successfully.")
            self.load_all_songs()
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Error", "Unable to delete song.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicGUI()
    window.show()
    sys.exit(app.exec())
