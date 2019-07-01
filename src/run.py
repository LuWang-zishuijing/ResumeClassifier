from os import listdir
from os.path import isfile, join
import subprocess
from subprocess import Popen, PIPE, STDOUT
import os
import time

input_location = './input'

if not os.path.exists('./output/'):
    os.makedirs('./output/')

def process_one(id, name):
    output_json = f'./tmp.json'
   
    p = subprocess.run(["python", "./job.py", name, output_json], stdout=PIPE, stderr=PIPE)

    output = p.stdout.decode('utf8')
    outerr = p.stderr.decode('utf8')

    if outerr:
        # failed case
        print(f'There is an error for {name}')
        print(outerr)
        output_log = f'./output/fail/{id}/stdout.log'
        error_log = f'./output/fail/{id}/stderr.log'

        result_state = 'failure'
    else:
        # successful case
        output_log = f'./output/succeed/{id}/stdout.log'
        error_log = f'./output/succeed/{id}/stderr.log'

        json_dir = os.path.dirname(os.path.realpath(f'./output/succeed/{id}/1.json'))
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)

        os.rename(output_json, f'./output/succeed/{id}/{name}.json')

        result_state = 'success'

    output_log_dir = os.path.dirname(os.path.realpath(output_log))
    if not os.path.exists(output_log_dir):
        os.makedirs(output_log_dir)

    file = open(output_log, 'w')
    file.write(output)
    file.close()

    error_log_dir = os.path.dirname(os.path.realpath(error_log))
    if not os.path.exists(error_log_dir):
        os.makedirs(error_log_dir)

    file = open(error_log, 'w')
    file.write(outerr)
    file.close()


    print(f'{id} {name} completed with {result_state}')


def tick():
    onlyfiles = [f for f in listdir(input_location) if isfile(join(input_location, f))]

    onefile_id = onlyfiles[0]

    fullpath = join(input_location, onefile_id)

    with open(fullpath, 'r') as content_file:
        name = content_file.read()

    process_one(onefile_id, name)

    # remove input
    os.remove(fullpath)

    return len(onlyfiles) == 1

while True:
    start = time.time()

    is_done = tick()

    end = time.time()
    print(f'spend time: {end - start}\n')

    print('waiting 5 sec')
    if is_done:
        break

    time.sleep(5)

