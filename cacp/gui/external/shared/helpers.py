def process_unique_names(names: list):
    new_names = names.copy()
    for x in set(new_names):
        number = 0
        for i in range(0, len(new_names)):
            if new_names[i] == x:
                number += 1
                if number >= 2:
                    new_names[i] += str(number)
    return new_names
