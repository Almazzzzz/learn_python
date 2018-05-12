def get_vat(full_price, vat_rate):
    if full_price < 1 or not(vat_rate in range(1, 101)):
        return 'Error'
    vat = full_price / (100 + vat_rate) * vat_rate
    price_no_vat = full_price - vat + global_var
    return price_no_vat

global_var = 2
full_price = 118
vat_rate = 18
vat = get_vat(full_price, vat_rate)
print(vat)
