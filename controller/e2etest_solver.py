import os
import threading
import subprocess
import concurrent.futures

# Create a lock
lock = threading.Lock()

# Replace 'path/to/input/folder' with the path to the folder containing the images
in_folder_host = '../shared/test_data/images/'
in_folder_container = '/shared/test_data/images/'
out_folder_container = '/shared/test_data/out/'

# Define the maximum number of threads
max_workers = 12
results = {}
# Define a function to run the tests for a single image
def run_tests_for_image(filename):
    
    # Define the Octave command
    filename_no_ext = os.path.splitext(filename)[0]
    path_cont_img = f'{in_folder_container}{filename}'
    path_cont_out_eye = f'{out_folder_container}{filename_no_ext}.txt'
    octave_command = f'docker exec -t eye octave go_bin.m {path_cont_img} {path_cont_out_eye} 0'

    path_swipe_dummy = f'{out_folder_container}{filename_no_ext}.swipe'
    path_travel_dummy = f'{out_folder_container}{filename_no_ext}.travel'
    path_stats_dummy = f'{out_folder_container}{filename_no_ext}.stats'
    # Define the Python command
    python_command = f'docker exec -t brain python main.py {path_cont_out_eye} {path_swipe_dummy} {path_travel_dummy} {path_stats_dummy}'
    try:
        # Run the Octave command
        subprocess.run(octave_command, shell=True, check=True)

        # Run the Python command
        subprocess.run(python_command, shell=True, check=True)

        results[filename]='passed'

    except subprocess.CalledProcessError as e:
        results[filename]='failed'

# Create a ThreadPoolExecutor with the specified number of workers
with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    # Iterate through all the images in the input folder
    for filename in sorted(os.listdir(in_folder_host)):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            # Submit the function call to the executor
            executor.submit(run_tests_for_image, filename)

# Print the results at the end of the test
for filename, result in results.items():
    print(f'{filename}: {result}')