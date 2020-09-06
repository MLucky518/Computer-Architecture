"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.running = False
        self.pc = 0

    def load(self):
        """Load a program into memory."""
        self.read_argv()
        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def read_argv(self):
        params = sys.argv

        if len(params) != 2:
            print(f"Usage: file.py filename")
            sys.exit(1)

        if len(params) == 2:
            try:
                with open(params[1]) as f:
                    address = 0
                    for line in f:
                        split_comment = line.split("#")
                        num = split_comment[0].strip()
                        if num == '':
                            continue
                        num2 = int("0b"+num,2)
                        self.ram_write(address,num2)
                        address += 1
            except:
                print("file not found")
                sys.exit(2)
                            



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def run(self):
        self.running = True
        HLT = 0b00000001
        PRN = 0b01000111
        LDI = 0b10000010  # binary code for 130
        MUL = 0b10100010
        self.load()
        self.trace()
        while self.running:
            current_instruction = self.ram_read(self.pc)
            op_a = self.ram_read(self.pc+1)
            op_b = self.ram_read(self.pc+2)

            if current_instruction == LDI:
                self.reg[op_a] = op_b
                self.pc += 3

            elif current_instruction == PRN:
                print(self.reg[op_a])
                self.pc += 2
            elif current_instruction == MUL:
                self.reg[op_a] = self.reg[op_a] * self.reg[op_b]
                self.pc+=3

            elif current_instruction == HLT:
                self.running = False
cpu = CPU()


cpu.run()