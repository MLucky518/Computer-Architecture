"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.sp = 7  # Last index in the registry is 7
        self.reg[self.sp] = 0xF4  # reserved space for the start of stack
        self.running = False
        self.flag_reg = [0] * 8
        self.pc = 0
        self.branch_table = {

            0b01000111: self.op_PRN,
            0b10000010: self.op_LDI,
            0b10100010: self.op_MUL,
            0b00000001: self.op_HLT,
            0b01000101: self.push_to_stack,
            0b01000110: self.pop_from_stack,
            0b01010000: self.call,
            0b00010001: self.return_op,
            0b10100000: self.ADD,
            0b10100001:self.SUB,
            0b10100111: self.CMP,
            0b01010100: self.JMP,
            0b01010110: self.JNE,
            0b01010101: self.JEQ,
            0b10101000: self.AND,
            0b10101010: self.OR,
            0b10101011: self.XOR,
            0b01101001: self.NOT


        }

    def load(self):
        print(self.flag_reg)
        """Load a program into memory."""
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
                        num2 = int("0b"+num, 2)
                        self.ram_write(address, num2)
                        address += 1
            except:
                print("file not found")
                sys.exit(2)

    def push_to_stack(self, a, b):
        # decrements the stack counter by one as the stack grows downward
        self.reg[self.sp] -= 1

        reg_val = self.reg[a]
        self.ram_write(self.reg[self.sp], reg_val)
        self.pc += 2

    def pop_from_stack(self, a, b):
        popped_val = self.ram_read(self.reg[self.sp])
        self.reg[a] = popped_val
        self.reg[self.sp] += 1
        self.pc += 2

    def op_MUL(self, a, b):
        self.alu("MUL", a, b)

    def AND(self, a, b):
        a = self.reg[a]
        b = self.reg[b]
        self.alu("AND", a, b)

    def OR(self, a, b):
        a = self.reg[a]
        b = self.reg[b]
        self.alu("OR", a, b)

    def XOR(self, a, b):
        a = self.reg[a]
        b = self.reg[b]
        self.alu("XOR", a, b)

    def NOT(self, a, b):
        a = self.reg[a]
        self.alu("NOT", a, b)

    def return_op(self, a, b):
        self.pc = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1

    def CMP(self, a, b):
        a = self.reg[a]
        b = self.reg[b]
        self.alu("CMP", a, b)

    def JMP(self, a, b):
        self.pc = self.reg[a]

    def JEQ(self, a, b):
        if self.flag_reg[-1] == 1:
            self.JMP(a, b)
        else:
            self.pc += 2

    def JNE(self, a, b):
        if self.flag_reg[-1] == 0:
            self.JMP(a, b)
        else:
            self.pc += 2

    def call(self, a, b):
        return_address = self.pc + 2
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[self.sp], return_address)
        self.pc = self.reg[a]

    def op_HLT(self, a, b):
        self.running = False

    def ADD(self, a, b):
        self.alu("ADD", a, b)

    def SUB(self, a, b):
        self.alu("SUB", a, b)

    def op_PRN(self, a, b):
        print(self.reg[a])
        self.pc += 2

    def op_LDI(self, a, b):

        self.reg[a] = b
        self.pc += 3

    def alu(self, op, a, b):
        """ALU operations."""

        if op == "ADD":
            self.reg[a] += self.reg[b]
            self.pc += 3
        elif op == "SUB":
            self.reg[a] -= self.reg[b]
            self.pc += 3 
        elif op == "MUL":
            self.reg[a] = self.reg[a] * self.reg[b]
            self.pc += 3
        elif op == "CMP":
            if a == b:
                self.flag_reg[-1] = 1
            elif a > b:
                self.flag_reg[-2] = 1
            elif a < b:
                self.flag_reg[-3] = 1
            self.pc += 3
            print(self.flag_reg)
        elif op == "AND":
            self.reg[self.ram[self.pc+1]] = a & b
            self.pc += 3
        elif op == "OR":
            self.reg[self.ram[self.pc+1]] = a | b
            self.pc += 3
        elif op == "XOR":
            self.reg[self.ram[self.pc+1]] = a ^ b
            self.pc += 3
        elif op == "NOT":
            self.reg[self.ram[self.pc+1]] = ~a
            self.pc += 2
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
        self.load()

        while self.running:
            op_a = self.ram_read(self.pc+1)
            op_b = self.ram_read(self.pc+2)
            current_instruction = self.ram_read(self.pc)

            self.branch_table[current_instruction](op_a, op_b)


cpu = CPU()


cpu.run()
