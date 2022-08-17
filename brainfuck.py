def find_closing_brace(text:str, start_index:int):
    """
    public int findClosingParen(char[] text, int openPos) {
    int closePos = openPos;
    int counter = 1;
    while (counter > 0) {
        char c = text[++closePos];
        if (c == '(') {
            counter++;
        }
        else if (c == ')') {
            counter--;
        }
    }
    return closePos;
}
"""
    close_index = start_index
    counter = 1
    while counter > 0:
        close_index+=1
        c = text[close_index]
        if c == "[":
            counter += 1
        elif c == "]":
            counter -= 1
    return close_index

def find_opening_brace(text:str, end_index: int):
    open_index = end_index
    counter = 1
    while counter > 0:
        open_index -= 1
        c = text[open_index]
        if c == "[":
            counter -= 1
        elif c == "]":
            counter += 1
    return open_index


def run(script: str):
    """
    OUTLINE:
    I need a:
        -   stack of length 255
        -   stack pointer
        -   command interpreter (>,<,+,-,[,],",",.,#)
        - > : Move stack pointer right
        - < : Move stack pointer left
        - + : Increment stack at pointer
        - - : Decrement stack at pointer
        - [ : Begin loop
        - ] : End loop
        - . : Print ascii value of stack at pointer
        - , : Accept input to stack at pointer
        
    """

    
    stack = [0 for _ in range(255)]
    stack_ptr = 0

    code_ptr = 0    #   Tells the program which line of code to run

    running = True
    while running:
        try:
            command = script[code_ptr]
        except IndexError:
            # We reached the end of the program
            running = False
            print(stack)

        if command == ">":
            # Increment ptr with wrapping
            stack_ptr = (stack_ptr+1) % 255
        elif command == "<":
            # Decrement stack_ptr with wrapping
            stack_ptr = (stack_ptr-1) % 255
        elif command == "+":
            stack[stack_ptr] += 1
        elif command == "-":
            stack[stack_ptr] -= 1
        elif command == ".":
            print(chr(stack[stack_ptr]), end="")
        elif command == "[":
            if stack[stack_ptr] == 0:
                code_ptr = find_closing_brace(script, code_ptr)

        elif command == "]":
            if stack[stack_ptr] != 0:
                code_ptr = find_opening_brace(script, code_ptr)

        code_ptr += 1


if __name__ == "__main__":
    script = """
        [ This program prints "Hello World!" and a newline to the screen, its
  length is 106 active command characters. [It is not the shortest.]

  This loop is an "initial comment loop", a simple way of adding a comment
  to a BF program such that you don't have to worry about any command
  characters. Any ".", ",", "+", "-", "<" and ">" characters are simply
  ignored, the "[" and "]" characters just have to be balanced. This
  loop and the commands it contains are ignored because the current cell
  defaults to a value of 0; the 0 value causes this loop to be skipped.
]
++++++++               Set Cell #0 to 8
[
    >++++               Add 4 to Cell #1; this will always set Cell #1 to 4
    [                   as the cell will be cleared by the loop
        >++             Add 2 to Cell #2
        >+++            Add 3 to Cell #3
        >+++            Add 3 to Cell #4
        >+              Add 1 to Cell #5
        <<<<-           Decrement the loop counter in Cell #1
    ]                   Loop until Cell #1 is zero; number of iterations is 4
    >+                  Add 1 to Cell #2
    >+                  Add 1 to Cell #3
    >-                  Subtract 1 from Cell #4
    >>+                 Add 1 to Cell #6
    [<]                 Move back to the first zero cell you find; this will
                        be Cell #1 which was cleared by the previous loop
    <-                  Decrement the loop Counter in Cell #0
]                       Loop until Cell #0 is zero; number of iterations is 8

The result of this is:
Cell no :   0   1   2   3   4   5   6
Contents:   0   0  72 104  88  32   8
Pointer :   ^

>>.                     Cell #2 has value 72 which is 'H'
>---.                   Subtract 3 from Cell #3 to get 101 which is 'e'
+++++++..+++.           Likewise for 'llo' from Cell #3
>>.                     Cell #5 is 32 for the space
<-.                     Subtract 1 from Cell #4 for 87 to give a 'W'
<.                      Cell #3 was set to 'o' from the end of 'Hello'
+++.------.--------.    Cell #3 for 'rl' and 'd'
>>+.                    Add 1 to Cell #5 gives us an exclamation point
>++.                    And finally a newline from Cell #6
    """
    # script = "+++++[-]"
    run(script)