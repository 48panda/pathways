# pathways

A 2d esoteric programming language

## Current Features

* Parsing to a graph (code cannot be run, but you can view the graph it makes)

## Current Instructions

### Special instructions

`?` -- Pops a value from the stack. Only executes the next instruction if the value it popped is truthy. Multiple `?`s in a row will be all be replaced with the `&` instruction (but only in that direction) e.g. `????` wil be interpreted as `&&&?` when moving right, `?&&&` when moving left and `?` for all 8 vertical approaches. This behaviour keeps the and property of multiple `?`s whilst making the stack more predictable if false (all values will be consumed.)

`n` -- parses the digits directly following it into a number and pushes it to the stack. Whitespace is not ignored. e.g. `n123` will push 123, while `n12 3` will push 12 and then 3, while `123` will push 1, 2 then 3.

`N` -- like `n`, but negates the number.

### Normal Instructions

* `^`, `v`, `<`, `>`: Changes instruction flow to the specified direction (the way the "arrow" points)
* `&`: Pops `a`, `b` from the stack. Pushes `True` if both `a` and `b` are truthy or `False` if either of them are not truthy
* `|`: Pops `a`, `b` from the stack. Pushes `True` if either `a` or `b` are truthy or `False` if neither of them are truthy
* `T`: Pushes `True`
* `F`: pushes `False`
* `!`: Pops and prints the popped value
* `+`: Pops `a`, `b` from the stack. pushes `a + b`
* `-`: Pops `a`, `b` from the stack. pushes `b - a`
* `*`: Pops `a`, `b` from the stack. pushes `a * b`
* `/`: Pops `a`, `b` from the stack. pushes `b / a`
* `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`: Pushes the respective integer to the stack.
* `d`: Pops from the stack. Pushes the value on twice.
* `=`: Pops `a`, `b` from the stack. pushes `a == b`
* `~`: pops `a` from the stack. If `a` is a boolean, pushes `not a`. If `a` is a number, returns `-a`. If `a` is a string, returns `a[::-1]`. Otherwise, pushes the value back unchanged

All characters:

```¬!"£$%^&*()_-+={}[]:;@'~#|\<>,.?/``

Currently in use:
`!^&*-+~#|<>?/`

Planned deprecations:
`#`

Currently not in use:
```¬"£$%()_={}[]:;@'\.,``

Planned to implement:

`%` for mod arithmetic
`"` for strings
`'` for characters
`=` for equals
`@` for **exciting new feature**
`UNKNOWN` for user input (could also use a letter)
`#` for escaping arrows (for 2-directional code) 
`.,` for secondary stack

Planned to not be in use:
```¬£$()_{}[]:;``