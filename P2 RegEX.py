1
from abc import ABC, abstractmethod
import re

class InvalidSongDataError(Exception):    # custom exception for song error
    pass
class InvalidNameError(Exception):     #wrong name
    pass
class InvalidEmailError(Exception):    #wrong email
    pass
class InvalidPasswordError(Exception):    #wrong password
    pass
class InvalidLoginError(Exception):    #invalid login
    pass

name_pattern = re.compile(r'^[A-Za-z ]{3,50}$')    #validate full name

username_pattern = re.compile(r'^[A-Za-z][A-Za-z0-9_]{4,14}$')    #username

email_pattern = re.compile(
    r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'    #email
)

phone_pattern = re.compile(r'^[6-9]\d{9}$')    #phone number

password_pattern = re.compile(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'    #password
)

users = {}   #storin users

def show_password_checklist(password):            #password requirements checklist

    upper = bool(re.search(r'[A-Z]', password))    #uppercase
    lower = bool(re.search(r'[a-z]', password))  #lowercase
    digit = bool(re.search(r'\d', password))     #digit
    special = bool(re.search(r'[@$!%*?&]', password))    #special character
    
    length = len(password) >= 8  #check length
    print("\nPassword Checklist")
    print(
        "Contains uppercase letter"
        if upper else
        "Does not contain uppercase letter"
    )

    print(
        "Contains lowercase letter"
        if lower else
        "Does not contain lowercase letter"
    )

    print(
        "Contains digit"
        if digit else
        "Does not contain digit"
    )

    print(
        "Contains special character"
        if special else
        "Does not contain special character"
    )

    print(
        "Minimum 8 characters"
        if length else
        "Please fill minimum 8 characters"
    )

    return upper and lower and digit and special and length

def register():

    try:
        full_name = input("Enter Full Name: ")

        if not name_pattern.fullmatch(full_name):    #fullmatch to check full name
            raise InvalidNameError(
                "Name should contain only alphabets and spaces."
            )
        username = input(
            "Enter Username (5-15 characters): "
        )
        if not username_pattern.match(username):    #match to check the starting element of username
            raise Exception(
                "Username must start with a letter and contain only letters, numbers or underscore."
            )

        if username in users:
            raise Exception(
                "Username already exists."   #duplicate
            )

        email = input("Enter Email: ")

        if not email_pattern.fullmatch(email):   #fullmatch pattern for email
            raise InvalidEmailError(
                "Invalid Email Format."
            )

        phone = input(
            "Enter Mobile Number: "
        )
        if not phone_pattern.fullmatch(phone):    #fullmatch pattern for phone 
            raise Exception(
                "Invalid Mobile Number."
            )

        while True:    #loop for password checklist
            password = input(
                "Enter Password: "
            )
            valid_password = (
                show_password_checklist(
                    password
                )
            )
            if (
                valid_password and
                password_pattern.fullmatch(password)   #password fullatch
            ):
                break
            print(
                "\nPassword does not meet all requirements."
            )
            print(
                "Please try again.\n"
            )

        genres = input(
            "Enter Favourite Genres (comma separated): "
        )

        genre_list = re.split(
            r',',
            genres  #split ,
        )
        users[username] = {    #add user
            "name": full_name,
            "email": email,
            "phone": phone,
            "password": password,
            "genres": genre_list
        }
        print(
            "\nRegistration Successful!"
        )

    except Exception as e:

        print(
            "\nRegistration Error:",
            e
        )


def login():

    try:
        username = input(
            "Enter Username: "
        )
        password = input(
            "Enter Password: "
        )
        if username not in users:
            raise InvalidLoginError(
                "Username does not exist."   #validare username in users 
            )
        if (
            users[username]["password"]
            != password
        ):
            raise InvalidLoginError(
                "Incorrect Password."   #invalid password
            )

        print(
            f"\nWelcome {users[username]['name']}!"
        )

        return True

    except InvalidLoginError as e:

        print(
            "\nLogin Error:",
            e
        )
        return False


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

    # Added optional keyword parameter
    def analyze(self, keyword=""):

        if self.lyrics:
            search_result = (
                re.search(    #search to see keyword
                    keyword,
                    self.lyrics,
                    re.IGNORECASE
                )
                if keyword
                else None
            )

            words = re.findall(   #findall lyrics
                r'\b\w+\b',
                self.lyrics
            )

            cleaned_lyrics = re.sub(   #sub
                r'[^A-Za-z ]',
                '',
                self.lyrics
            )

            return (
                f"\nTitle: {self.title}\n"
                f"Artist: {self.artist}\n"
                f"Total Words Found: {len(words)}\n"
                f"Keyword Found: "
                f"{'Yes' if search_result else 'No'}\n"
                f"Cleaned Lyrics: {cleaned_lyrics}\n"
                f"Emotional depth detected."
            )

        return (
            f"'{self.title}' by {self.artist}: "
            f"No lyrics provided to analyze -> "
            f"Basic thematic analysis applied."
        )


