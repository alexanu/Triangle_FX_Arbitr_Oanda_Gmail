import fxcmpy
import time
import datetime as dt

###### USER PARAMETERS ######
token = 'INSERT-TOKEN-HERE'
symbol = 'GBP/USD'
timeframe = "m1"	        # (m1,m5,m15,m30,H1,H2,H3,H4,H6,H8,D1,W1,M1)
#############################

# Global Variables
pricedata = None
numberofcandles = 300

# Connect to FXCM API
con = fxcmpy.fxcmpy(access_token=token, log_level="error")

# This function runs once at the beginning of the strategy to run initial one-time processes/computations
def Prepare():
    global pricedata

    print("Requesting Initial Price Data...")
    pricedata = con.get_candles(
        symbol, period=timeframe, number=numberofcandles)
    print(pricedata)
    print("Initial Price Data Received...")

# Get latest close bar prices and run Update() function every close of bar/candle
def StrategyHeartBeat():
    while True:
        currenttime = dt.datetime.now()
        if timeframe == "m1" and currenttime.second == 0 and GetLatestPriceData():
            Update()
        elif timeframe == "m5" and currenttime.second == 0 and currenttime.minute % 5 == 0 and GetLatestPriceData():
            Update()
            time.sleep(240)
        elif timeframe == "m15" and currenttime.second == 0 and currenttime.minute % 15 == 0 and GetLatestPriceData():
            Update()
            time.sleep(840)
        elif timeframe == "m30" and currenttime.second == 0 and currenttime.minute % 30 == 0 and GetLatestPriceData():
            Update()
            time.sleep(1740)
        elif currenttime.second == 0 and currenttime.minute == 0 and GetLatestPriceData():
            Update()
            time.sleep(3540)
        time.sleep(1)

# Returns True when pricedata is properly updated
def GetLatestPriceData():
    global pricedata

    # Normal operation will update pricedata on first attempt
    new_pricedata = con.get_candles(
        symbol, period=timeframe, number=numberofcandles)
    if new_pricedata.index.values[len(new_pricedata.index.values)-1] != pricedata.index.values[len(pricedata.index.values)-1]:
        pricedata = new_pricedata
        return True

    counter = 0
    # If data is not available on first attempt, try up to 3 times to update pricedata
    while new_pricedata.index.values[len(new_pricedata.index.values)-1] == pricedata.index.values[len(pricedata.index.values)-1] and counter < 3:
        print("No updated prices found, trying again in 10 seconds...")
        counter += 1
        time.sleep(10)
        new_pricedata = con.get_candles(
            symbol, period=timeframe, number=numberofcandles)
    if new_pricedata.index.values[len(new_pricedata.index.values)-1] != pricedata.index.values[len(pricedata.index.values)-1]:
        pricedata = new_pricedata
        return True
    else:
        return False

# This function is run every time a candle closes
def Update():
    print(str(dt.datetime.now()) + "	 " + timeframe +
          " Bar Closed - Running Update Function...")

    print("Close Price: " + str(pricedata['bidclose'][len(pricedata)-1]))

    print(str(dt.datetime.now()) + "	 " +
          timeframe + " Update Function Completed.\n")


Prepare()  # Initialize strategy
StrategyHeartBeat()  # Run strategy