from os.path import realpath, dirname, abspath
import json
import hashlib


def get_config(name):
    path = abspath(dirname(dirname(realpath(__file__)))) + '/configs/' + name + '.json'
    with open(path, 'r', encoding='utf-8') as fd:
        return json.loads(fd.read())


def get_md5(string):
    md = hashlib.md5()
    md.update(string.encode("utf-8"))
    return md.hexdigest()
