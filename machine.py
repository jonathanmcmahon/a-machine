""" A Turing machine example ("Busy Beaver").

https://en.wikipedia.org/wiki/Turing_machine

"""
from collections import deque


class Machine:

    states = ["A", "B", "C", "HALT"]

    final_state = "HALT"

    alphabet = ["0", "1"]

    blank = "0"

    instruction_table = {
        "A":
            {
                "0": ("1", "R", "B"),
                "1": ("1", "L", "C")
            },
        "B":
            {
                "0": ("1", "L", "A"),
                "1": ("1", "R", "B")
            },
        "C":
            {
                "0": ("1", "L", "B"),
                "1": ("1", "R", "HALT")
            }
    }


    def __init__(self, initial_state="A"):
        self.tape = deque(self.blank)
        self.current_state = initial_state
        self.head_position = 0

    def read_symbol(self):
        # Simulate an infinite tape by growing the list as necessary
        if self.head_position < 0:
            self.tape.appendleft(self.blank)
            self.head_position = 0
        elif self.head_position >= len(self.tape):
            self.tape.append(self.blank)
            self.head_position = len(self.tape) - 1
        return self.tape[self.head_position]

    def write_symbol(self, sym):
        try:
            self.tape[self.head_position] = sym
        except IndexError:
            # This shouldn't happen if the read_symbol
            # method grows the list properly
            print("Time to replace the tape head.")
            raise

    def move_tape(self, direction):
        if direction == "L":
            self.head_position -= 1
        if direction == "R":
            self.head_position += 1

    def run(self):

        print(list(self.tape))

        while self.current_state is not self.final_state:

            # Read the symbol off the tape
            s = self.read_symbol()
            assert s in self.alphabet, "Symbol not in alphabet!"

            # Look up the instruction based on state and symbol
            instruction = self.instruction_table[self.current_state][s]

            # Decode instruction
            write_sym, move_dir, next_state = instruction

            # Write the appropriate symbol to tape per instruction
            self.write_symbol(write_sym)

            # Move tape per instruction
            self.move_tape(move_dir)

            # Change state per instruction
            self.current_state = next_state

            # The tale of the tape
            print(list(self.tape))

        # Our machine has encountered a terminal state
        print("HALT!")


if __name__ == "__main__":

    # Test the machine!

    m = Machine()

    m.run()
