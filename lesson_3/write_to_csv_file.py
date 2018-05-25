import csv

person = {'name': 'Bob', 'age': 20, 'job': 'gardener', 'take him away!': True}


# Just for example
def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        fields = ['first_name', 'last_name', 'email', 'gender', 'balance']
        reader = csv.DictReader(f, fields, delimiter=';')
        for row in reader:
            print(row)


def write_to_file(file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        fieldsnames = ['param', 'value']
        writer = csv.DictWriter(f, fieldsnames, delimiter=';')
        writer.writeheader()
        for param in person:
            writer.writerow({'param': param, 'value': person[param]})

        print(f'Data was successfully writen to {file_name}')


write_to_file('bob.csv')
