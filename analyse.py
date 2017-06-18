#!/usr/bin/env python3
import json
import os
import pickle
import shlex
import shutil
import tempfile

import docker
from tqdm import tqdm

client = docker.from_env()

scripts_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'docker_scripts'
)

with open('.tmp/stage_01.pickle', 'rb') as input_fn:
    data = pickle.load(input_fn)

for i in tqdm(data):
    tmp_dir = tempfile.mkdtemp(prefix='rolca_', dir='/tmp')
    shutil.copy(os.path.join('.tmp', data[i]['file']), tmp_dir)
    
    file_name = os.path.basename(data[i]['file'])

    result = client.containers.run(
        "centos-opencv",
        command=shlex.split("sh -c 'run_cv.py {}'".format(file_name)),
        volumes={
            tmp_dir: {'bind': '/data', 'mode': 'rw'},
            scripts_path: {'bind': '/scripts', 'mode': 'ro'},
        },
        remove=True,
    )
    
    shutil.rmtree(tmp_dir)

    data[i].update(json.loads(result))


print(data[1])
