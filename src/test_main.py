import picam
import os
import main
import keypad

def test_decode_barcode():
    fn = os.path.basename("barcode.jpg")
    actual_result = picam.decode_barcode(fn)
    expected_result = '38'

    assert (actual_result == expected_result)

def test_print_keypad_input():
    actual_result = keypad.print_keypad_input(1234)
    expected_result = 1234

    assert( actual_result == expected_result)

