import streamlit as st
import os
import re
import shutil
from datetime import datetime


# ============================================================
# CONFIGURATION
# ============================================================

DATA_FILE = "music_records.txt"
BACKUP_FILE = "music_records_backup.txt"

HEADER = (
    "track_id|track_name|artists|album_name|popularity|"
    "duration_ms|explicit|track_genre\n"
)


# ============================================================
# VALIDATION FUNCTIONS
# ============================================================

def validate_track_id(track_id):
    """
    Spotify Track IDs normally contain 22 alphanumeric characters.
    """
    return bool(re.fullmatch(r"[A-Za-z0-9]{22}", track_id))


def validate_text(value, field_name):
    """
    Validate general text fields.
    """
    if not value.strip():
        return False, f"{field_name} cannot be empty."

    if "|" in value:
        return False, f"{field_name} cannot contain the | character."

    return True, ""


def validate_popularity(value):
    """
    Popularity must be an integer between 0 and 100.
    """
    try:
        popularity = int(value)

        if 0 <= popularity <= 100:
            return True, ""

        return False, "Popularity must be between 0 and 100."

    except ValueError:
        return False, "Popularity must be a valid integer."


def validate_duration(value):
    """
    Duration must be a positive integer.
    """
    try:
        duration = int(value)

        if duration > 0:
            return True, ""

        return False, "Duration must be greater than 0."

    except ValueError:
        return False, "Duration must be a valid integer."


def validate_explicit(value):
    """
    Explicit field must be Yes or No.
    """
    if value in ["Yes", "No"]:
        return True, ""

    return False, "Explicit value must be Yes or No."


def validate_record(record):
    """
    Validate all fields of a music record.
    """

    track_id = record["track_id"]
    track_name = record["track_name"]
    artists = record["artists"]
    album_name = record["album_name"]
    popularity = record["popularity"]
    duration_ms = record["duration_ms"]
    explicit = record["explicit"]
    genre = record["track_genre"]

    # Track ID validation
    if not validate_track_id(track_id):
        return False, "Track ID must contain exactly 22 alphanumeric characters."

    # Text validations
    for value, field in [
        (track_name, "Track Name"),
        (artists, "Artists"),
        (album_name, "Album Name"),
        (genre, "Genre")
    ]:
        valid, message = validate_text(value, field)

        if not valid:
            return False, message

    # Popularity
    valid, message = validate_popularity(popularity)

    if not valid:
        return False, message

    # Duration
    valid, message = validate_duration(duration_ms)

    if not valid:
        return False, message

    # Explicit
    valid, message = validate_explicit(explicit)

    if not valid:
        return False, message

    return True, "Record is valid."


# ============================================================
# FILE CREATION
# ============================================================

def create_file(records=None):
    """
    Create/overwrite the music data file using 'w' mode.
    """

    if records is None:
        records = []

    with open(DATA_FILE, "w", encoding="utf-8") as file:

        # Demonstrates write()
        file.write(HEADER)

        for record in records:

            line = (
                f"{record['track_id']}|"
                f"{record['track_name']}|"
                f"{record['artists']}|"
                f"{record['album_name']}|"
                f"{record['popularity']}|"
                f"{record['duration_ms']}|"
                f"{record['explicit']}|"
                f"{record['track_genre']}\n"
            )

            file.write(line)


# ============================================================
# W+ MODE DEMONSTRATION
# ============================================================

def initialize_file():
    """
    Demonstrates w+ mode.

    w+ allows both writing and reading.
    This function is only used when the file does not exist,
    preventing accidental deletion of existing records.
    """

    if not os.path.exists(DATA_FILE):

        with open(DATA_FILE, "w+", encoding="utf-8") as file:

            file.write(HEADER)

            # Demonstrates tell()
            position_after_write = file.tell()

            # Demonstrates seek()
            file.seek(0)

            # Demonstrates read()
            contents = file.read()

            return position_after_write, contents

    return None, None


# ============================================================
# READ FUNCTIONS
# ============================================================

