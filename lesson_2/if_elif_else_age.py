def get_job(age):
    if age in range(0,7):
        job = 'Kindergarten'
    elif age in range(7,18):
        job = 'School'
    elif age in range(18,24):
        job = 'University'
    else:
        job = 'Try to get a job'
    return job

def input_age():
    while True:
        age = int(input('Enter your age: '))
        if age > 0:
            return age
        else:
            print('Wrong value. Try again.')

age = input_age()
job = get_job(age)
print(job)
