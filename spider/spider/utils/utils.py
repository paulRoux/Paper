from os.path import realpath, dirname, abspath
import json
import hashlib
import os
import subprocess


def get_config(name):
    path = abspath(dirname(dirname(realpath(__file__)))) + '/configs/' + name + '.json'
    with open(path, 'r', encoding='utf-8') as fd:
        return json.loads(fd.read())


def get_md5(string):
    md = hashlib.md5()
    md.update(string.encode("utf-8"))
    return md.hexdigest()


def run_proxy_pool():
    cmd = 'python run.py'
    os.getcwd()
    cwd = os.getcwd() + "/spider/IpProxyPool"
    print(cwd)
    if os.path.exists(cwd):
        os.chdir(cwd)
    else:
        return False
    subprocess.Popen(cmd, shell=True)
