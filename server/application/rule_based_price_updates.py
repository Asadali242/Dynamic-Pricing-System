import datetime
from services import manual_season_price_updater, manual_hour_price_updater

def hourly_update():
    print("Running manualHourlyPriceUpdate...")
    manual_hour_price_updater.manualHourlyPriceUpdate()
    print("manualHourlyPriceUpdate completed.") 

def seasonal_update():
    current_month = datetime.datetime.now().month
    if current_month == 12:  # December (Winter)
        print("Running manualSeasonalPriceUpdate...")
        manual_season_price_updater.manualSeasonalPriceUpdate('Winter')
        print("manualSeasonalPriceUpdate completed.") 
    elif current_month == 3:  # March (Spring)
        print("Running manualSeasonalPriceUpdate...")
        manual_season_price_updater.manualSeasonalPriceUpdate('Spring')
        print("manualSeasonalPriceUpdate completed.") 
    elif current_month == 6:  # June (Summer)
        print("Running manualSeasonalPriceUpdate...")
        manual_season_price_updater.manualSeasonalPriceUpdate('Summer')
        print("manualSeasonalPriceUpdate completed.") 
    elif current_month == 9:  # September (Fall)
        print("Running manualSeasonalPriceUpdate...")
        manual_season_price_updater.manualSeasonalPriceUpdate('Fall')
        print("manualSeasonalPriceUpdate completed.") 

#test to show scheduler works and calls functions every _
def new_minute_update():
    print("A minute has passed")