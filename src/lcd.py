import hal.hal_lcd as LCD
import main as main


lcd = LCD.lcd()
lcd.lcd_clear()


def display_item_details(item_name,item_cost,total_cost):
    #assign dummy values to functions
    item_name = "bobby"
    item_cost = 1.50
    total_cost = 10.50

    #Display variables on lcd
    lcd.lcd_display_string(" ".join([str(item_name), " || ", str(item_cost)]) , 1)
    lcd.lcd_display_string(str(total_cost), 2)
if __name__=="__main__":
    display_item_details()
