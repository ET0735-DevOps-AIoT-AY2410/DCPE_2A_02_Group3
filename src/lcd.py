import hal.hal_lcd as LCD
import main as main
import time


lcd = LCD.lcd()
lcd.lcd_clear()


def display_item_details(item_name,item_cost,total_cost):
    #Display variables on lcd
    lcd.lcd_display_string(str(item_name), 1)
    time.sleep(1)
    lcd.lcd_clear()
    lcd.lcd_display_string("Item price:" + str(item_cost),1)
    lcd.lcd_display_string("Total price:" + str(total_cost), 2)

    return
    
if __name__=="__main__":
    display_item_details()
