# pylint: disable=missing-class-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import sys
from enum import Enum

from config import AddressMask


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


# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
def translate(source: str) -> (list, list, list):
    with open(source, "r", encoding="utf-8") as file:
        code = file.readlines()
        state = CursorState.DATA
        print(code, state)

    data: list = []
    code: list = []
    mnemonics: list = []
    variables: dict = {}
    labels: dict = parse_labels(code)

    for line in code:
        tokens = line.split()
        for value in tokens:
            if ".data" in value:
                assert state == CursorState.DATA, "Data segment has already set"
                state = CursorState.DATA
                continue
            if ".code" in value:
                assert state == CursorState.CODE, "Code segment has already set"
                state = CursorState.CODE
                continue
            if value[0].startswith(";"):
                continue

            if state == CursorState.DATA:
                if len(tokens) >= 2 and tokens[0][-1] == ":":
                    name = tokens[0][:-1]
                    value = tokens[1]
                    assert (
                        name not in variables
                    ), f"Variable with {name} has already defined"
                    try:
                        value = int(value)
                    except ValueError as exception:
                        if len(value) == 1:
                            value = ord(value)
                        else:
                            raise exception

                elif len(tokens) == 1:
                    if tokens[0][0] != ";" and not tokens[0].contains("data"):
                        value = tokens[0]
                        try:
                            value = int(value)
                        except ValueError as exc:
                            if len(value) == 1:
                                value = ord(value)
                            else:
                                raise ValueError(f"Invalid value {value}") from exc
                        data.append(value)

                if state == CursorState.CODE:
                    if (
                        len(tokens) == 0
                        or tokens[0] == ""
                        or tokens[0][0] == ";"
                        or tokens[0].contains(".code")
                    ):
                        continue

                    if tokens[0][-1] == ":":
                        tokens.pop(0)
                        if len(tokens) == 0:
                            continue

                    mnemonic: str = tokens[0].lower()

                    # parse operand
                    operand: str = tokens[1]

                    if operand.startswith("#"):
                        operand = operand[1:]
                        try:
                            value = int(operand)
                            code.append(
                                commands[mnemonic]
                                << AddressMask.BIT_LENGTH + labels["start"]
                            )
                            continue
                        except ValueError:
                            pass

                        assert operand in variables, f"Unknown variable name: {operand}"
                        address: int = (
                            variables[operand] + AddressMask.STRAIGHT_ABSOLUTE
                        )

                    elif operand[0] == "$":
                        operand = operand[1:]
                        try:
                            value: int = int(operand)
                            address: int = value
                            assert address <= (
                                1 << AddressMask.WIDTH
                            ), "Address overflow"
                            address += AddressMask.STRAIGHT_ABSOLUTE
                        except ValueError:
                            assert (
                                operand in variables
                            ), f"Unknown variable name: {operand}"
                            address: int = (
                                variables[operand] + AddressMask.INDIRECT_ABSOLUTE
                            )

                    elif operand in labels:
                        address: int = labels[operand]

                    elif operand in variables:
                        address: int = (
                            int(variables[operand]) + AddressMask.ADDR_REFERENCE
                        )

                    code.append(
                        (commands[mnemonic].code << AddressMask.BIT_LENGTH) + address
                    )

                    mnemonics.append(mnemonic + " " + str(address))

                else:
                    code.append(commands[mnemonic] << AddressMask.BIT_LENGTH)
                    mnemonics.append(mnemonic)

            return code, data, mnemonics


def main(args):
    assert len(args) == 2, "Wrong arguments: translator.py <input_file> <target_file>"
    source, target = args

    with open(source, "rt", encoding="utf-8") as file:
        source = file.read()

    code, data, mnemonics = translate(source)
    print("source LoC:", len(source.split()), "code instr:", len(code), mnemonics)
    print(target, data)


if __name__ == "__main__":
    main(sys.argv[1:])


__all__ = ["main"]
