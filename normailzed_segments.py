import os
import mne
import numpy as np

def z_score_normalize(data):
    """
    Applies z-score normalization to the data.
    Data is assumed to be in shape (n_channels, n_samples).
    """
    return (data - np.mean(data, axis=1, keepdims=True)) / np.std(data, axis=1, keepdims=True)

def process_file(file_path, output_folder):
    try:
        # Load raw data (using preload=True to load all data into memory)
        raw = mne.io.read_raw_fif(file_path, preload=True, verbose=False)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return

    # Extract the data and time vector
    data, times = raw.get_data(return_times=True)
    
    # Apply z-score normalization channel-wise
    data_norm = z_score_normalize(data)
    
    # Update the raw object's data with the normalized data
    raw._data = data_norm

    # Construct the output file path (keeping the same filename)
    file_name = os.path.basename(file_path)
    output_path = os.path.join(output_folder, file_name)
    
    # Save the normalized file (overwrite if exists)
    raw.save(output_path, overwrite=True, verbose=False)
    print(f"File {file_name} normalized and saved.")

def process_folder(input_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Iterate over all files ending with .fif in the input folder
    for file in os.listdir(input_folder):
        if file.endswith('.fif'):
            file_path = os.path.join(input_folder, file)
            process_file(file_path, output_folder)

if __name__ == '__main__':
    # Set the input folder (cleaned segments) and output folder (normalized segments)
    input_folder = r"C:\Users\XXX\cleaned_segments"
    output_folder = r"C:\Users\XXX\normalized_segments"
    process_folder(input_folder, output_folder)
