def arb_calculator(obj, starting_balance, starting_currency):

    edge_pair = []
    mid_pair = ''

    # Get possible starting pairs based on starting_currency
    for key, value in obj.items():
        if starting_currency in key:
            edge_pair.append(key)
        else:
            mid_pair = key

    pairing_1 = (edge_pair[0], mid_pair, edge_pair[1])
    pairing_2 = (edge_pair[1], mid_pair, edge_pair[0])
    pairing_orders = [pairing_1, pairing_2]

    # To run both pairing order options
    for pairing in pairing_orders:

        balance = starting_balance
        currency = starting_currency

        for x in range(0, len(pairing)):

            base = pairing[x][:3]
            quote = pairing[x][4:]

            if base == currency:
                # We are buying base/quote at the ask price
                balance = balance * (1 * obj[pairing[x]]['ask'])
                currency = quote

            elif quote == currency:
                # We are selling base/quote at the bid price
                balance = balance * (1 / obj[pairing[x]]['bid'])
                currency = base

        profit = round(balance - starting_balance, 5)
        profit_margin = round((profit / balance) * 100, 5)

        if profit > 0:

            print('Arbitrage Detected')
            print('Trade in this order: {} for a profit of ${} {} ({} %)'.format(
                pairing, profit, currency, profit_margin))
            print('-------------------------------------------------------------------------------------------')

            result_object = {
                "steps": pairing,
                "profit": profit,
                "profit_margin": profit_margin,
                "currency": currency
            }
            return result_object