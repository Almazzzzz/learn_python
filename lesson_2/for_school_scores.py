school_scores = [{'school_class': '4a', 'scores': [3, 4, 4, 5, 2]},
                 {'school_class': '4b', 'scores': [2, 3, 5, 5, 5]},
                 {'school_class': '4c', 'scores': [5, 3, 3, 2, 4]}]


def get_average_class_scores():
    all_school_scores = []
    for school_class in school_scores:
        class_scores = school_class.get('scores')
        average_class_score = sum(class_scores) / len(class_scores)
        all_school_scores += class_scores
        print(f"Class '{school_class.get('school_class')}': \
            {average_class_score or 'No scores available'}")

    average_school_score = sum(all_school_scores) / len(all_school_scores)
    print(f"All school classes: {average_school_score}")


get_average_class_scores()
