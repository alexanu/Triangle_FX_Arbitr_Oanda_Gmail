from config import key, account_id
from ArbWrapper import ArbitrageWrapper
import pprint

starting_balance = 1000
starting_currency = 'USD'

arb = ArbitrageWrapper(starting_balance, starting_currency)

instruments = arb.get_all_instruments()
print(instruments)

triangles = arb.make_instrument_triangles(instruments)
print(triangles)

tri_w_starting_curr = arb.make_tri_w_starting_curr(triangles)
print(tri_w_starting_curr)

# Initializing results object
obj = {}

# Function to get price for all possible instrument pairs
for triangle in tri_w_starting_curr:

    # Initializing current triangle object
    obj[triangle] = {}

    # Fetch data for each instrument and add it to object
    for instrument in triangle:
        obj[triangle][instrument] = {}
        bid_rate = arb.get_instrument_rates(instrument)['bid']
        ask_rate = arb.get_instrument_rates(instrument)['ask']
        obj[triangle][instrument]['bid'] = bid_rate
        obj[triangle][instrument]['ask'] = ask_rate
    
    pprint.pprint(obj[triangle])

    # Calculate if arbitrage exist between the triangle
    arb.arb_calculator(obj[triangle])