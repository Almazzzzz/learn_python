school_scores = [{ 'school_class': '4a', 'scores': [3, 4, 4, 5, 2] },
    { 'school_class': '4b', 'scores': [2, 3, 5, 5, 5] },
    { 'school_class': '4c', 'scores': [5, 3, 3, 2, 4] }
]

def get_average_class_scores():
    average_class_scores = []
    for school_class in school_scores:
        class_scores = school_class.get('scores')
        if class_scores:
            average_class_score = sum(class_scores) / len(class_scores)
            average_class_scores.append(average_class_score)
        else:
            average_class_score = None

        print(f"Class '{school_class.get('school_class', 'Noname class')}': {average_class_score or 'No scores available'}")
    
    return average_class_scores

def get_average_school_score(average_class_scores):
    if average_class_scores:
        average_score = sum(average_class_scores) / len(average_class_scores)
    else:
        average_score = None
    print(f"All school classes: {average_score or 'No scores available'}")

average_class_scores = get_average_class_scores()
average_school_score = get_average_school_score(average_class_scores)
