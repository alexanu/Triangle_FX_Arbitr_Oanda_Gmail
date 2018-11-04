from main import obj

def arb_calculator(obj, start_balance, start_currency):
  rates = []
  for instrument, rate in obj.items():
      rates.append((instrument, float(rate)) )

  # print(rates)
  # print('---------------------------------------------')

  # start_balance = 1000000
  # start_currency = 'USD'
  next_currency = ''
  last_currency = ''

  current_balance = 0
  current_currency = ''

  # Step 1: Convert starting currency into currency2
  for rate in rates:
      base = rate[0][:3]
      quoted = rate[0][4:]

      if base == start_currency:

          current_balance = rate[1] * start_balance
          current_currency = rate[0][4:]
          rates.remove(rate)
          break

  # print('Rates: ', rates)
  # print('Balance: ', current_balance, current_currency)
  # print('---------------------------------------------')

  # Step 2: Convert currency2 into currency3
  for rate in rates:
      base = rate[0][:3]
      quoted = rate[0][4:]

      if current_currency in rate[0] and start_currency not in rate[0]:
          
          if base == current_currency:

            current_balance = rate[1] * current_balance
            current_currency = quoted
            rates.remove(rate)
            break

          if quoted == current_currency:

            current_balance = current_balance / rate[1]
            current_currency = base
            rates.remove(rate)
            break

  # print('Rates: ', rates)
  # print('Balance: ', current_balance, current_currency)
  # print('---------------------------------------------')

  # Step 3: Convert currency 3 back into starting currency
  for rate in rates:
      base = rate[0][:3]
      quoted = rate[0][4:]

      if current_currency in rate[0] and start_currency in rate[0]:
          
          if base == current_currency:

            current_balance = rate[1] * current_balance
            current_currency = quoted
            rates.remove(rate)
            break

          if quoted == current_currency:

            current_balance = current_balance / rate[1]
            current_currency = base
            rates.remove(rate)
            break

  # print('Rates: ', rates)
  # print('Balance: ', current_balance, current_currency)
  # print('---------------------------------------------')


  profit = current_balance - start_balance
  # print('Profit: $', profit)

  return profit


for pear, rates in obj.items():
  print(pear, ': Profit = ', arb_calculator(rates, 10000, 'USD'))