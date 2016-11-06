import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

gameMap = {'28-9': False, '25-21': False, '7-14': False, '10-16': False, '13-14': False, '13-7': False, '5-17': False,
           '4-17': False, '10-17': False, '25-1': False, '18-3': False, '4-18': False, '27-9': False, '14-7': False,
           '17-15': False, '1-3': False, '9-15': False, '16-18': False, '11-8': False, '18-15': False, '11-19': False,
           '29-14': False, '14-11': False, '6-0': True, '5-18': False, '8-3': False, '23-1': False, '14-9': False,
           '21-14': True, '11-1': False, '22-18': False, '16-12': False, '15-6': False, '28-2': False, '2-7': False,
           '18-7': False, '29-21': False, '1-7': False, '8-8': False, '30-17': False, '17-9': False, '12-2': False,
           '0-4': True, '10-20': False, '5-0': True, '13-2': False, '31-19': False, '13-12': False, '27-14': False,
           '26-12': False, '10-7': False, '26-19': False, '12-21': False, '16-11': False, '18-13': False, '14-6': False,
           '10-2': False, '8-15': False, '9-20': False, '6-14': False, '9-10': False, '6-19': False, '18-20': False,
           '1-20': False, '30-6': False, '17-7': False, '10-21': False, '31-18': False, '6-3': False, '22-4': False,
           '21-8': True, '1-17': False, '28-8': False, '18-17': False, '6-11': False, '18-1': False, '2-5': False,
           '5-8': False, '6-12': False, '9-17': False, '17-11': False, '19-21': False, '2-3': False, '27-16': False,
           '4-10': False, '21-20': True, '1-21': False, '30-8': False, '31-3': False, '0-2': True, '25-16': False,
           '21-5': True, '3-3': False, '3-8': False, '6-16': False, '2-12': False, '31-0': True, '6-7': False,
           '15-11': False, '22-19': False, '2-2': False, '27-19': False, '20-2': False, '0-7': True, '13-3': False,
           '6-4': False, '7-15': False, '16-3': False, '4-9': False, '12-3': False, '24-3': False, '18-4': False,
           '20-13': False, '5-15': False, '28-17': False, '21-1': True, '0-1': True, '22-12': False, '31-7': False,
           '22-17': False, '16-1': False, '9-9': False, '14-19': False, '26-11': False, '19-15': False, '4-21': False,
           '3-7': False, '24-19': False, '30-11': False, '29-1': False, '24-20': False, '30-10': False, '28-4': False,
           '10-1': False, '6-15': False, '26-6': False, '1-15': False, '19-6': False, '12-12': False, '8-7': False,
           '13-9': False, '12-15': False, '0-5': True, '25-11': False, '22-9': False, '10-12': False, '27-7': False,
           '22-13': False, '0-14': True, '21-13': True, '0-6': True, '30-0': True, '6-8': False, '22-3': False,
           '31-2': False, '9-1': False, '31-13': False, '2-0': True, '27-21': False, '26-5': False, '31-5': False,
           '2-17': False, '17-13': False, '8-13': False, '2-15': False, '28-1': False, '26-21': False, '22-21': False,
           '19-5': False, '7-8': False, '31-4': False, '8-0': True, '31-9': False, '13-6': False, '5-21': False,
           '5-2': False, '15-21': False, '20-18': False, '28-3': False, '26-20': False, '16-20': False, '22-16': False,
           '17-16': False, '30-21': False, '22-11': False, '22-5': False, '12-10': False, '31-12': False, '2-19': False,
           '9-5': False, '3-18': False, '9-3': False, '5-14': False, '15-2': False, '11-15': False, '0-3': True,
           '14-10': False, '30-4': False, '10-13': False, '16-17': False, '0-9': True, '15-1': False, '24-18': False,
           '9-2': False, '7-5': False, '0-0': True, '12-19': False, '3-4': False, '12-16': False, '1-1': False,
           '7-21': False, '21-4': True, '25-17': False, '16-6': False, '20-9': False, '29-4': False, '1-10': False,
           '25-3': False, '14-21': False, '9-0': True, '28-15': False, '19-8': False, '24-16': False, '24-1': False,
           '7-1': False, '19-10': False, '11-4': False, '26-8': False, '24-9': False, '8-12': False, '2-20': False,
           '6-2': False, '16-16': False, '3-15': False, '8-18': False, '20-5': False, '13-15': False, '14-14': False,
           '19-12': False, '17-8': False, '28-21': False, '5-10': False, '8-6': False, '12-1': False, '0-16': True,
           '30-15': False, '3-2': False, '16-4': False, '5-9': False, '23-7': False, '17-2': False, '29-7': False,
           '15-14': False, '19-19': False, '26-2': False, '11-14': False, '20-11': False, '17-20': False, '6-9': False,
           '17-4': False, '9-13': False, '2-13': False, '15-12': False, '23-4': False, '25-18': False, '21-18': True,
           '30-19': False, '2-14': False, '11-5': False, '21-11': True, '20-3': False, '29-3': False, '18-14': False,
           '31-8': False, '22-20': False, '5-4': False, '1-0': True, '27-20': False, '0-15': True, '13-16': False,
           '10-9': False, '23-20': False, '21-0': True, '6-1': False, '17-18': False, '0-8': True, '27-10': False,
           '4-3': False, '23-9': False, '7-19': False, '13-8': False, '20-4': False, '9-14': False, '23-13': False,
           '20-15': False, '18-19': False, '23-15': False, '28-13': False, '8-5': False, '4-8': False, '19-17': False,
           '5-1': False, '0-12': True, '7-0': True, '10-19': False, '31-17': False, '22-14': False, '13-20': False,
           '24-6': False, '25-19': False, '13-5': False, '13-18': False, '14-3': False, '26-7': False, '21-16': True,
           '15-18': False, '9-19': False, '8-9': False, '29-19': False, '4-16': False, '6-17': False, '22-10': False,
           '27-2': False, '17-6': False, '12-13': False, '24-12': False, '8-14': False, '10-18': False, '30-20': False,
           '31-16': False, '30-1': False, '16-2': False, '21-3': True, '3-19': False, '14-13': False, '20-16': False,
           '15-15': False, '13-11': False, '3-17': False, '28-6': False, '28-19': False, '7-7': False, '7-9': False,
           '20-14': False, '29-0': True, '2-18': False, '23-6': False, '25-12': False, '22-15': False, '29-2': False,
           '15-10': False, '6-6': False, '29-15': False, '15-17': False, '3-11': False, '19-11': False, '28-12': False,
           '3-0': True, '3-20': False, '16-21': False, '20-21': False, '7-3': False, '2-1': False, '18-12': False,
           '8-2': False, '17-21': False, '1-14': False, '10-5': False, '1-4': False, '13-17': False, '3-1': False,
           '31-10': False, '12-4': False, '26-4': False, '21-21': True, '14-1': False, '4-19': False, '5-11': False,
           '18-10': False, '3-16': False, '27-11': False, '5-7': False, '21-19': True, '24-15': False, '11-18': False,
           '24-4': False, '26-10': False, '2-6': False, '8-20': False, '14-18': False, '4-11': False, '3-14': False,
           '30-16': False, '11-9': False, '3-6': False, '11-17': False, '30-2': False, '19-13': False, '22-7': False,
           '12-5': False, '17-10': False, '16-15': False, '12-6': False, '15-20': False, '29-16': False, '31-1': False,
           '1-6': False, '1-5': False, '19-9': False, '16-0': True, '1-9': False, '1-2': False, '25-7': False,
           '28-16': False, '16-10': False, '8-21': False, '30-14': False, '25-8': False, '26-16': False, '9-8': False,
           '2-8': False, '22-6': False, '23-17': False, '20-7': False, '7-13': False, '14-0': True, '6-10': False,
           '17-17': False, '18-6': False, '26-18': False, '18-8': False, '25-6': False, '22-2': False, '10-4': False,
           '5-6': False, '20-6': False, '11-20': False, '9-12': False, '19-1': False, '24-0': True, '13-10': False,
           '17-19': False, '10-3': False, '21-2': True, '15-16': False, '29-6': False, '16-13': False, '9-18': False,
           '11-11': False, '27-12': False, '25-0': True, '2-16': False, '18-11': False, '4-20': False, '25-20': False,
           '15-3': False, '1-8': False, '17-14': False, '24-7': False, '26-1': False, '18-16': False, '7-2': False,
           '29-8': False, '22-0': True, '25-5': False, '15-5': False, '27-1': False, '27-13': False, '1-11': False,
           '14-2': False, '27-17': False, '12-11': False, '19-20': False, '17-3': False, '11-10': False, '23-12': False,
           '30-12': False, '19-3': False, '30-18': False, '16-8': False, '20-10': False, '15-13': False, '14-20': False,
           '7-12': False, '8-16': False, '31-11': False, '23-2': False, '28-10': False, '1-18': False, '9-6': False,
           '0-19': True, '29-10': False, '14-16': False, '16-7': False, '23-11': False, '30-5': False, '10-15': False,
           '29-9': False, '16-14': False, '30-7': False, '0-17': True, '11-2': False, '9-16': False, '4-14': False,
           '15-7': False, '29-13': False, '16-19': False, '5-16': False, '23-16': False, '24-21': False, '30-13': False,
           '11-21': False, '27-4': False, '18-21': False, '11-3': False, '19-14': False, '11-12': False, '31-21': False,
           '7-17': False, '5-19': False, '8-1': False, '2-21': False, '24-11': False, '8-11': False, '30-3': False,
           '4-6': False, '24-17': False, '2-9': False, '28-18': False, '13-0': True, '14-4': False, '25-10': False,
           '26-0': True, '12-18': False, '10-0': True, '18-2': False, '10-8': False, '29-20': False, '6-18': False,
           '1-13': False, '27-3': False, '7-18': False, '24-14': False, '20-19': False, '5-5': False, '20-0': True,
           '26-9': False, '13-1': False, '1-19': False, '18-9': False, '31-14': False, '9-11': False, '10-10': False,
           '16-5': False, '8-17': False, '12-7': False, '7-6': False, '6-21': False, '5-20': False, '27-18': False,
           '15-4': False, '3-12': False, '4-12': False, '15-0': True, '4-1': False, '23-19': False, '14-17': False,
           '4-5': False, '1-12': False, '7-16': False, '31-20': False, '4-7': False, '13-19': False, '9-21': False,
           '28-11': False, '20-20': False, '13-13': False, '2-4': False, '11-13': False, '28-7': False, '26-15': False,
           '3-9': False, '14-5': False, '10-14': False, '27-8': False, '25-4': False, '28-5': False, '27-15': False,
           '31-6': False, '5-3': False, '21-10': True, '25-9': False, '8-19': False, '0-20': True, '15-9': False,
           '2-11': False, '9-7': False, '27-5': False, '21-9': True, '23-8': False, '21-7': True, '23-0': True,
           '0-10': True, '27-6': False, '23-21': False, '24-8': False, '31-15': False, '29-18': False, '14-15': False,
           '26-17': False, '0-13': True, '24-10': False, '14-8': False, '25-13': False, '7-11': False, '23-5': False,
           '25-14': False, '21-15': True, '23-10': False, '4-2': False, '21-17': True, '19-2': False, '9-4': False,
           '7-4': False, '5-13': False, '29-5': False, '0-21': True, '6-20': False, '6-13': False, '12-17': False,
           '17-12': False, '17-1': False, '17-0': True, '21-12': True, '10-11': False, '27-0': True, '4-4': False,
           '22-1': False, '18-0': True, '8-10': False, '23-3': False, '4-0': True, '26-14': False, '16-9': False,
           '24-5': False, '19-7': False, '3-21': False, '30-9': False, '13-21': False, '20-12': False, '3-10': False,
           '14-12': False, '4-13': False, '18-5': False, '18-18': False, '19-4': False, '21-6': True, '24-13': False,
           '2-10': False, '25-2': False, '20-8': False, '12-20': False, '12-8': False, '23-14': False, '29-17': False,
           '19-0': True, '0-11': True, '13-4': False, '15-19': False, '28-0': True, '28-20': False, '11-16': False,
           '17-5': False, '11-0': True, '23-18': False, '20-1': False, '19-18': False, '26-3': False, '11-6': False,
           '29-12': False, '22-8': False, '24-2': False, '8-4': False, '12-0': True, '12-9': False, '20-17': False,
           '25-15': False, '1-16': False, '15-8': False, '6-5': False, '4-15': False, '3-13': False, '10-6': False,
           '3-5': False, '7-20': False, '0-18': True, '19-16': False, '26-13': False, '7-10': False, '5-12': False,
           '11-7': False, '12-14': False, '29-11': False, '28-14': False}
