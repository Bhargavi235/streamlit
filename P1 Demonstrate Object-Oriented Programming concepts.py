from abc import ABC, abstractmethod

class InvalidSongDataError(Exception):    #custom exception
    pass


class MusicContent(ABC):     #abstract base class
    
    def __init__(self, title: str, artist: str):
        if not title.strip() or not artist.strip():
            raise InvalidSongDataError("Title and Artist fields cannot be empty.")
        
        self.title = title.strip()
        self.artist = artist.strip()
    
    @abstractmethod
    def analyze(self):     #abstract method
        pass

class LyricsAnalyzer(MusicContent):     #first derived class 
    
    def __init__(self, title, artist, lyrics=""):
        super().__init__(title, artist)
        self.lyrics = lyrics.strip()

    def analyze(self):    #overidden function in first derived class
        if self.lyrics:
            return f"'{self.title}' by {self.artist}: Analyzing provided lyrics -> '{self.lyrics[:20]}...' -> Emotional depth detected."
        return f"'{self.title}' by {self.artist}: No lyrics provided to analyze -> Basic thematic analysis applied."


class AudioFeatureAnalyzer(MusicContent): #second derived class
    
    def analyze(self):   #overideen function in second derived class
        return f"'{self.title}' by {self.artist}: Scanning frequencies -> High energy, rhythmic synth-patterns, and danceable."


class PopularityPredictor(MusicContent):  #third derived class
  
    def analyze(self):      #overidden function in third derived class
        return f"'{self.title}' by {self.artist}: Checking streaming trends -> Strong hit potential on global charts."


if __name__ == "__main__":
    print("Music Information Retrieval")
 
    song1 = LyricsAnalyzer("Midnight Dreams", "Aurora Wave", "In the shadows of the night...")     #existing songs
    song2 = AudioFeatureAnalyzer("Electric Pulse", "Neon Beats")
    song3 = PopularityPredictor("Sunset Boulevard", "The Wanderers")
    
    analyzers = [song1, song2, song3]     #passing objects as a list

    while True:
        print("1. View existing songs")
        print("2. Analysis of songs")
        print("3.  Add your song")
        print("4. Exit System")
        
        choice = input("Select an option ").strip()
        
        if choice == "1":
            print("\nExisting tracks")
            for idx, track in enumerate(analyzers, 1):
                print(f"[{idx}] {track.__class__.__name__} -> Title: '{track.title}' | Artist: {track.artist}")
        
        elif choice == "2":
            print("\nAnalyse songs")
            for track in analyzers:
                print(track.analyze())
        
        elif choice == "3":
            print("\nAdd your own track")
            print("Select Analyzer Type:")
            print("1. Lyrics Analyzer\n2. Audio Feature Analyzer\n3. Popularity Predictor")
            
            type_choice = input("Enter choices (1-3): ").strip()
            
            while True:
                try:
                    user_title = input("Enter track title: ")
                    user_artist = input("Enter artist name: ")
                    
                    if type_choice == "1":
                        user_lyrics = input("Enter sample lyrics (optional): ")
                        new_track = LyricsAnalyzer(user_title, user_artist, user_lyrics)
                    elif type_choice == "2":
                        new_track = AudioFeatureAnalyzer(user_title, user_artist)
                    else:
                        new_track = PopularityPredictor(user_title, user_artist)
                    
                    analyzers.append(new_track)
                    print(f"\n[SUCCESS] Added {new_track.__class__.__name__} successfully!")
                    break 
                    
                except InvalidSongDataError as e:
                    
                    print("Please enter the information again.\n")
        
        elif choice == "4":
            print("\nExiting")
            break
            
        else:
            print("\nInvalid choice! Please select an option between 1 and 5.")