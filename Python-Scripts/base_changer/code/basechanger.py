#!/usr/bin/env python3
import code.changebase as cb
import code.basechange as bc


def nbase_change(input_number, input_base, output_base):
	if input_base == 10:
		input_number = int(input_number)
		output_number = bc.base_change(input_number, output_base)
		return output_number

	elif output_base == 10:
		output_number = cb.change_base_n(input_number, input_base)
		return output_number

	else:
		base10 = cb.change_base_n(input_number, input_base)
		output_number = bc.base_change(base10, output_base)
		return output_number
#limit base 16, can be changed (increase the alphabet)
