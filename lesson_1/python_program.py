people = {
    'Alex': { 'city': 'Moscow', 'temperature': 23, 'wind': 34 },
    'Petya': { 'city': 'Orlando', 'temperature': 32, 'wind': 40 },
    'Petya': { 'city': 'Warsaw', 'temperature': 22, 'wind': 23 }
}
name = input('Ваше имя: ')
print(people.get(name, 'Not found'))
