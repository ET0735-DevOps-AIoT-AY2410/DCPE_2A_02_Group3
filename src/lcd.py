import hal.hal_lcd as LCD
import main as main


lcd = LCD.lcd()
lcd.lcd_clear()


def display_item_details(item_name,item_cost,total_cost):
    #Display variables on lcd
    lcd.lcd_display_string(str(item_name), 1)
    lcd.lcd_display_string(" ".join([str(item_cost), " || ", str(total_cost)]) , 2)
    
    
if __name__=="__main__":
    display_item_details()
