def string_comparison(first_str, second_str):
    if first_str == second_str:
        return 1
    else:
        if second_str == 'learn':
            return 3
        elif len(first_str) > len(second_str):
            return 2


def input_strings():
    first_str = input('Enter the first string: ')
    second_str = input('Enter the second string: ')
    return first_str, second_str


first_str, second_str = input_strings()
result = string_comparison(first_str, second_str)
print(f'Result: {result}')
