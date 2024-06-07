# What for dinner - lab 3 - variant 4

This is an example project which demonstrates project structure and necessary
CI checks. It is not the best structure for real-world projects, but good
enough for educational purposes.

## Project structure

- `fsm.py` -- implementation of `Foo` class with `hello` and `add` features.
   Stateless.
- `fsm_test.py` -- unit and PBT tests for `Foo`.

## Features

- PBT: `test_add_commutative`

## Contribution

- Lu Bin (1476683166@qq.com) -- All work.
- Wang Yining (351432511@qq.com) -- All work.

## Changelog

- 08.06.2022 - 4
  - Add visualization functions.
  - modify code style.
- 07.06.2022 - 3
  - Complete design of finite state machine.
  - Implement tests.
- 06.06.2022 - 2
  - Add more function of finite state machine.
- 05.06.2022 - 1
  - Implement basic function of finite state machine 
- 03.06.2022 - 0
  - Initial

## Design notes

- ...

## Visualize

- Test Cases
   - Since there are too few states in the traffic light,
     there are only three states: red, yellow and green,
     and the output of each state is different,
     green 123 is added as an additional state of the green light,
     similar to the green light countdown,
     which better shows that the output is independent of the input.

| State | Output |
|-------|--------|
|Red    |Stop    |
|Green1 |Go      |
|Green2 |Go      |
|Green3 |Go      |
|Yellow |Caution |

| Source | Destination | Output | Latency |
|--------|-------------|--------|---------|
|Red     |Green1       |Stop    |1        |
|Green1  |Green2       |Go      |1        |
|Green2  |Green3       |Go      |1        |
|Green3  |Yellow       |Go      |1        |
|Yellow  |Red          |Caution |1        |