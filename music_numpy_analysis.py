# ============================================================
# PROGRAM: NUMPY-BASED MUSIC ANALYSIS
# DOMAIN: MUSIC ANALYSIS
# ============================================================

# Import NumPy for numerical computations and array operations.
import numpy as np

# Import Pandas to read and process the CSV file.
import pandas as pd

# Import Matplotlib for data visualization.
import matplotlib.pyplot as plt


# ============================================================
# 1. LOAD THE MUSIC DATASET
# ============================================================

# Specify the name of the CSV file.
# Replace this with the actual path if the CSV is stored elsewhere.
file_path = "spotify-tracks-dataset.csv"

# Read the CSV file using Pandas.
df = pd.read_csv(file_path, encoding="utf-8")

# Display basic information about the dataset.
print("Music Dataset Loaded Successfully")
print("----------------------------------")

# Display the number of rows and columns.
print("Number of records:", len(df))
print("Number of columns:", len(df.columns))

# Display the first five records.
print("\nFirst Five Records:")
print(df.head())


# ============================================================
# 2. SELECT NUMERICAL FEATURES
# ============================================================

# Select important numerical audio features from the dataset.
# These features are useful for music popularity analysis.
audio_features = [
    "popularity",
    "duration_ms",
    "danceability",
    "energy",
    "loudness",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo"
]

# Create a new DataFrame containing only the selected features.
music_numeric = df[audio_features].copy()

# Remove rows containing missing values.
# This prevents numerical operations from producing NaN results.
music_numeric = music_numeric.dropna()

# Convert the selected Pandas data into a NumPy array.
music_array = music_numeric.to_numpy()

print("\nNumPy Array Shape:")
print(music_array.shape)


# ============================================================
# 3. COMPUTATION WITH NUMPY
# ============================================================

print("\n")
print("=" * 60)
print("3. COMPUTATION WITH NUMPY")
print("=" * 60)

# Extract the popularity column as a NumPy array.
popularity = music_numeric["popularity"].to_numpy()

# Extract the energy column as a NumPy array.
energy = music_numeric["energy"].to_numpy()

# Extract the danceability column as a NumPy array.
danceability = music_numeric["danceability"].to_numpy()

# Extract the valence column as a NumPy array.
valence = music_numeric["valence"].to_numpy()

# Calculate the average popularity using NumPy.
average_popularity = np.mean(popularity)

# Calculate the average energy using NumPy.
average_energy = np.mean(energy)

# Calculate the average danceability using NumPy.
average_danceability = np.mean(danceability)

# Display the calculated values.
print("Average Popularity:", round(average_popularity, 2))
print("Average Energy:", round(average_energy, 2))
print("Average Danceability:", round(average_danceability, 2))


# ============================================================
# 4. AGGREGATIONS
# ============================================================

print("\n")
print("=" * 60)
print("4. AGGREGATIONS")
print("=" * 60)

# Calculate the minimum popularity.
minimum_popularity = np.min(popularity)

# Calculate the maximum popularity.
maximum_popularity = np.max(popularity)

# Calculate the mean popularity.
mean_popularity = np.mean(popularity)

# Calculate the median popularity.
median_popularity = np.median(popularity)

# Calculate the standard deviation of popularity.
std_popularity = np.std(popularity)

# Calculate the total popularity value across all records.
total_popularity = np.sum(popularity)

# Display the aggregation results.
print("Minimum Popularity:", minimum_popularity)
print("Maximum Popularity:", maximum_popularity)
print("Mean Popularity:", round(mean_popularity, 2))
print("Median Popularity:", round(median_popularity, 2))
print("Standard Deviation:", round(std_popularity, 2))
print("Total Popularity:", total_popularity)


# ============================================================
# 5. COMPUTATION ON ARRAYS
# ============================================================

print("\n")
print("=" * 60)
print("5. COMPUTATION ON ARRAYS")
print("=" * 60)

# Create a NumPy array containing the first ten popularity values.
sample_popularity = popularity[:10]

# Increase every popularity score by 5.
# NumPy performs this operation element by element.
increased_popularity = sample_popularity + 5

# Multiply popularity values by 2.
doubled_popularity = sample_popularity * 2

# Divide popularity values by 100 to convert them into a 0-1 scale.
normalized_popularity = sample_popularity / 100

# Calculate the square root of popularity values.
sqrt_popularity = np.sqrt(sample_popularity)

# Display the results.
print("Original Popularity:")
print(sample_popularity)

print("\nPopularity + 5:")
print(increased_popularity)

print("\nPopularity x 2:")
print(doubled_popularity)

print("\nNormalized Popularity:")
print(normalized_popularity)

print("\nSquare Root of Popularity:")
print(sqrt_popularity)


# ============================================================
# 6. COMPARISONS, MASKS AND BOOLEAN ARRAYS
# ============================================================