def read_all_records():
    """
    Read and return all records using readlines().
    """

    initialize_file()

    records = []

    try:

        with open(DATA_FILE, "r", encoding="utf-8") as file:

            # Demonstrates readlines()
            lines = file.readlines()

            for line in lines[1:]:

                line = line.strip()

                if not line:
                    continue

                parts = line.split("|")

                if len(parts) == 8:

                    record = {
                        "track_id": parts[0],
                        "track_name": parts[1],
                        "artists": parts[2],
                        "album_name": parts[3],
                        "popularity": parts[4],
                        "duration_ms": parts[5],
                        "explicit": parts[6],
                        "track_genre": parts[7]
                    }

                    records.append(record)

    except FileNotFoundError:
        return []

    return records


def read_first_record():
    """
    Demonstrates readline().
    """

    initialize_file()

    try:

        with open(DATA_FILE, "r", encoding="utf-8") as file:

            # Demonstrates readline()
            header = file.readline()

            first_record = file.readline()

            return header, first_record

    except FileNotFoundError:

        return "", ""


# ============================================================
# APPEND RECORD
# ============================================================

def append_record(record):
    """
    Append a new record using 'a' mode.
    """

    valid, message = validate_record(record)

    if not valid:
        return False, message

    existing_records = read_all_records()

    # Check duplicate Track ID
    for existing in existing_records:

        if existing["track_id"] == record["track_id"]:

            return False, "A record with this Track ID already exists."

    try:

        with open(DATA_FILE, "a", encoding="utf-8") as file:

            line = (
                f"{record['track_id']}|"
                f"{record['track_name']}|"
                f"{record['artists']}|"
                f"{record['album_name']}|"
                f"{record['popularity']}|"
                f"{record['duration_ms']}|"
                f"{record['explicit']}|"
                f"{record['track_genre']}\n"
            )

            # Demonstrates write()
            file.write(line)

        return True, "Music record added successfully."

    except Exception as e:

        return False, f"Error while adding record: {e}"


# ============================================================
# SEARCH RECORD
# ============================================================

def search_record(track_id):
    """
    Search for a record using Track ID.
    """

    initialize_file()

    try:

        with open(DATA_FILE, "r", encoding="utf-8") as file:

            # Demonstrates readline()
            header = file.readline()

            while True:

                line = file.readline()

                if not line:
                    break

                parts = line.strip().split("|")

                if len(parts) == 8 and parts[0] == track_id:

                    return {
                        "track_id": parts[0],
                        "track_name": parts[1],
                        "artists": parts[2],
                        "album_name": parts[3],
                        "popularity": parts[4],
                        "duration_ms": parts[5],
                        "explicit": parts[6],
                        "track_genre": parts[7]
                    }

    except FileNotFoundError:

        return None

    return None


# ============================================================
# UPDATE RECORD
# ============================================================

def update_record(track_id, updated_record):
    """
    Update an existing record.

    Demonstrates r+ mode, seek() and tell().
    """

    valid, message = validate_record(updated_record)

    if not valid:
        return False, message

    try:

        with open(DATA_FILE, "r+", encoding="utf-8") as file:

            # Demonstrates tell()
            start_position = file.tell()

            # Demonstrates readlines()
            lines = file.readlines()

            # Demonstrates seek()
            file.seek(0)

            found = False
            new_lines = [HEADER]

            for line in lines[1:]:

                parts = line.strip().split("|")

                if len(parts) != 8:
                    continue

                if parts[0] == track_id:

                    found = True

                    new_line = (
                        f"{updated_record['track_id']}|"
                        f"{updated_record['track_name']}|"
                        f"{updated_record['artists']}|"
                        f"{updated_record['album_name']}|"
                        f"{updated_record['popularity']}|"
                        f"{updated_record['duration_ms']}|"
                        f"{updated_record['explicit']}|"
                        f"{updated_record['track_genre']}\n"
                    )

                    new_lines.append(new_line)

                else:

                    new_lines.append(line)

            if not found:

                return False, "Track ID not found."

            # Rewrite entire file from beginning
            file.seek(0)

            # Demonstrates writelines()
            file.writelines(new_lines)

            # Remove old content remaining after rewritten data
            file.truncate()

            return True, "Record updated successfully."

    except Exception as e:

        return False, f"Error while updating record: {e}"


# ============================================================
# DELETE RECORD
# ============================================================

def delete_record(track_id):
    """
    Delete a record using Track ID.
    """

    try:

        records = read_all_records()

        new_records = []

        found = False

        for record in records:

            if record["track_id"] == track_id:

                found = True

            else:

                new_records.append(record)

        if not found:

            return False, "Track ID not found."

        # Recreate file using w mode
        create_file(new_records)

        return True, "Record deleted successfully."

    except Exception as e:

        return False, f"Error while deleting record: {e}"


