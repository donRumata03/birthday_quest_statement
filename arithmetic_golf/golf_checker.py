# Compile and run the golfed code
# Check the output against the expected output
import os
import sys
import unittest
from random import randint
from os import environ
import unicodedata



def compile_golfed_code(filename) -> str:
    """ Compile C code into file .exe (for Windows) or .out (for Linux) """
    import os
    import subprocess

    # Wrap the code in a main function
    with open(filename, 'r') as f:
        code = f.read()

    changed_fname = filename + '.tmp.c'

    with open(changed_fname, 'w') as f:
        f.write(f"""#include <stdlib.h>
#include <string.h>
#include "stdio.h"
#include "stdint.h"

typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef uint64_t u64;

typedef int8_t i8;
typedef int16_t i16;
typedef int32_t i32;
typedef int64_t i64;


{code}

int main(int argc, char *argv[])
{{
   // Parse arguments
    u8 a = 0;
    u8 b = 0;
    char* operation = argv[1];
    if (strcmp(operation, "add") == 0)
    {{
        a = atoi(argv[2]);
        b = atoi(argv[3]);
        printf("%d", add(a, b));
    }}
    else if (strcmp(operation, "mul") == 0)
    {{
        a = atoi(argv[2]);
        b = atoi(argv[3]);
        printf("%d", mul(a, b));
    }}
    else if (strcmp(operation, "int_sqrt") == 0)
    {{
        a = atoi(argv[2]);
        printf("%d", int_sqrt(a));
    }}
    else
    {{
        printf("Usage: %s <a> <b>", argv[0]);
        return 1;
    }}
}}""")

    if sys.platform == 'win32':
        executable = 'a.exe'
    else:
        executable = 'a.out'

    if os.path.exists(executable):
        os.remove(executable)

    gcc = 'gcc.exe' if sys.platform == 'win32' else 'gcc'
    print(f'Compiling {changed_fname} with {gcc}...')
    subprocess.run([gcc, changed_fname, '-o', executable])
    return executable

def run_golfed_code(executable, operation, *args):
    """ Run the golfed code and return the output as int """
    import subprocess
    import os

    # Run the golfed code
    with open('golfed_output.txt', 'w') as f:
        subprocess.run([executable, operation, *args], stdout=f)
    with open('golfed_output.txt', 'r') as f:
        golfed_output = f.read()

    # Clean up
    os.remove('golfed_output.txt')
    return int(golfed_output)

class GolfChecker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.executable = compile_golfed_code(environ["GOLF_FILE"])
        pass

    def test_add_basic(self):
        self.assertEqual(run_golfed_code(self.executable, 'add', '11', '7'), 18)

    def test_mul_basic(self):
        self.assertEqual(run_golfed_code(self.executable, 'mul', '11', '7'), 77)

    def test_int_sqrt_basic(self):
        self.assertEqual(run_golfed_code(self.executable, 'int_sqrt', '100'), 10)

    def test_add_overflow(self):
        self.assertEqual(run_golfed_code(self.executable, 'add', '255', '1'), 0)

    def test_mul_overflow(self):
        self.assertEqual(run_golfed_code(self.executable, 'mul', '255', '2'), 254)

    def test_int_sqrt_rounding(self):
        self.assertEqual(run_golfed_code(self.executable, 'int_sqrt', '101'), 10)

    def test_int_sqrt_zero(self):
        self.assertEqual(run_golfed_code(self.executable, 'int_sqrt', '0'), 0)

    def test_int_sqrt_max(self):
        self.assertEqual(run_golfed_code(self.executable, 'int_sqrt', '255'), 15)


    def test_add_random(self):
        for _ in range(100):
            a = randint(0, 255)
            b = randint(0, 255)
            self.assertEqual(run_golfed_code(self.executable, 'add', str(a), str(b)), (a + b) % 256)

    def test_mul_random(self):
        for _ in range(100):
            a = randint(0, 255)
            b = randint(0, 255)
            self.assertEqual(run_golfed_code(self.executable, 'mul', str(a), str(b)), (a * b) % 256)

    def test_int_sqrt_random(self):
        for _ in range(100):
            a = randint(0, 255)
            self.assertEqual(run_golfed_code(self.executable, 'int_sqrt', str(a)), int(a ** 0.5), f'Failed for {a}')



if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        # Output size of code (chars) without space symbols
        with open(environ["GOLF_FILE"], 'r') as f:
            code = f.read()
        # Consider «space symbols» unicode category space separator
        code = ''.join([c for c in code if unicodedata.category(c) != 'Zs'])
        print(f'Code size: {len(code)} chars (without space symbols)')

        # Clean up
        if sys.platform == 'win32':
            executable = 'a.exe'
        else:
            executable = 'a.out'
        if os.path.exists(executable):
            os.remove(executable)

        if os.path.exists('golfed_output.txt'):
            os.remove('golfed_output.txt')

        if os.path.exists(environ["GOLF_FILE"] + '.tmp.c'):
            os.remove(environ["GOLF_FILE"] + '.tmp.c')