class AudioFeatureAnalyzer(MusicContent): #second derived class
    
    def analyze(self):   #overideen function in second derived class
        return f"'{self.title}' by {self.artist}: Scanning frequencies -> High energy, rhythmic synth-patterns, and danceable."


class PopularityPredictor(MusicContent):  #third derived class
  
    def analyze(self):      #overidden function in third derived class
        return f"'{self.title}' by {self.artist}: Checking streaming trends -> Strong hit potential on global charts."


if __name__ == "__main__":

    print("Music Information Retrieval")


    while True:

        print("\n")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        access_choice = input(
            "Enter Choice: "
        ).strip()

        if access_choice == "1":

            register()

        elif access_choice == "2":

            if login():
                break

        elif access_choice == "3":

            print("\nExit")
            exit()

        else:

            print("\nInvalid Choice")

    song1 = LyricsAnalyzer("Midnight Dreams", "Aurora Wave", "In the shadows of the night...")     #existing songs
    song2 = AudioFeatureAnalyzer("Electric Pulse", "Neon Beats")
    song3 = PopularityPredictor("Sunset Boulevard", "The Wanderers")
    
    analyzers = [song1, song2, song3]     #passing objects as a list

    while True:
        print("\n1. View existing songs")
        print("2. Analysis of songs")
        print("3. Add your song")
        print("4. View Registered Users")
        print("5. Exit System")
        
        choice = input("Select an option ").strip()
        
        if choice == "1":

            print("\nExisting tracks")

            for idx, track in enumerate(
                analyzers,
                1
            ):

                print(
                    f"[{idx}] "
                    f"{track.__class__.__name__}"
                    f" -> Title: '{track.title}'"
                    f" | Artist: {track.artist}"
                )
        
        elif choice == "2":

            # Ask user for keyword once
            keyword = input(
                "\nEnter a keyword to search in lyrics: "
            )

            print("\nAnalyse songs")

            for track in analyzers:

                # LyricsAnalyzer needs keyword
                if isinstance(
                    track,
                    LyricsAnalyzer
                ):

                    print(
                        track.analyze(
                            keyword
                        )
                    )

                else:

                    print(
                        track.analyze()
                    )
        
        elif choice == "3":

            print("\nAdd your own track")
            print("Select Analyzer Type:")
            print("1. Lyrics Analyzer")
            print("2. Audio Feature Analyzer")
            print("3. Popularity Predictor")
            
            type_choice = input(
                "Enter choices (1-3): "
            ).strip()
            
            while True:
                try:
                    user_title = input(
                        "Enter track title: "
                    )

                    user_artist = input(
                        "Enter artist name: "
                    )
                    
                    if type_choice == "1":

                        user_lyrics = input(
                            "Enter sample lyrics: "
                        )

                        new_track = LyricsAnalyzer(
                            user_title,
                            user_artist,
                            user_lyrics
                        )

                    elif type_choice == "2":

                        new_track = AudioFeatureAnalyzer(
                            user_title,
                            user_artist
                        )

                    elif type_choice == "3":

                        new_track = PopularityPredictor(
                            user_title,
                            user_artist
                        )

                    else:

                        print(
                            "Invalid Analyzer Type."
                        )

                        break
                    
                    analyzers.append(
                        new_track
                    )

                    print(
                        f"\n[SUCCESS] Added "
                        f"{new_track.__class__.__name__} successfully!"
                    )

                    break
                    
                except InvalidSongDataError as e:

                    print(e)
                    print(
                        "Please enter the information again.\n"
                    )

        elif choice == "4":

            # Display all registered users
            if not users:

                print(
                    "\nNo Registered Users."
                )

            else:

                print(
                    "\nRegistered Users"
                )

                for username, details in users.items():

                    print(
                        f"\nUsername: {username}"
                    )

                    print(
                        f"Name: {details['name']}"
                    )

                    print(
                        f"Email: {details['email']}"
                    )

                    print(
                        f"Genres: "
                        f"{', '.join(details['genres'])}"
                    )

        elif choice == "5":

            print("\nExiting")
            break
            
        else:
            print(
                "\nInvalid choice! Please select an option between 1 and 5."
            )