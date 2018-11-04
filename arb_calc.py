def arb_calculator(pairing_obj, start_balance, start_currency):
  
  # Initializing variables that will be used
  rates = []
  current_balance = 0
  current_currency = ''

  # Adding rate tuples to empty rates list
  for instrument, rate in pairing_obj.items():
      rates.append( (instrument, float(rate)) )


  # Step 1: Convert starting currency into currency 2
  for rate in rates:
      base = rate[0][:3]
      quoted = rate[0][4:]

      if base == start_currency:

          current_balance = rate[1] * start_balance
          current_currency = rate[0][4:]
          rates.remove(rate)
          break


  # Step 2: Convert currency 2 into currency 3
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


  profit = current_balance - start_balance
  return profit