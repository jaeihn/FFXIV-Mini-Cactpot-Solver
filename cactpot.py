import string
import itertools
from statistics import mode


positions = dict.fromkeys(string.ascii_lowercase[:9], 0)
numbers = dict.fromkeys(list(range(1,10)), False)
possibles = list(itertools.permutations(range(1,10)))

reward = {
    6: 10000,
    7: 36,
    8: 720,
    9: 360,
    10: 80,
    11: 252,
    12: 108,
    13: 72,
    14: 54,
    15: 180,
    16: 72,
    17: 180,
    18: 119,
    19: 36,
    20: 306,
    21: 1080,
    22: 144,
    23: 1800,
    24: 3600,
}

score = {
    0: [0, 3, 6],
    1: [0, 5], 
    2: [0, 7, 5],
    3: [1, 3], 
    4: [1, 4, 6, 7], 
    5: [1, 5],
    6: [2, 3], 
    7: [2, 4], 
    8: [2, 5, 6]
}

choices = {
    0: [0, 1, 2],
    1: [3, 4, 5],
    2: [6, 7, 8],
    3: [0, 3, 6],
    4: [1, 4, 7],
    5: [2, 5, 8],
    6: [0, 4, 8],
    7: [2, 4, 6],
}


def evaluate(state):
    choices = [
        state[0] + state[1] + state[2],
        state[3] + state[4] + state[5],
        state[6] + state[7] + state[8],
        state[0] + state[3] + state[6],
        state[1] + state[4] + state[7],
        state[2] + state[5] + state[8],
        state[0] + state[4] + state[8],
        state[2] + state[4] + state[6]
    ]
    return [reward[x] for x in choices]


def eliminate(possibles):
    state = tuple(positions.values())

    for i in range(9):
        if state[i]!=0:
            possibles = [x for x in possibles if x[i]==state[i]]
    return sorted(possibles, key=lambda x: max(evaluate(x)), reverse=True)


def printCard(mark):
    card = ''
    state = list(positions.values())

    for i in range(9):
        if i in mark:
            card+='*'
        elif state[i]==0:
            card+='_'
        else:
            card+= str(state[i])

    print('===========================')
    for i in range(0,3):
        print(*card[i*3:i*3+3], sep=' ')
    print('===========================')
    

def receive():
    while True:
        update = input('Enter number & position (e.g. 2a): ')
        if len(update)==2 and int(update[0]) in numbers and update[1] in positions:
            num = int(update[0])
            pos = update[1]

            if positions[pos]:
                print('Position already taken. Try again.\n')
                continue
            elif numbers[num]:
                print('Number already taken. Try again.\n')
                continue
            else:
                positions[pos] = num
                numbers[num] = True
                break
        else:
            print('Enter a valid input. \n')


def nextStep(possibles):
    expected = []
    mark = []
    bestcase = max(evaluate(possibles[0]))
    i = 0

    print(possibles[0])
    print(possibles[-1])
    while i < len(possibles):
        if max(evaluate(possibles[i]))==bestcase:
            expected.append(evaluate(possibles[i]).index(bestcase))
        else:
            break
        i += 1
    
    state = list(positions.values())
    empty = [x==0 for x in state]


    nextpos = [0]*9

    for row in [choices[x] for x in list(set(expected))]:
        for pos in row:
            if empty[pos]:
                mark.append(pos)

    for pos in range(9):
        known = [0]*8
        learn = [0]*8

        if not empty[pos] or pos in mark:
            for row in score[pos]:
                learn[row] += 1
        if not empty[pos]:
            for row in score[pos]:
                known[row] += 1
        nextpos[pos] = sum([learn[i]-known[i] for i in range(8)])

    mark = [x for x in mark if nextpos[x]==max(nextpos)]

    return mark



def bestChoice(possibles):

    payout = [0]*8
    for state in possibles:
        expected = evaluate(state)
        for i in range(8):
            payout[i] += expected[i]
    
    payout = [x/len(possibles) for x in payout]
    choice = payout.index(max(payout))
    print("Recommended row is", choice, "hoping for", max(payout))



for i in range(4):
    receive()
    possibles = eliminate(possibles)
    mark = nextStep(possibles)
    possibles = eliminate(possibles)
    printCard(mark)

possibles = eliminate(possibles)
bestChoice(possibles)