print("\n")
print("=" * 60)
print("6. COMPARISONS, MASKS AND BOOLEAN ARRAYS")
print("=" * 60)

# Create a Boolean array identifying highly popular songs.
# A value of True means that the popularity is at least 80.
high_popularity_mask = popularity >= 80

# Use the Boolean mask to extract only highly popular songs.
high_popularity_songs = popularity[high_popularity_mask]

# Count the number of highly popular songs.
number_of_high_popularity_songs = np.sum(high_popularity_mask)

# Create another mask for highly energetic songs.
high_energy_mask = energy >= 0.8

# Count the number of highly energetic songs.
number_of_high_energy_songs = np.sum(high_energy_mask)

# Create a mask for highly danceable songs.
high_danceability_mask = danceability >= 0.8

# Count the number of highly danceable songs.
number_of_high_danceability_songs = np.sum(high_danceability_mask)

# Display the results.
print("Number of songs with popularity >= 80:",
      number_of_high_popularity_songs)

print("Number of songs with energy >= 0.8:",
      number_of_high_energy_songs)

print("Number of songs with danceability >= 0.8:",
      number_of_high_danceability_songs)


# ============================================================
# 7. COMBINED BOOLEAN CONDITIONS
# ============================================================

print("\n")
print("=" * 60)
print("7. COMBINED BOOLEAN CONDITIONS")
print("=" * 60)

# Identify songs that are both highly popular and highly energetic.
popular_and_energetic = (
    (popularity >= 80) &
    (energy >= 0.8)
)

# Count songs satisfying both conditions.
count_popular_energetic = np.sum(popular_and_energetic)

# Identify songs that are popular OR highly danceable.
popular_or_danceable = (
    (popularity >= 80) |
    (danceability >= 0.8)
)

# Count songs satisfying at least one condition.
count_popular_or_danceable = np.sum(popular_or_danceable)

# Display the results.
print(
    "Popular and energetic songs:",
    count_popular_energetic
)

print(
    "Popular or highly danceable songs:",
    count_popular_or_danceable
)


# ============================================================
# 8. FANCY INDEXING
# ============================================================

print("\n")
print("=" * 60)
print("8. FANCY INDEXING")
print("=" * 60)

# Select specific positions from the popularity array.
# This demonstrates NumPy fancy indexing.
selected_indices = [0, 5, 10, 15, 20]

# Extract values at the selected positions.
selected_popularity = popularity[selected_indices]

# Display the selected values.
print("Selected indices:")
print(selected_indices)

print("\nPopularity values at selected indices:")
print(selected_popularity)


# Select several rows and columns from the NumPy matrix.
# Rows represent songs and columns represent audio features.
selected_rows = [0, 2, 4, 6, 8]

# Select columns for popularity, energy and danceability.
selected_columns = [0, 3, 2]

# Perform fancy indexing using NumPy.
selected_data = music_array[
    np.ix_(selected_rows, selected_columns)
]

# Display the selected data.
print("\nSelected music data:")
print(selected_data)


# ============================================================
# 9. SORTING ARRAYS
# ============================================================

print("\n")
print("=" * 60)
print("9. SORTING ARRAYS")
print("=" * 60)

# Sort popularity values in ascending order.
sorted_popularity = np.sort(popularity)

# Display the five least popular scores.
print("Five lowest popularity scores:")
print(sorted_popularity[:5])

# Display the five highest popularity scores.
print("\nFive highest popularity scores:")
print(sorted_popularity[-5:])


# ============================================================
# 10. FIND TOP 10 SONGS USING NUMPY
# ============================================================

print("\n")
print("=" * 60)
print("10. TOP 10 SONGS")
print("=" * 60)

# Obtain indices that would sort popularity in ascending order.
sorted_indices = np.argsort(popularity)

# Reverse the indices to obtain descending popularity.
descending_indices = sorted_indices[::-1]

# Select the top ten indices.
top_10_indices = descending_indices[:10]

# Retrieve the corresponding rows from the original DataFrame.
top_10_songs = music_numeric.iloc[top_10_indices]

# Display the top ten numerical records.
print(top_10_songs)


# ============================================================
# 11. TOP 10 SONG NAMES
# ============================================================

# Get the original DataFrame rows corresponding to the top songs.
top_10_original = df.loc[top_10_songs.index]

# Display song names and artists.
print("\nTop 10 Most Popular Songs:")
print("----------------------------------")

for index, row in top_10_original.iterrows():

    # Retrieve the song name.
    song_name = row["track_name"]

    # Retrieve the artist name.
    artist_name = row["artists"]

    # Retrieve the popularity score.
    song_popularity = row["popularity"]

    # Display the song details.
    print(
        song_name,
        "-",
        artist_name,
        "| Popularity:",
        song_popularity
    )


