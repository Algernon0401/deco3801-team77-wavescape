from collections import defaultdict

# Initialize the track_history dictionary
track_history = defaultdict(list)

# Populate the track_history dictionary with sample data
track_history["track1"] = [
    (1.0, 2.0),
    (2.0, 3.0),
    (3.0, 4.0),
    (1.0, 2.0),
    (2.0, 3.0),
    (3.0, 4.0),
]  # Replace with your data
track_history["track2"] = [(2.0, 3.0), (3.0, 4.0), (4.0, 5.0)]  # Replace with your data

# Dictionary to store the average coordinates for each track
average_coordinates = {}

# Calculate the average for each track
for track_id, track in track_history.items():
    if track:
        total_x = sum(coord[0] for coord in track)
        total_y = sum(coord[1] for coord in track)
        avg_center_x = total_x / len(track)
        avg_center_y = total_y / len(track)
        avg_center = (avg_center_x, avg_center_y)
        average_coordinates[track_id] = avg_center
    else:
        average_coordinates[track_id] = None  # Handle cases with no coordinates

if len(track) > 2:  # keeps only the latest 30 records
    track.pop(0)

# Print the average coordinates for each track
for track_id, avg_center in average_coordinates.items():
    if avg_center is not None:
        print(f"Average Center Coordinate for {track_id}: {avg_center}")
        print(len(track))
    else:
        print(f"No coordinates for {track_id}.")