action = {"UP", "LEFT", "DOWN", "RIGHT"}
myX = 0
myY = 0
# game loop
while True:
    # n: total number of players (2 to 4).
    # p: your player number (0 to 3).
    n, p = [int(i) for i in input().split()]
    for i in range(n):
        # x0: starting X coordinate of lightcycle (or -1)
        # y0: starting Y coordinate of lightcycle (or -1)
        # x1: starting X coordinate of lightcycle (can be the same as X0 if you play before this player)
        # y1: starting Y coordinate of lightcycle (can be the same as Y0 if you play before this player)
        x0, y0, x1, y1 = [int(j) for j in input().split()]
        gameMap[str(x1+1) + "-" + str(y1+1)] = True
        if p == i:
            myX = x1+1
            myY = y1+1

            # Write an action using print
            # To debug: print("Debug messages...", file=sys.stderr)
    if not gameMap[str(myX) + "-" + str(myY - 1)]:
        print("UP")
    elif not gameMap[str(myX - 1) + "-" + str(myY)]:
        print("LEFT")
    elif not gameMap[str(myX) + "-" + str(myY + 1)]:
        print("DOWN")
    elif not gameMap[str(myX + 1) + "-" + str(myY)]:
        print("RIGHT")
    else:
        print("UP")

    # A single line with UP, DOWN, LEFT or RIGHT
