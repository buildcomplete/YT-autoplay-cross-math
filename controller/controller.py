import os
import subprocess
import random
import shutil
import sys
import time
import Command
import datetime

def grab(local_path):
    subprocess.run(["adb", "shell", "screencap", "-p", "/sdcard/autograb.png"], check=True)
    subprocess.run(["adb", "pull", "/sdcard/autograb.png", local_path], check=True)

def adbClick(x,y):
    subprocess.run(f'adb shell input tap {x} {y}', shell=True, check=True)

def grabAndSolvePuzzle(run_id, step):

    # Create the ID as a string
    screenshot_name = f"{step}-crsmth.png"

    # Transfer the screenshot to the local computer
    local_screenshot_path = os.path.join(f"../shared/{run_id}/", screenshot_name)
    docker_screenshot_path = os.path.join(f"../shared/{run_id}/", screenshot_name)

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


def tryPassAdv(run_id, step, attempt):
    # check that we passed ad hell
    local_screenshot_path_ad = f"../shared/{run_id}/{step}-{attempt}-adck.png"
    docker_screenshot_path_ad = f"/shared/{run_id}/{step}-{attempt}-adck.png"
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


solver_errors_in_row=0
step=1
run_id = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# Create the folder if it does not exist
if not os.path.exists(f"../shared/{run_id}/"):
    os.makedirs(f"../shared/{run_id}/")

while (solver_errors_in_row < 3):
    try:
        grabAndSolvePuzzle(run_id,step)
        solver_errors_in_row=0
    except:
        solver_errors_in_row = solver_errors_in_row+1

    end_time = time.time() + 120 - solver_errors_in_row * 30
    attempt = 1
    while(False == tryPassAdv(run_id, step, attempt) and end_time > time.time()):
        time.sleep(0.3)
        attempt = attempt+1
    time.sleep(1.5)
    step = step+1
