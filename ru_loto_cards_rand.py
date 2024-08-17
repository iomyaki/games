import random
from ru_loto_cards_std import Loto_card


def get_random_card():
    def get_col_num(column):
        if column == 0:
            a, b = 1, 9
        elif column == 1:
            a, b = 10, 19
        elif column == 2:
            a, b = 20, 29
        elif column == 3:
            a, b = 30, 39
        elif column == 4:
            a, b = 40, 49
        elif column == 5:
            a, b = 50, 59
        elif column == 6:
            a, b = 60, 69
        elif column == 7:
            a, b = 70, 79
        else:  # column == 8
            a, b = 80, 90

        return random.randint(a, b)

    card_template = [[], [], []]
    card = Loto_card()
    used_numbers = []
    indices = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    # upper row indices

    random.shuffle(indices)

    upper_indices = indices[:5]

    # middle row indices

    middle_indices = [index for index in indices if index not in upper_indices]
    repeating_index = upper_indices[0]  # shuffle?
    print(repeating_index)
    middle_indices.append(repeating_index)

    # lower row indices

    random.shuffle(indices)

    lower_indices = indices[:5]

    if repeating_index in lower_indices:
        lower_indices.remove(repeating_index)
        lower_indices.append(indices[5])

    # shuffle indices

    del indices
    del repeating_index

    upper_indices.sort()
    middle_indices.sort()
    lower_indices.sort()

    row_indices = [upper_indices, middle_indices, lower_indices]
    random.shuffle(row_indices)

    # fill the card with numbers

    for i in range(3):
        for index in row_indices[i]:
            while True:
                number = get_col_num(index)
                if number not in used_numbers:
                    used_numbers.append(number)
                    card_template[i].append(number)
                    break

    card.upper, card.middle, card.lower = card_template[0], card_template[1], card_template[2]

    return card


example = get_random_card()
print(example.upper, example.middle, example.lower, sep='\n')
