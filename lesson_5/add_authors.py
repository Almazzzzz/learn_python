from db import db_session, User

authors = [
    {
        'first_name': 'Василий',
        'last_name': 'Петров',
        'email': 'vasya@example.com'
    },
    {
        'first_name': 'Маша',
        'last_name': 'Иванова',
        'email': 'mari@example.com'
    },
    {
        'first_name': 'Полуэкт',
        'last_name': 'Невструев',
        'email': 'p@example.com'
    }
]


for a in authors:
    author = User(a['first_name'], a['last_name'], a['email'])
    db_session.add(author)


db_session.commit()