# ============================================================
# 12. NUMPY CORRELATION
# ============================================================

print("\n")
print("=" * 60)
print("12. CORRELATION ANALYSIS")
print("=" * 60)

# Calculate the correlation between popularity and energy.
popularity_energy_correlation = np.corrcoef(
    popularity,
    energy
)[0, 1]

# Calculate the correlation between popularity and danceability.
popularity_danceability_correlation = np.corrcoef(
    popularity,
    danceability
)[0, 1]

# Calculate the correlation between popularity and valence.
popularity_valence_correlation = np.corrcoef(
    popularity,
    valence
)[0, 1]

# Display correlation results.
print(
    "Popularity vs Energy:",
    round(popularity_energy_correlation, 3)
)

print(
    "Popularity vs Danceability:",
    round(popularity_danceability_correlation, 3)
)

print(
    "Popularity vs Valence:",
    round(popularity_valence_correlation, 3)
)


# ============================================================
# 13. DATA VISUALIZATION
# ============================================================

# Create a small sample of the dataset for visualizations.
# Using a sample keeps the graphs readable and efficient.
plot_sample = df.sample(
    n=min(1000, len(df)),
    random_state=42
)


# ============================================================
# 13.1 BAR CHART
# ============================================================

# Group the data by genre and calculate average popularity.
genre_popularity = (
    df.groupby("track_genre")["popularity"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

# Create a new figure.
plt.figure(figsize=(12, 6))

# Create the bar chart.
plt.bar(
    genre_popularity.index,
    genre_popularity.values
)

# Add a title.
plt.title("Top 10 Genres by Average Popularity")

# Add labels to the axes.
plt.xlabel("Genre")
plt.ylabel("Average Popularity")

# Rotate genre names for readability.
plt.xticks(rotation=45)

# Adjust the layout.
plt.tight_layout()

# Display the chart.
plt.show()


# ============================================================
# 13.2 HISTOGRAM
# ============================================================

# Create a new figure for the histogram.
plt.figure(figsize=(10, 6))

# Plot the distribution of popularity scores.
plt.hist(
    popularity,
    bins=20,
    edgecolor="black"
)

# Add a title.
plt.title("Distribution of Music Popularity")

# Add axis labels.
plt.xlabel("Popularity")
plt.ylabel("Number of Songs")

# Adjust the layout.
plt.tight_layout()

# Display the histogram.
plt.show()


# ============================================================
# 13.3 SCATTER PLOT
# ============================================================

# Create a new figure.
plt.figure(figsize=(10, 6))

# Plot energy against popularity.
plt.scatter(
    plot_sample["energy"],
    plot_sample["popularity"],
    alpha=0.5
)

# Add a title.
plt.title("Energy vs Popularity")

# Add axis labels.
plt.xlabel("Energy")
plt.ylabel("Popularity")

# Adjust the layout.
plt.tight_layout()

# Display the scatter plot.
plt.show()


# ============================================================
# 13.4 LINE PLOT
# ============================================================

# Select the first 30 records for a readable line plot.
line_data = df.head(30)

# Create a new figure.
plt.figure(figsize=(12, 6))

# Plot popularity values.
plt.plot(
    range(len(line_data)),
    line_data["popularity"]
)

# Add a title.
plt.title("Popularity Across Sampled Tracks")

# Add axis labels.
plt.xlabel("Track Index")
plt.ylabel("Popularity")

# Adjust the layout.
plt.tight_layout()

# Display the line plot.
plt.show()


# ============================================================
# 13.5 PIE CHART
# ============================================================

# Count the number of songs belonging to the five most common genres.
genre_counts = (
    df["track_genre"]
    .value_counts()
    .head(5)
)

# Create a new figure.
plt.figure(figsize=(8, 8))

# Create the pie chart.
plt.pie(
    genre_counts.values,
    labels=genre_counts.index,
    autopct="%1.1f%%"
)

# Add a title.
plt.title("Distribution of Top 5 Music Genres")

# Display the pie chart.
plt.show()


# ============================================================
# 14. FINAL SUMMARY
# ============================================================

print("\n")
print("=" * 60)
print("MUSIC ANALYSIS COMPLETE")
print("=" * 60)

# Display a final summary of the analysis.
print("Total records analysed:", len(df))

print(
    "Average popularity:",
    round(np.mean(popularity), 2)
)

print(
    "Average energy:",
    round(np.mean(energy), 2)
)

print(
    "Average danceability:",
    round(np.mean(danceability), 2)
)

print(
    "Highly popular songs:",
    np.sum(popularity >= 80)
)

print(
    "Highly energetic songs:",
    np.sum(energy >= 0.8)
)

print(
    "Highly danceable songs:",
    np.sum(danceability >= 0.8)
)

print("\nAnalysis completed successfully.")