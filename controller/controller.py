import os
import subprocess
import random
import shutil
import sys
import time
import Command

def grab(load_path):
    subprocess.run(["adb", "shell", "screencap", "-p", "/sdcard/autograb.png"], check=True)
    subprocess.run(["adb", "pull", "/sdcard/autograb.png", load_path], check=True)

def adbClick(x,y):
    subprocess.run(f'adb shell input tap {x} {y}', shell=True, check=True)

def grabAndSolvePuzzle():
    # Take a screenshot with a random name
    screenshot_id = random.randint(1000, 9999)
    screenshot_name = f"screenshot_{screenshot_id}.png"
    screenshot_path = os.path.join("/sdcard", screenshot_name)

    # Transfer the screenshot to the local computer
    local_screenshot_path = os.path.join("../shared/new", screenshot_name)
    docker_screenshot_path = os.path.join("/shared/new", screenshot_name)

    grab(local_screenshot_path)

    # Invoke Octave in a Docker container
    octave_command = f'docker exec -t eye octave go_bin.m "{docker_screenshot_path}" /shared/results/x.txt 0'
    subprocess.run(octave_command, shell=True, check=True)

    # Invoke another Python script in a Docker container
    python_command = f'docker exec -t brain python main.py /shared/results/x.txt /shared/results/x.swipe /shared/results/travel /shared/results/stats'
    subprocess.run(python_command, shell=True, check=True)

    if not os.path.exists("../shared/results/x.swipe"):
        print("Error: file does not exist")
        sys.exit(1)

    # Read the swipes in the swipe file and send them
    with  open("../shared/results/x.swipe", "r") as swipe_file:
        next(swipe_file)  # Skip the first line
        for line in swipe_file:
            src_r, src_c, dst_r, dst_c = map(int, line.strip().split(","))
            adbClick(dst_c, dst_r)
            time.sleep(0.3)
            adbClick(src_c, src_r)
            time.sleep(0.3)

    # Delete the file after it has been processed
    os.remove("../shared/results/x.swipe")

    # Click submit result, continue
    time.sleep(0.5)
    subprocess.run('adb shell input tap 750 1280', shell=True, check=True)
    time.sleep(10)
    subprocess.run('adb shell input tap 530 1890', shell=True, check=True)
    time.sleep(5)


def tryPassAdv():
    # check that we passed ad hell
    local_screenshot_path_ad = "../shared/adck.png"
    docker_screenshot_path_ad = "/shared/adck.png"
    grab(local_screenshot_path_ad)
    octave_command_ac = f'docker exec -t eye octave step_adcheck.m "{docker_screenshot_path_ad}" /shared/ad_check.txt 0'
    subprocess.run(octave_command_ac, shell=True, check=True)
    command = Command.Command.CreateCommandFromOctaveFile('../shared/ad_check.txt')
    
    if (command.commandName == "none"):
        return False # We are not done
    
    # If command not none, send click.
    adbClick(command.tabPosition[1], command.tabPosition[0])

    # Return true if this is the blue button that completes the advertisement loop
    return (command.commandName == 'bluenext')

while (True):
    grabAndSolvePuzzle()
    while(False == tryPassAdv()):
        time.sleep(1)
    time.sleep(1)
