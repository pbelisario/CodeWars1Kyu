# Regular Expression for Binary Numbers Divisible by n

Create a function that will return a regular expression string that is capable of evaluating binary strings (which consist of only 1s and 0s) and determining whether the given string represents a number divisible by n.


### Notes
- Strings that are not binary numbers should be rejected.

- Keep your solution under 5000 characters. This means you can't hard-code the answers.

- Only these characters may be included in your returned string: _01?:*+^$()[]|_

### Python Notes
- Whenever you use parentheses (...), instead use non-capturing ones (?:...). This is due to module re's restriction in the number of capturing (or named) groups, which is capped at 99.

- Each regex will be tested with re.search, so be sure to include both starting and ending marks in your regex.
- The second anti-cheat test checks if you used any of re, sys, or print in your code. You won't need to print anything since each test will show what numbers your code is being tested on.

Available in <https://www.codewars.com/kata/regular-expression-for-binary-numbers-divisible-by-n>

## SOLUTION IDEA

- Built a FSM (Finite state machine), vased on the remainder of any number divided by n.

- Each vertex will by a possible remainder of a division by n, with 0 as the final vertex.
    - For example, if n = 3 then the vertices will be 0, 1 , 2
- Each edge will by which binary number it is needed to read to go from one vertex for another.
    - For example, if n = 3 then the graph built will be
    <img class="graph" src="images\mod3_Graph.png">

    | Origin Vertex | Number Read | Final Vertex |
    | ------------- | ----------- | ------------ |
    |       0       |      0      |       0      |
    |       0       |      1      |       1      |
    |       1       |      0      |       2      |
    |       1       |      1      |       0      |
    |       2       |      0      |       1      |
    |       2       |      1      |       2      |


- Then, translate de FSM built to a regular expression.

