
import subprocess

import Command


expectations = {
    'ad_trans_arrow.png': ("adv_next", (150, 83)),
    'ad_trans_arrow2.png': ("adv_next", (150, 1023)),
    'ad_trans_x.png': ("adv_next", (150, 1000)),
    'adck.png': ("none",(0,0)),
    'complte_next.png': ("bluenext", (1972, 540)),
}

in_folder_container = '/shared/test_data/cut_scenes/'
out_folder_container = '/shared/test_data/out/'
out_folder_host = '../shared/test_data/out/'

RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'


for filename, expectation in expectations.items():
    print (f"{filename}, {expectation}")
    
    testfileresult_container = f"{out_folder_container}advtest.txt"
    testfileresult_host = f"{out_folder_host}advtest.txt"

    octave_command = f'docker exec -t eye octave step_adcheck.m {in_folder_container}{filename} {testfileresult_container} 0'
    
    # Run the Octave command
    subprocess.run(octave_command, shell=True, check=True)
    with  open(testfileresult_host, "r") as fHandle:
        lines = [line.strip() for line in fHandle]
        command = Command.Command(lines)
        
        #coord = next(fHandle)
        print(f'{command.commandName} == {expectation[0]} and {command.tabPosition} == {expectation[1]}')
        if(command.commandName == expectation[0] and command.tabPosition == expectation[1] ):
            print(GREEN + 'passed' + RESET)
        else:
            print(RED + 'failed' + RESET)


    