# ============================================================
# BACKUP
# ============================================================

def create_backup():
    """
    Create a backup copy of the data file.
    """

    try:

        initialize_file()

        shutil.copy2(DATA_FILE, BACKUP_FILE)

        return True, "Backup created successfully."

    except Exception as e:

        return False, f"Backup failed: {e}"


# ============================================================
# CONVERT RECORDS FOR STREAMLIT TABLE
# ============================================================

def records_to_table(records):

    table = []

    for record in records:

        table.append({
            "Track ID": record["track_id"],
            "Track Name": record["track_name"],
            "Artists": record["artists"],
            "Album": record["album_name"],
            "Popularity": int(record["popularity"]),
            "Duration (ms)": int(record["duration_ms"]),
            "Explicit": record["explicit"],
            "Genre": record["track_genre"]
        })

    return table


# ============================================================
# STREAMLIT USER INTERFACE
# ============================================================

st.set_page_config(
    page_title="MusicTrack Manager",
    page_icon="🎵",
    layout="wide"
)


# Initialize file
initialize_file()


# ============================================================
# HEADER
# ============================================================

st.title("🎵 MusicTrack Manager")

st.write(
    "A domain-based file management application for managing "
    "music analysis records using Python text-file handling."
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("📂 File Management")

st.sidebar.write(f"Data File: `{DATA_FILE}`")

if os.path.exists(DATA_FILE):

    file_size = os.path.getsize(DATA_FILE)

    st.sidebar.success(
        f"Data file available\n\nSize: {file_size} bytes"
    )

else:

    st.sidebar.error("Data file not found.")


if st.sidebar.button("🔄 Initialize Data File"):

    create_file([])

    st.sidebar.success("Data file initialized.")

    st.rerun()


if st.sidebar.button("💾 Create Backup"):

    success, message = create_backup()

    if success:

        st.sidebar.success(message)

    else:

        st.sidebar.error(message)


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 View Records",
    "➕ Add Record",
    "🔍 Search",
    "✏️ Update",
    "🗑️ Delete"
])


# ============================================================
# VIEW RECORDS
# ============================================================

with tab1:

    st.subheader("All Music Records")

    records = read_all_records()

    if records:

        st.dataframe(
            records_to_table(records),
            use_container_width=True
        )

        st.info(f"Total records: {len(records)}")

    else:

        st.warning("No music records found.")


# ============================================================
# ADD RECORD
# ============================================================

with tab2:

    st.subheader("Add New Music Record")

    col1, col2 = st.columns(2)

    with col1:

        track_id = st.text_input(
            "Track ID",
            placeholder="22-character Spotify Track ID"
        )

        track_name = st.text_input(
            "Track Name"
        )

        artists = st.text_input(
            "Artist(s)"
        )

        album_name = st.text_input(
            "Album Name"
        )

    with col2:

        popularity = st.number_input(
            "Popularity Score",
            min_value=0,
            max_value=100,
            value=50
        )

        duration_ms = st.number_input(
            "Duration (milliseconds)",
            min_value=1,
            value=180000
        )

        explicit = st.selectbox(
            "Explicit Content",
            ["No", "Yes"]
        )

        track_genre = st.text_input(
            "Genre"
        )

    if st.button("➕ Add Music Record"):

        record = {
            "track_id": track_id.strip(),
            "track_name": track_name.strip(),
            "artists": artists.strip(),
            "album_name": album_name.strip(),
            "popularity": str(popularity),
            "duration_ms": str(duration_ms),
            "explicit": explicit,
            "track_genre": track_genre.strip()
        }

        success, message = append_record(record)

        if success:

            st.success(message)

        else:

            st.error(message)


# ============================================================
# SEARCH
# ============================================================

