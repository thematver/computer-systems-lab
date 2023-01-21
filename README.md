# computer-systems-lab
Корепанов Матвей из группы P33101

`asm | acc | harv | hw | instr | binary | stream | port | prob5`

```
       ASM
        |                                       ввод (stream)
        |                      Система команд        |
        |                           |                v
        |     +------------+        |          +------------+
   -----*---->| Транслятор |--------*--------->|   Модель   |----> журнал
      prob5   +------------+   машинный код    | процессора |
                                 (binary)      +------------+
                                                     |
                                                     v
                                                вывод (stream)

```

# Структура программы
```angular2html
.data
<var_name>: <var_value> ;<comment>
.code
<label>: <operation_mnemonic> <operand>; <comment>
```

# BNF
```angular2html
<operation_no_arg> ::= "INC"
<operation_one_arg> ::= "JMP" | "LD" | "ADD"
<operation> ::= <operation_no_arg> | <operation_one_arg> <data_value>
<space> ::= " "
<new_line> ::= "\t"
<letter> ::= ([a-z] | [A-Z])+
<space_or_letter> ::= <space> | <letter>
<comment> ::= ; <space_or_letter> <new_line> | ""
<label> ::= <letter>

<data_value> ::= (<letter>)+ | [0-9]+
<data_line> ::= <label>: <data_value> <comment>

<code_line> ::= <label>: <operation> <comment>

<data_segment> ::= ".data" <new_line> (<data_line>)+
<code_segment> ::= ".code" <new_line> (<code_line>)+

<program> ::= [<data_segment>] <code_segment>
```
