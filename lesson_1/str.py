def get_summ(one, two, delimeter=' '):
    summ = str(one) + str(delimeter) + str(two).upper()
    return summ.upper()

summ = get_summ('qqq', 'www')
print(summ)
