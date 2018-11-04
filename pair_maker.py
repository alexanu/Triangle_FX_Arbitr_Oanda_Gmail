from data_init import pair_data
import itertools

# Making a list of all instruments offered
instruments = []
for key, value in pair_data.items():
    instruments.append(key)


# Making a list of all instrument pairs (based on quoted currency)
first_pairs = []
for pair in itertools.combinations(instruments, 2):

    quote1 = pair[0][4:]

    if quote1 in pair[1]:
        first_pairs.append((pair[0], pair[1]))


# Adding the final instrument to the pairs to convert currency back to starting (based on the currency only in one pair and the starting currency)
pairs = []
for pair in first_pairs:
    currency1 = pair[0][:3]
    currency2 = pair[0][4:]
    currency3 = pair[1][:3]
    currency4 = pair[1][4:]

    currencies = [currency1, currency2]

    if currency3 not in currencies:
        currencies.append(currency3)

    elif currency4 not in currencies:
        currencies.append(currency4)

    for combo in itertools.combinations(currencies, 2):
        combo_str = combo[0] + '_' + combo[1]
        if combo_str not in pair and combo_str in instruments:
            pairs.append((pair[0], pair[1], combo_str))