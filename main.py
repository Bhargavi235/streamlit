import sys
import re
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
#ui created
from ui import MIRDashboard


class MusicApp(MIRDashboard):   #main application class
    def __init__(self):
        super().__init__()
        self.songs = {
            "Believer": {
                "artist": "Imagine Dragons",
                "genre": "Rock",
                "mood": "Energetic",
                "duration": 3,
                "popularity": 87,
                "lyrics": "First things first I'ma say all the words inside my head..."
            },

            "Perfect": {
                "artist": "Ed Sheeran",
                "genre": "Pop",
                "mood": "Happy",
                "duration": 4,
                "popularity": 92,
                "lyrics": "I found a love for me..."
            },

            "Heat Waves": {
                "artist": "Glass Animals",
                "genre": "Rock",
                "mood": "Calm",
                "duration": 4,
                "popularity": 78,
                "lyrics": "Sometimes all I think about is you..."
            },

            "Levitating": {
                "artist": "Dua Lipa",
                "genre": "Pop",
                "mood": "Happy",
                "duration": 3,
                "popularity": 90,
                "lyrics": "If you wanna run away with me..."
            },

            "Shape Of You": {
                "artist": "Ed Sheeran",
                "genre": "Pop",
                "mood": "Energetic",
                "duration": 4,
                "popularity": 95,
                "lyrics": "The club isn't the best place to find a lover..."
            }

        }

        #signals
        
        self.playlist.currentTextChanged.connect(self.load_song) #loading song when playlist item changes
        self.analyze_button.clicked.connect(self.analyze_song) #analyzing the selected song
        self.clear_button.clicked.connect(self.clear_fields) #clearing all editable fields
        self.exit_button.clicked.connect(self.close) #exiting the application
        self.popularity.valueChanged.connect(self.progress.setValue) #updating progress bar when slider moves
        self.genre.currentTextChanged.connect(self.genre_changed) #updating genre
        self.mood.currentTextChanged.connect(self.mood_changed) #updating mood
        
        self.lyrics.textChanged.connect(self.lyrics_changed) #checking lyrics while typing
        self.duration.valueChanged.connect(self.duration_changed) #updating duration
        self.playlist.setCurrentRow(0) #selecting the first song automatically

    def load_song(self, song):  #load song details
        if song not in self.songs:
            return

        data = self.songs[song]
        self.song_name.setText(song)
        self.artist.setText(data["artist"])
        self.genre.setCurrentText(data["genre"])
        self.mood.setCurrentText(data["mood"])
        self.duration.setValue(data["duration"])
        self.popularity.setValue(data["popularity"])
        self.lyrics.setPlainText(data["lyrics"])
        
            #validate all user inputs
    def validate_input(self):

        if self.song_name.text().strip() == "":  #empty song name
            QMessageBox.warning(self, "Input Error", "Please enter the song name.")
            return False

        if self.artist.text().strip() == "": #rtist name is empty
            QMessageBox.warning(self, "Input Error", "Please enter the artist name.")
            return False

        #checking whether artist contains only letters and spaces
        if not re.fullmatch(r"[A-Za-z ]+", self.artist.text().strip()):
            QMessageBox.warning(
                self,
                "Input Error",
                "Artist name should contain only alphabets."
            )
            return False

        #checking whether genre is selected
        if self.genre.currentText() == "Select Genre":
            QMessageBox.warning(
                self,
                "Input Error",
                "Please select a genre."
            )
            return False

        #checking whether mood is selected
        if self.mood.currentText() == "Select Mood":
            QMessageBox.warning(
                self,
                "Input Error",
                "Please select a mood."
            )
            return False

        if len(self.lyrics.toPlainText().strip()) < 20:  #minimum lyrics length
            QMessageBox.warning(
                self,
                "Input Error",
                "Lyrics should contain at least 20 characters."
            )
            return False
        return True


    #analyze song
    def analyze_song(self):
        if not self.validate_input():
            return
        
        popularity = self.popularity.value() #popularity value

        if popularity >= 90:   #song category
            rating = "⭐⭐⭐⭐⭐"
            category = "Likely Viral"
        elif popularity >= 70:
            rating = "⭐⭐⭐⭐"
            category = "Trending"
        elif popularity >= 50:
            rating = "⭐⭐⭐"
            category = "Average Popularity"
        else:
            rating = "⭐⭐"
            category = "Needs Promotion"

        genre = self.genre.currentText() #getting selected genre

        if genre == "Pop": #recommending playlist based on genre
            recommendation = "Party Playlist"
        elif genre == "Rock":
            recommendation = "Workout Playlist"
        elif genre == "Hip Hop":
            recommendation = "Driving Playlist"
        elif genre == "Classical":
            recommendation = "Study Playlist"
        else:
            recommendation = "Relax Playlist"

        self.rating_label.setText(rating)
        self.classification_label.setText(category)
        self.recommend_label.setText(recommendation)  #updating the 3 labels
        
        #report
        report = f"""
Song Name : {self.song_name.text()}
Artist : {self.artist.text()}
Genre : {genre}
Mood : {self.mood.currentText()}
Duration : {self.duration.value()} min
Popularity : {popularity}/100
Recommendation : {recommendation}
Result : {category}
"""
        self.output.setText(report)
        QMessageBox.information(
            self,
            "Analysis Complete",
            "Song analysis completed successfully."
        )
        
            #clear
    def clear_fields(self):
        reply = QMessageBox.question(
            self,
            "Clear Details",
            "Do you want to clear all the fields?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            #clearing song name
            self.song_name.clear()
            #clearing artist
            self.artist.clear()
            #resetting genre
            self.genre.setCurrentIndex(0)
            #resetting mood
            self.mood.setCurrentIndex(0)
            #resetting duration
            self.duration.setValue(1)
            #resetting popularity
            self.popularity.setValue(0)
            #clearing lyrics
            self.lyrics.clear()
            #resetting analysis labels
            self.rating_label.setText("⭐⭐☆☆☆")
            self.classification_label.setText("No analysis yet")
            self.recommend_label.setText("None")
            self.output.setText("Song details cleared.")

    
    def genre_changed(self, text): #function called when genre changes
        self.output.setText(f"Genre selected : {self.genre.currentText()}")
    
    def mood_changed(self, text): #function called when mood changes
        self.output.setText(f"Mood selected : {self.mood.currentText()}")

    def lyrics_changed(self): #function called while typing lyrics

        count = len(self.lyrics.toPlainText())
        self.setWindowTitle(
            f"Music Information Retrieval Dashboard ({count} characters)"
        )

    def duration_changed(self, value): #function called when duration changes
        self.progress.setToolTip(
            f"Popularity : {self.popularity.value()}"
        )

    def keyPressEvent(self, event):
        if event.key() in (
            Qt.Key.Key_Return,
            Qt.Key.Key_Enter
        ):

            self.analyze_song()
        super().keyPressEvent(event)

    #event function while leaving the window
    def leaveEvent(self, event):

        #capitalizing the song title automatically
        self.song_name.setText(
            self.song_name.text().title()
        )

        super().leaveEvent(event)

    #event function while closing the application
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Exit",
            "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    #application object
    app = QApplication(sys.argv)
    #main window
    window = MusicApp()
    #displaying the window
    window.show()

    #run
    sys.exit(app.exec())