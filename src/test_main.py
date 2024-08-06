import picam
import os
import main

def test_decode_barcode():
    fn = os.path.basename("barcode.jpg")
    actual_result = picam.decode_barcode(fn)
    expected_result = '38'

    assert (actual_result == expected_result)

def test_interfacing_with_bank():
    bank_database = main.import_bank_database()
    UID = 567890123435
    actual_result = main.interfacing_with_bank(bank_database , UID)
    
    expected_data = {'UID': [567890123435], 'Card Num': [5678901234567890], 'Balance': [2000.0], 'Pin': [2373]}
    expected_result = pd.DataFrame(expected_data)

    #reset index , prevent error of index 4 and 0
    expected_result = expected_result.reset_index(drop=True)
    actual_result = actual_result.reset_index(drop=True)
    
    # .equals used dataframe objects ( the value pandas returns) , cannot be compared , gives ambiguous error
    assert (actual_result.equals(expected_result))




