from collections import defaultdict, deque
import numpy as np

def domain(friendship, work):
    team = deque([("President", ["Jhonatan"])])
    for place in work["President"]:
        team.append((place, friendship["Jhonatan"]))

    return team


def restriction(team, name):

    for place, domain in team:
        try:
            domain.remove(name)
        except:
            continue

def csp(friendship, work, team):
    #worker, position = team[0]
    #for places in work["President"]
    #    print(places, team)
    restriction(team, "Mike")


def main():
    friendship = {'Jhonatan': ['Mike', 'James', 'Emily', 'Tom', 'Amy'],
                  'Mike':     ['Jhonatan', 'Emily', 'Tom', 'Amy'],
                  'James':    ['Jhonatan', 'Mike', 'Emily', 'Amy'],
                  'Emily':    ['Jhonatan', 'Mike', 'James'],
                  'Tom':      ['Jhonatan', 'Mike', 'Emily', 'Amy'],
                  'Amy':      ['Jhonatan', 'James', 'Tom']}

    work = {'President':      ['Farming', 'Design', 'Manufacturing', 'Packing', 'Transportation'],
            'Farming':        ['President', 'Design', 'Transportation'],
            'Design':         ['President', 'Farming', 'Manufacturing'],
            'Manufacturing':  ['President', 'Design', 'Packing'],
            'Packing':        ['President', 'Manufacturing', 'Transportation'],
            'Transportation': ['President', 'Packing', 'Farming']}

    csp(friendship, work, domain(friendship, work))


if __name__ == "__main__":
    main()