from config import key, account_id
from ArbWrapper import ArbitrageWrapper
import pprint

starting_balance = 1000
starting_currency = 'USD'

arb = ArbitrageWrapper(starting_balance, starting_currency)

# Initializing results object
obj = {}

pairs = arb.get_all_instruments()

combos = arb.make_instrument_combos(pairs)

start_currency_pairs = []

for pair in combos:
  for instrument in pair:
    if starting_currency in instrument and pair not in start_currency_pairs:
        start_currency_pairs.append(pair)

# Function to get price for all possible instrument pairs
for pair in start_currency_pairs:

    # Initializing current pair object
    obj[pair] = {}

    # Fetch data for each instrument and add it to object
    for instrument in pair:
        obj[pair][instrument] = {}
        bid_rate = arb.get_instrument_rates(instrument)['bid']
        ask_rate = arb.get_instrument_rates(instrument)['ask']
        obj[pair][instrument]['bid'] = bid_rate
        obj[pair][instrument]['ask'] = ask_rate
    
    pprint.pprint(obj[pair])

    # Calculate if arbitrage exist between the pairing
    arb.arb_calculator(obj[pair], starting_balance, starting_currency)