from os.path import realpath, dirname
import json


def get_config(name):
    path = dirname(realpath(__file__)) + '/' + name + '.json'
    with open(path, 'r', encoding='utf-8') as f:
        return json.loads(f.read())


if __name__ == '__main__':
    import sys
    name = sys.argv[1]
    configs = get_config(name)
    print(configs)