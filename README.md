# pathways

A 2d esoteric programming language

## Current Features

* Parsing to a graph (code cannot be run, but you can view the graph it makes)

## Current Instructions

### Special instructions

`?` -- Pops a value from the stack. Only executes the next instruction if the value it popped is truthy. Multiple `?`s in a row will be all be replaced with the `&` instruction (but only in that direction) e.g. `????` wil be interpreted as `&&&?` when moving right, `?&&&` when moving left and `?` for all 8 vertical approaches. This behaviour keeps the and property of multiple `?`s whilst making the stack more predictable if false (all values will be consumed.)

### Normal Instructions

* `^`,`v`,`<`,`>`: Changes instruction flow to the specified direction (the way the "arrow" points)
* `&`: Pops `a`, `b` from the stack. Otherwise, it pushes `True` if both `a` and `b` are truthy or `False` if either of them are not truthy
* `|`: Pops `a`, `b` from the stack. Otherwise, it pushes `True` if either `a` or `b` are truthy or `False` if neither of them are truthy
* `T`: Pushes `True`
* `F`: pushes `False`
