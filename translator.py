# pylint: disable=missing-class-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import sys
from enum import Enum


class CursorState(Enum):
    DATA = 0
    CODE = 1


class Command(int, Enum):
    NOP = 0b0000
    ADD = 0b0001
    SUB = 0b0010
    LD = 0b0011
    MOV = 0b0100
    INC = 0b0101
    NOT = 0b0110
    JMP = 0b0111
    CMP = 0b1000
    JZ = 0b1001
    JN = 0b1010
    JNZ = 0b1011
    SV = 0b1100
    HLT = 0b1101


commands = {
    "nop": Command.NOP,
    "sub": Command.SUB,
    "ld": Command.LD,
    "mov": Command.MOV,
    "inc": Command.INC,
    "not": Command.NOT,
    "jmp": Command.JMP,
    "cmp": Command.CMP,
    "jz": Command.JZ,
    "jnz": Command.JNZ,
    "sv": Command.SV,
    "hlt": Command.HLT,
}


def _is_label(line: list[str]) -> bool:
    return line[0][-1] == ":"


def _is_unimportant(line: list[str]) -> bool:
    return not line[0] or line[0].startswith(";")


def parse_labels(code: list[str]):
    counter = 0
    state = CursorState.DATA
    labels: dict = {}

    for line in code:
        words = line.split()
        if len(words) == 0:
            continue
        if ".code" in words[0]:
            state = CursorState.CODE
            continue
        if state == CursorState.CODE:
            if _is_unimportant(words):
                continue
            if _is_label(words):
                name: str = line[0][:-1]
                assert name not in labels, f"Label {name} has already defined earlier."
                labels[name] = counter
                words.pop(0)
        if len(words) > 0 and words[0].lower() in commands:
            counter += 1
        else:
            continue
    return labels


def translate(source: str) -> (list, list):
    with open(source, "r", encoding="utf-8") as file:
        code = file.readlines()
        state = CursorState.DATA
        print(code, state)

    data: list = []
    code: list = []
    mnemonics: list = []
    variables: dict = {}
    labels: dict = parse_labels(code)
    print(data, mnemonics, variables, labels)

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
