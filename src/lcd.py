from hal import hal_lcd as LCD
import main as main


lcd = LCD.lcd()
lcd.lcd_clear()


def display_item_details():
    #assign dummy values to functions
    item_name = "bobby"
    item_cost = 1.50
    total_cost = 10.50

    #Display variables on lcd
    lcd.lcd_display_string(item_name, " || ", item_cost , 1)
    lcd.lcd_display_string(total_cost, 2)
