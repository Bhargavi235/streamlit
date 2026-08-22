import requests
BASE_URL = "http://127.0.0.1:5000"


def get_all_songs():

    try:
        response = requests.get(f"{BASE_URL}/songs")    #get request from client
        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        print("ERROR : Could not connect to the Flask server.")
    except requests.exceptions.HTTPError:
        print("ERROR :", response.status_code)
    except Exception as e:
        print("Unexpected Error :", e)

    return None

def get_song(song_id):

    try:
        response = requests.get(f"{BASE_URL}/songs/{song_id}")
        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        print("ERROR : Server is unavailable.")
    except requests.exceptions.HTTPError:
        print("ERROR :", response.status_code)
    except Exception as e:
        print("Unexpected Error :", e)

    return None


def add_song(song_data):

    try:
        response = requests.post(
            f"{BASE_URL}/songs",
            json=song_data    #send song data as request

        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        print("ERROR : Server is unavailable.")
    except requests.exceptions.HTTPError:
        print("ERROR :", response.status_code)
    except Exception as e:
        print("Unexpected Error :", e)

    return None


def update_song(song_id, updated_data):

    try:

        response = requests.put(
            f"{BASE_URL}/songs/{song_id}",
            json=updated_data   #send ypdated data with id

        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        print("ERROR : Server is unavailable.")
    except requests.exceptions.HTTPError:
        print("ERROR :", response.status_code)
    except Exception as e:
        print("Unexpected Error :", e)

    return None


def delete_song(song_id):

    try:

        response = requests.delete(   #delete by id
            f"{BASE_URL}/songs/{song_id}"
        )

        response.raise_for_status()
        return True

    except requests.exceptions.ConnectionError:
        print("ERROR : Server is unavailable.")
    except requests.exceptions.HTTPError:
        print("ERROR :", response.status_code)
    except Exception as e:
        print("Unexpected Error :", e)

    return False



if __name__ == "__main__":
    songs = get_all_songs()

    if songs:

        for song in songs:
            print("ID :", song["id"])
            print("Track :", song["track_name"])
            print("Artist :", song["artist"])
            print("Genre :", song["genre"])
            print("Popularity :", song["popularity"])