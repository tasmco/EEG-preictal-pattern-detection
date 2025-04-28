import mne
import os

# Define source and destination directories (update paths if needed)
src_dir = r"C:\Users\XXX\normalized_segments"
dest_dir = r"C:\Users\XXX\five_second_segments"

# Create the destination directory if it does not exist
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)
    print(f"Created destination folder: {dest_dir}")

# Duration (in seconds) for each segment
segment_duration = 5.0

# Process each .fif file in the source folder
for filename in os.listdir(src_dir):
    if filename.endswith('.fif'):
        file_path = os.path.join(src_dir, filename)
        print(f"Opening file: {file_path}")
        try:
            # Read the raw file (ignoring naming warnings)
            raw = mne.io.read_raw_fif(file_path, preload=True, verbose=False)
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            continue

        # Get total duration in seconds from the raw instance
        total_time = raw.times[-1]
        n_segments = int(total_time // segment_duration)
        print(f"Total duration: {total_time:.2f} s, splitting into {n_segments} segments.")

        # Loop to crop and save each 5-second segment
        for i in range(n_segments):
            start = i * segment_duration
            stop = (i + 1) * segment_duration
            # Crop the data (set include_tmax=False so that segments do not overlap)
            segment = raw.copy().crop(tmin=start, tmax=stop, include_tmax=False)
            # Generate a new filename with a segment suffix
            new_filename = f"{os.path.splitext(filename)[0]}_seg{i+1}_5s_raw.fif"
            new_file_path = os.path.join(dest_dir, new_filename)
            segment.save(new_file_path, overwrite=True)
            print(f"Saved segment {i+1}: {start:.2f} s to {stop:.2f} s as {new_filename}")

print("Splitting completed!")
