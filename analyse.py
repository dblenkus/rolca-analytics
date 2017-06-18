#!/usr/bin/env python3
import json
import os
import pickle
import shlex
import shutil
import tempfile

import docker
from tqdm import tqdm

tmp_dir = tempfile.mkdtemp(prefix='rolca_', dir='/tmp')

scripts_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'docker_scripts'
)

with open('.tmp/stage_01.pickle', 'rb') as input_fn:
    data = pickle.load(input_fn)
    
client = docker.from_env()
container = client.containers.create(
    'centos-opencv', 
    '/bin/bash',
    volumes={
        tmp_dir: {'bind': '/data', 'mode': 'rw'},
        scripts_path: {'bind': '/scripts', 'mode': 'ro'},
    },
    stdin_open=True,
    tty=True
)
container.start()

try:
    bar_format = '{desc}{percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]'

    for i in tqdm(data, bar_format=bar_format):
        shutil.copy(os.path.join('.tmp', data[i]['file']), tmp_dir)
        file_name = os.path.basename(data[i]['file'])

        result = container.exec_run('run_cv.py {}'.format(file_name))
        data[i].update(json.loads(result))

        os.remove(os.path.join(tmp_dir, file_name))
finally:
    container.kill()
    container.remove()

    shutil.rmtree(tmp_dir)

with open('.tmp/stage_02.pickle', 'wb') as output_fn:
    data = pickle.dump(data, output_fn)
