# pathways

A 2d esoteric programming language


| Instruction     | Compound Instruction? | Pops? | Description                                                                                                                                                                                                                                                                                                                                             |
| ----------------- | ----------------------- | ------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `<`,`>`,`^`,`v` | N                     | 0     | Sets control flow to the specified direction.                                                                                                                                                                                                                                                                                                           |
| `?`             | Y (any)               | 1     | Only executes the next instruction if the popped value is truthy. Can be nested, but subsequent ?s will be treated as preceeding &s (to keep stack size known in each branch) e.g. ???? will compile as &&&?<br /> This guarantees that if the condition fails, four values will be popped from the stack, whereas ???? could pop any number of values. |
| `@`             | N                     | 0     | Adds one to the number of suppressions the program has. See below.                                                                                                                                                                                                                                                                                      |
| `$`             | Y (direction)         | 0     | See supression section. If compunded with a non-direction instruction, this instruction does nothing (the compounded instruction will run as normal)                                                                                                                                                                                                    |

## Supression


The `@` instruction is used to add a supression to the supression count. This describes how suppressions act on code.

In the table, `_` means any instruction not covered by other cases. `D`stands for any of`<>^v`. `*` means one or more copies of the preceeding instruction.

The instruction column is a non-compund instruction (i.e. the `D` row is not used if there is a `?` before it). note that `$_` is uncompounded unless `_` is `D`


| Instruction | No Supression                                                                   | Supression                                                                                         |
| ------------- | --------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `D`         | Sets control flow to the specified direction.                                   | Control flow carries on in the same direction. Suppression count decreases.                        |
| `?D`        | Pops 1 from the stack. If truthy, Sets control flow to the specified direction. | Pops 1 from the stack. Control flow carries on in the same direction. Suppression count decreases. |
