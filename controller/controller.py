import os
import subprocess
import random
import shutil
import time

# Take a screenshot with a random name
screenshot_id = random.randint(1000, 9999)
screenshot_name = f"screenshot_{screenshot_id}.png"
screenshot_path = os.path.join("/sdcard", screenshot_name)
subprocess.run(["adb", "shell", "screencap", "-p", screenshot_path], check=True)

# Transfer the screenshot to the local computer
local_screenshot_path = os.path.join("../shared/new", screenshot_name)
docker_screenshot_path = os.path.join("/shared/new", screenshot_name)

subprocess.run(["adb", "pull", screenshot_path, local_screenshot_path], check=True)

# Invoke Octave in a Docker container
octave_command = f'docker exec -t eye octave go_bin.m "{docker_screenshot_path}" /shared/results/x.txt 0'
subprocess.run(octave_command, shell=True, check=True)

# Invoke another Python script in a Docker container
python_command = f'docker exec -t brain python main.py /shared/results/x.txt /shared/results/x.swipe /shared/results/travel /shared/results/stats'
subprocess.run(python_command, shell=True, check=True)

# Read the swipes in the swipe file and send them
swipe_file = open("../shared/results/x.swipe", "r")
next(swipe_file)  # Skip the first line
for line in swipe_file:
    src_r, src_c, dst_r, dst_c = map(int, line.strip().split(","))
    clickOne = f'adb shell input tap {dst_c} {dst_r}'
    clickTwo = f'adb shell input tap {src_c} {src_r}'
    subprocess.run(clickOne, shell=True, check=True)
    time.sleep(0.1)
    subprocess.run(clickTwo, shell=True, check=True)
    time.sleep(1)

# Close the swipe file
swipe_file.close()
