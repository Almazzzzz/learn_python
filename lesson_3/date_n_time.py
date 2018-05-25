from datetime import datetime, date, timedelta


def working_with_fatetime():
    today = date.today()
    yesterday = today - timedelta(days=30)
    string = '01/01/17 12:10:03.234567'
    dt = datetime.strptime(string, '%d/%m/%y %H:%M:%S.%f')
    print(f'Today: {today}\n'
          f'Yesterday: {yesterday}\n'
          f'Datetime, converted form string: {dt}')


working_with_fatetime()