with tab3:

    st.subheader("🔍 Search Music Record")

    search_id = st.text_input(
        "Enter Track ID",
        key="search_id"
    )

    if st.button("🔍 Search Record"):

        if not validate_track_id(search_id.strip()):

            st.error(
                "Invalid Track ID. "
                "It must contain exactly 22 alphanumeric characters."
            )

        else:

            result = search_record(search_id.strip())

            if result:

                st.success("Record found!")

                st.write("### Music Details")

                col1, col2 = st.columns(2)

                with col1:

                    st.write(f"**Track ID:** {result['track_id']}")
                    st.write(f"**Track Name:** {result['track_name']}")
                    st.write(f"**Artist:** {result['artists']}")
                    st.write(f"**Album:** {result['album_name']}")

                with col2:

                    st.write(
                        f"**Popularity:** {result['popularity']}"
                    )

                    st.write(
                        f"**Duration:** {result['duration_ms']} ms"
                    )

                    st.write(
                        f"**Explicit:** {result['explicit']}"
                    )

                    st.write(
                        f"**Genre:** {result['track_genre']}"
                    )

            else:

                st.error("No record found for this Track ID.")


# ============================================================
# UPDATE
# ============================================================

with tab4:

    st.subheader("✏️ Update Music Record")

    update_id = st.text_input(
        "Track ID to Update",
        key="update_id"
    )

    if st.button("Load Record"):

        result = search_record(update_id.strip())

        if result:

            st.session_state["update_record"] = result

            st.success("Record loaded. Edit the details below.")

        else:

            st.error("Track ID not found.")


    if "update_record" in st.session_state:

        record = st.session_state["update_record"]

        col1, col2 = st.columns(2)

        with col1:

            new_track_name = st.text_input(
                "Track Name",
                value=record["track_name"],
                key="update_track_name"
            )

            new_artists = st.text_input(
                "Artists",
                value=record["artists"],
                key="update_artists"
            )

            new_album = st.text_input(
                "Album Name",
                value=record["album_name"],
                key="update_album"
            )

            new_genre = st.text_input(
                "Genre",
                value=record["track_genre"],
                key="update_genre"
            )

        with col2:

            new_popularity = st.number_input(
                "Popularity",
                min_value=0,
                max_value=100,
                value=int(record["popularity"]),
                key="update_popularity"
            )

            new_duration = st.number_input(
                "Duration (ms)",
                min_value=1,
                value=int(record["duration_ms"]),
                key="update_duration"
            )

            new_explicit = st.selectbox(
                "Explicit",
                ["No", "Yes"],
                index=0 if record["explicit"] == "No" else 1,
                key="update_explicit"
            )

        if st.button("💾 Update Record"):

            updated_record = {
                "track_id": record["track_id"],
                "track_name": new_track_name.strip(),
                "artists": new_artists.strip(),
                "album_name": new_album.strip(),
                "popularity": str(new_popularity),
                "duration_ms": str(new_duration),
                "explicit": new_explicit,
                "track_genre": new_genre.strip()
            }

            success, message = update_record(
                record["track_id"],
                updated_record
            )

            if success:

                st.success(message)

                del st.session_state["update_record"]

            else:

                st.error(message)


# ============================================================
# DELETE
# ============================================================

with tab5:

    st.subheader("🗑️ Delete Music Record")

    delete_id = st.text_input(
        "Track ID to Delete",
        key="delete_id"
    )

    st.warning(
        "Deleting a record permanently removes it from the "
        "current data file. Create a backup before deletion if required."
    )

    if st.button("🗑️ Delete Record"):

        if not validate_track_id(delete_id.strip()):

            st.error(
                "Invalid Track ID. "
                "It must contain exactly 22 alphanumeric characters."
            )

        else:

            success, message = delete_record(
                delete_id.strip()
            )

            if success:

                st.success(message)

            else:

                st.error(message)



st.divider()

with st.expander(" File Handling Concepts Demonstrated"):

    st.markdown("""
    ### File Opening Modes

    - **`w`** – Creates/overwrites the music data file.
    - **`r`** – Reads existing music records.
    - **`a`** – Appends new music records.
    - **`r+`** – Reads and modifies records during update.
    - **`w+`** – Creates a new file and allows both reading and writing.

    ### File Handling Methods

    - **`read()`** – Reads complete file contents.
    - **`readline()`** – Reads one line at a time.
    - **`readlines()`** – Reads all lines into a list.
    - **`write()`** – Writes individual records.
    - **`writelines()`** – Writes multiple lines.
    - **`seek()`** – Moves the file pointer.
    - **`tell()`** – Returns the current file pointer position.
    - **`close()`** – File resources are safely closed using `with open()`.
    """)



st.caption(
    "MusicTrack Manager | Python File Handling + Streamlit | "
    "Music Analysis Domain"
)