import random
import string

def my_choice():
    keepRun=0
    my_choices = []

    while keepRun < 10:
        samp = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        samp2 = random.choice(['FR', 'SO', 'JR', 'SR', 'GR'])
        my_choices.append(((samp),(samp2)))
        keepRun += 1

    return tuple(my_choices)