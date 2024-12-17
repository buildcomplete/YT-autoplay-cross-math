import math
import subprocess
import Command

expectations = {
    'ad_trans_arrow.png': ("adv_next", (150, 83)),
    'ad_trans_arrow2.png': ("adv_next", (150, 1023)),
    'ad_trans_arrow3.png': ("adv_next", (143, 1022)),
    'ad_trans_arrow4.png': ("adv_next", (150, 1023)),
    'ad_trans_arrow5.png': ("adv_next", (150, 1023)),
    'ad_trans_arrow6.png': ("adv_next", (150, 1023)),
    'ad_trans_x.png': ("adv_next", (150, 1000)),
    'ad_trans_x2.png': ("adv_next", (156, 80)),
    'ad_trans_x3.png': ("adv_next", (179, 981)),
    'ad_trans_x4.png': ("adv_next", (177, 979)),
    'ad_trans_x5.png': ("adv_next", (177, 979)),
    'ad_trans_x6.png': ("adv_next", (144, 1015)),
    'ad_trans_x7.png': ("adv_next", (170, 90)),
    'ad_trans_x8.png': ("adv_next", (39, 39)),
    'ad_trans_x9.png': ("adv_next", (142, 1020)),
    'nothing.png': ("none",(0,0)),
    'complte_next.png': ("bluenext", (1972, 540)),
}

in_folder_container = '/shared/test_data/cut_scenes/'
out_folder_container = '/shared/test_data/out/'
out_folder_host = '../shared/test_data/out/'

RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

def euclidean_distance(cmd, target_position):
    """Calculates the Euclidean distance between the tabPosition of this Command object and a given target position."""
    x1, y1 = cmd.tabPosition
    x2, y2 = target_position
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def testCmdIsOk(exp,cmd, tol):
    return exp[0] !=cmd and euclidean_distance(cmd, exp[1]) < tol

for filename, expectation in expectations.items():
    testfileresult_container = f"{out_folder_container}advtest.txt"
    testfileresult_host = f"{out_folder_host}advtest.txt"
    octave_command = f'docker exec -t eye octave step_adcheck.m {in_folder_container}{filename} {testfileresult_container} 0'
    
    # Run the Octave command
    subprocess.run(octave_command, shell=True, check=True)
    command = Command.Command.CreateCommandFromOctaveFile(testfileresult_host)
    if testCmdIsOk(expectation, command, 10 ):
        print(f"{filename},Expection: {expectation}, Actual: {command.commandName} {command.tabPosition}" + GREEN + ' passed' + RESET)
    else:
        print(f"{filename}, Expection: {expectation}, Actual: {command.commandName} {command.tabPosition}" + RED + ' failed' + RESET)


    
