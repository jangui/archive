#!/usr/bin/env python3
import code.basechanger as bc
import argparse
import sys

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(1)

def main():
    parser = MyParser(description="Change a number from one counting system (base) to another.")
    parser.add_argument("input_number", help="Desired number you wish to change base",type=str)
    parser.add_argument("input_base", help="What base is your input number in?",type=int)
    parser.add_argument("output_base", help="Desired base you wish to change the number to",type=int)
    args = parser.parse_args()

    answer = bc.nbase_change(input_number = args.input_number,
                            input_base = args.input_base, output_base = args.output_base)

    print("\n" + args.input_number + "(Base-" + str(args.input_base) +
             ") in Base-" + str(args.output_base) + " is: "+ str(answer))


if __name__ == "__main__":
    main()
