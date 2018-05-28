def count_words_in_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
        words = content.split()
        count_words = len(words)
        print(f'Words in file: {count_words}')


count_words_in_file('data/referat.txt')
