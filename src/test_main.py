import picam
import os
import main

def test_decode_barcode():
    fn = os.path.basename("qr_code_sample.jpg")
    actual_result = picam.decode_barcode(fn)
    expected_result = '38,120'

    assert (actual_result == expected_result)

def test_interfacing_with_bank():
    bank = main.import_bank_database()
    bank = bank[0]
    expected_result = {'UID': '567890123435', 'Card Num': '5678901234567890', 'Balance': '2000.0', 'Pin': '2373'}
    actual_result = main.interfacing_with_bank(bank,'567890123435')

    assert(expected_result == actual_result)

def test_update_balance():
    info = main.import_bank_database()
    bank = info[0]
    headers = info[1]
    expected_result = '6000'
    main.update_balance(headers,bank,'456789012335',6000)
    info = main.import_bank_database()
    bank = info[0]
    acc_info = main.interfacing_with_bank(bank,'456789012335')
    actual_result = acc_info['Balance']


    assert(expected_result == actual_result)




