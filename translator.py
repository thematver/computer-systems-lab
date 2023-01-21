# pylint: disable=missing-class-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import sys


def translate(source: str) -> (list, list):
    source.split()
    return [], []


def main(args):
    assert len(args) == 2, "Wrong arguments: translator.py <input_file> <target_file>"
    source, target = args

    with open(source, "rt", encoding="utf-8") as file:
        source = file.read()

    code, data = translate(source)
    print("source LoC:", len(source.split()), "code instr:", len(code))
    print(target, data)


if __name__ == "__main__":
    main(sys.argv[1:])
