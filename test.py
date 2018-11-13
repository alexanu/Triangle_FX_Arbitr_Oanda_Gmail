import pprint
# Cross currency arb
# If implied cross != cross, arb exists
# implied cross = A/B

# A/B x B/C x C/A = 1

start = 10000

wallet = {
  'EUR': 0,
  'USD': start,
  'GBP': 0
}

EUR_USD = 1.1246
EUR_GBP = 0.8750
GBP_USD = 1.2853

# 1) USD -> EUR (EUR_USD): Buy 
wallet['EUR'] = wallet['USD'] * (1 / EUR_USD)
wallet['USD'] = 0

# 2) EUR
wallet['GBP'] = wallet['EUR'] * (1 * EUR_GBP)
wallet['EUR'] = 0

# 3)
wallet['USD'] = wallet['GBP'] * (1 * GBP_USD)
wallet['GBP'] = 0


pprint.pprint(wallet)
print('Profit: $', wallet['USD'] - start)