people = ['Вася', 'Маша', 'Петя', 'Валера', 'Саша', 'Даша']


def find_person(name):
    return name == 'Валера'


while people:
    name = people.pop()
    if find_person(name):
        print('Валера нашелся!')
        break
else:
    print('Валера, ты где?')
