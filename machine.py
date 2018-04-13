"""A Turing machine example ("Busy Beaver").

https://en.wikipedia.org/wiki/Turing_machine
"""
from collections import deque


class Machine:
    """A one-tape Turing machine."""

    def __init__(self,
                 states,
                 initial_state,
                 final_state,
                 alphabet,
                 blank,
                 instruction_table):
        """Create a new machine."""
        self.states = states
        self.initial_state = initial_state
        self.final_state = final_state

        self.alphabet = alphabet
        self.blank = blank

        self.instruction_table = instruction_table

        # Initialize machine
        self.tape = deque(self.blank)
        self.current_state = initial_state
        self.head_position = 0

    def read_symbol(self):
        """Read tape at currently location and return symbol."""
        # Simulate an infinite tape by growing the list as necessary
        if self.head_position < 0:
            self.tape.appendleft(self.blank)
            self.head_position = 0
        elif self.head_position >= len(self.tape):
            self.tape.append(self.blank)
            self.head_position = len(self.tape) - 1
        return self.tape[self.head_position]

    def write_symbol(self, sym):
        """Write a specific symbol to the current tape location."""
        try:
            self.tape[self.head_position] = sym
        except IndexError:
            # This shouldn't happen if the read_symbol
            # method grows the list properly
            print("Time to replace the tape head.")
            raise

    def move_tape(self, direction):
        """Move tape one step in given direction (L or R)."""
        if direction == "L":
            self.head_position -= 1
        if direction == "R":
            self.head_position += 1

    def run(self):
        """Start the Turing machine."""
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


def main():
    """Create and run a Busy Beaver Turing machine."""
    # Define the "Busy Beaver"
    # https://en.wikipedia.org/wiki/Busy_beaver

    states = ["A", "B", "C", "HALT"]

    initial_state = "A"

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

    # Test the machine!
    m = Machine(states, initial_state, final_state, alphabet, blank, instruction_table)

    m.run()


if __name__ == "__main__":
    main()
