from functools import wraps
import sys
import errno
import os
import signal

#recydled output, timeout function and neighbors chart

NEIGHBOURS = {(7, 3): [(8, 3), (6, 3), (7, 4), (7, 2)], (6, 9): [(7, 9), (5, 9), (6, 10), (6, 8)],
             (17, 11): [(18, 11), (16, 11), (17, 12), (17, 10)], (19, 19): [(20, 19), (18, 19), (19, 18)],
             (16, 6): [(17, 6), (15, 6), (16, 7), (16, 5)], (7, 12): [(8, 12), (6, 12), (7, 13), (7, 11)],
             (24, 5): [(25, 5), (23, 5), (24, 6), (24, 4)], (19, 4): [(20, 4), (18, 4), (19, 5), (19, 3)],
             (18, 4): [(19, 4), (17, 4), (18, 5), (18, 3)], (22, 19): [(23, 19), (21, 19), (22, 18)],
             (21, 9): [(22, 9), (20, 9), (21, 10), (21, 8)], (20, 7): [(21, 7), (19, 7), (20, 8), (20, 6)],
             (18, 19): [(19, 19), (17, 19), (18, 18)], (22, 6): [(23, 6), (21, 6), (22, 7), (22, 5)],
             (21, 6): [(22, 6), (20, 6), (21, 7), (21, 5)], (29, 7): [(28, 7), (29, 8), (29, 6)],
             (8, 5): [(9, 5), (7, 5), (8, 6), (8, 4)], (23, 7): [(24, 7), (22, 7), (23, 8), (23, 6)],
             (10, 8): [(11, 8), (9, 8), (10, 9), (10, 7)], (9, 0): [(10, 0), (8, 0), (9, 1)],
             (27, 9): [(28, 9), (26, 9), (27, 10), (27, 8)], (28, 19): [(29, 19), (27, 19), (28, 18)],
             (11, 5): [(12, 5), (10, 5), (11, 6), (11, 4)], (10, 7): [(11, 7), (9, 7), (10, 8), (10, 6)],
             (14, 18): [(15, 18), (13, 18), (14, 19), (14, 17)], (27, 10): [(28, 10), (26, 10), (27, 11), (27, 9)],
             (12, 6): [(13, 6), (11, 6), (12, 7), (12, 5)], (10, 18): [(11, 18), (9, 18), (10, 19), (10, 17)],
             (0, 17): [(1, 17), (0, 18), (0, 16)], (15, 11): [(16, 11), (14, 11), (15, 12), (15, 10)],
             (14, 1): [(15, 1), (13, 1), (14, 2), (14, 0)], (13, 7): [(14, 7), (12, 7), (13, 8), (13, 6)],
             (12, 17): [(13, 17), (11, 17), (12, 18), (12, 16)], (26, 17): [(27, 17), (25, 17), (26, 18), (26, 16)],
             (0, 4): [(1, 4), (0, 5), (0, 3)], (15, 4): [(16, 4), (14, 4), (15, 5), (15, 3)],
             (1, 1): [(2, 1), (0, 1), (1, 2), (1, 0)], (4, 10): [(5, 10), (3, 10), (4, 11), (4, 9)],
             (3, 2): [(4, 2), (2, 2), (3, 3), (3, 1)], (2, 6): [(3, 6), (1, 6), (2, 7), (2, 5)],
             (5, 11): [(6, 11), (4, 11), (5, 12), (5, 10)], (4, 5): [(5, 5), (3, 5), (4, 6), (4, 4)],
             (28, 10): [(29, 10), (27, 10), (28, 11), (28, 9)], (27, 5): [(28, 5), (26, 5), (27, 6), (27, 4)],
             (6, 0): [(7, 0), (5, 0), (6, 1)], (4, 16): [(5, 16), (3, 16), (4, 17), (4, 15)],
             (26, 7): [(27, 7), (25, 7), (26, 8), (26, 6)], (7, 5): [(8, 5), (6, 5), (7, 6), (7, 4)],
             (25, 12): [(26, 12), (24, 12), (25, 13), (25, 11)], (20, 19): [(21, 19), (19, 19), (20, 18)],
             (19, 13): [(20, 13), (18, 13), (19, 14), (19, 12)], (7, 0): [(8, 0), (6, 0), (7, 1)],
             (16, 19): [(17, 19), (15, 19), (16, 18)], (24, 4): [(25, 4), (23, 4), (24, 5), (24, 3)],
             (17, 7): [(18, 7), (16, 7), (17, 8), (17, 6)], (20, 14): [(21, 14), (19, 14), (20, 15), (20, 13)],
             (18, 10): [(19, 10), (17, 10), (18, 11), (18, 9)], (17, 18): [(18, 18), (16, 18), (17, 19), (17, 17)],
             (23, 19): [(24, 19), (22, 19), (23, 18)], (21, 15): [(22, 15), (20, 15), (21, 16), (21, 14)],
             (16, 8): [(17, 8), (15, 8), (16, 9), (16, 7)], (8, 12): [(9, 12), (7, 12), (8, 13), (8, 11)],
             (22, 12): [(23, 12), (21, 12), (22, 13), (22, 11)], (9, 9): [(10, 9), (8, 9), (9, 10), (9, 8)],
             (23, 9): [(24, 9), (22, 9), (23, 10), (23, 8)], (10, 14): [(11, 14), (9, 14), (10, 15), (10, 13)],
             (26, 3): [(27, 3), (25, 3), (26, 4), (26, 2)], (8, 18): [(9, 18), (7, 18), (8, 19), (8, 17)],
             (25, 0): [(26, 0), (24, 0), (25, 1)], (11, 15): [(12, 15), (10, 15), (11, 16), (11, 14)],
             (9, 19): [(10, 19), (8, 19), (9, 18)], (15, 16): [(16, 16), (14, 16), (15, 17), (15, 15)],
             (14, 8): [(15, 8), (13, 8), (14, 9), (14, 7)], (13, 0): [(14, 0), (12, 0), (13, 1)],
             (12, 8): [(13, 8), (11, 8), (12, 9), (12, 7)], (11, 16): [(12, 16), (10, 16), (11, 17), (11, 15)],
             (25, 16): [(26, 16), (24, 16), (25, 17), (25, 15)], (15, 13): [(16, 13), (14, 13), (15, 14), (15, 12)],
             (13, 13): [(14, 13), (12, 13), (13, 14), (13, 12)], (28, 16): [(29, 16), (27, 16), (28, 17), (28, 15)],
             (2, 18): [(3, 18), (1, 18), (2, 19), (2, 17)], (0, 14): [(1, 14), (0, 15), (0, 13)],
             (3, 11): [(4, 11), (2, 11), (3, 12), (3, 10)], (2, 1): [(3, 1), (1, 1), (2, 2), (2, 0)],
             (1, 15): [(2, 15), (0, 15), (1, 16), (1, 14)], (4, 12): [(5, 12), (3, 12), (4, 13), (4, 11)],
             (28, 1): [(29, 1), (27, 1), (28, 2), (28, 0)], (2, 12): [(3, 12), (1, 12), (2, 13), (2, 11)],
             (27, 14): [(28, 14), (26, 14), (27, 15), (27, 13)], (5, 1): [(6, 1), (4, 1), (5, 2), (5, 0)],
             (29, 4): [(28, 4), (29, 5), (29, 3)], (3, 17): [(4, 17), (2, 17), (3, 18), (3, 16)],
             (27, 2): [(28, 2), (26, 2), (27, 3), (27, 1)], (16, 7): [(17, 7), (15, 7), (16, 8), (16, 6)],
             (6, 14): [(7, 14), (5, 14), (6, 15), (6, 13)], (25, 9): [(26, 9), (24, 9), (25, 10), (25, 8)],
             (19, 18): [(20, 18), (18, 18), (19, 19), (19, 17)], (26, 6): [(27, 6), (25, 6), (26, 7), (26, 5)],
             (17, 6): [(18, 6), (16, 6), (17, 7), (17, 5)], (7, 15): [(8, 15), (6, 15), (7, 16), (7, 14)],
             (25, 13): [(26, 13), (24, 13), (25, 14), (25, 12)], (19, 7): [(20, 7), (18, 7), (19, 8), (19, 6)],
             (18, 5): [(19, 5), (17, 5), (18, 6), (18, 4)], (7, 1): [(8, 1), (6, 1), (7, 2), (7, 0)],
             (22, 16): [(23, 16), (21, 16), (22, 17), (22, 15)], (21, 8): [(22, 8), (20, 8), (21, 9), (21, 7)],
             (20, 0): [(21, 0), (19, 0), (20, 1)], (18, 16): [(19, 16), (17, 16), (18, 17), (18, 15)],
             (22, 7): [(23, 7), (21, 7), (22, 8), (22, 6)], (21, 5): [(22, 5), (20, 5), (21, 6), (21, 4)],
             (8, 6): [(9, 6), (7, 6), (8, 7), (8, 5)], (23, 6): [(24, 6), (22, 6), (23, 7), (23, 5)],
             (22, 10): [(23, 10), (21, 10), (22, 11), (22, 9)], (10, 9): [(11, 9), (9, 9), (10, 10), (10, 8)],
             (9, 7): [(10, 7), (8, 7), (9, 8), (9, 6)], (11, 4): [(12, 4), (10, 4), (11, 5), (11, 3)],
             (10, 4): [(11, 4), (9, 4), (10, 5), (10, 3)], (14, 19): [(15, 19), (13, 19), (14, 18)],
             (12, 7): [(13, 7), (11, 7), (12, 8), (12, 6)], (11, 9): [(12, 9), (10, 9), (11, 10), (11, 8)],
             (10, 19): [(11, 19), (9, 19), (10, 18)], (0, 18): [(1, 18), (0, 19), (0, 17)],
             (15, 10): [(16, 10), (14, 10), (15, 11), (15, 9)], (14, 6): [(15, 6), (13, 6), (14, 7), (14, 5)],
             (13, 6): [(14, 6), (12, 6), (13, 7), (13, 5)], (12, 18): [(13, 18), (11, 18), (12, 19), (12, 17)],
             (1, 19): [(2, 19), (0, 19), (1, 18)], (0, 5): [(1, 5), (0, 6), (0, 4)],
             (15, 7): [(16, 7), (14, 7), (15, 8), (15, 6)], (13, 19): [(14, 19), (12, 19), (13, 18)],
             (1, 0): [(2, 0), (0, 0), (1, 1)], (0, 8): [(1, 8), (0, 9), (0, 7)],
             (4, 11): [(5, 11), (3, 11), (4, 12), (4, 10)], (3, 5): [(4, 5), (2, 5), (3, 6), (3, 4)],
             (2, 7): [(3, 7), (1, 7), (2, 8), (2, 6)], (5, 10): [(6, 10), (4, 10), (5, 11), (5, 9)],
             (4, 6): [(5, 6), (3, 6), (4, 7), (4, 5)], (28, 11): [(29, 11), (27, 11), (28, 12), (28, 10)],
             (6, 1): [(7, 1), (5, 1), (6, 2), (6, 0)], (5, 7): [(6, 7), (4, 7), (5, 8), (5, 6)],
             (4, 17): [(5, 17), (3, 17), (4, 18), (4, 16)], (24, 1): [(25, 1), (23, 1), (24, 2), (24, 0)],
             (27, 6): [(28, 6), (26, 6), (27, 7), (27, 5)], (27, 3): [(28, 3), (26, 3), (27, 4), (27, 2)],
             (16, 1): [(17, 1), (15, 1), (16, 2), (16, 0)], (19, 12): [(20, 12), (18, 12), (19, 13), (19, 11)],
             (17, 12): [(18, 12), (16, 12), (17, 13), (17, 11)], (7, 17): [(8, 17), (6, 17), (7, 18), (7, 16)],
             (21, 17): [(22, 17), (20, 17), (21, 18), (21, 16)], (20, 15): [(21, 15), (19, 15), (20, 16), (20, 14)],
             (19, 1): [(20, 1), (18, 1), (19, 2), (19, 0)], (18, 11): [(19, 11), (17, 11), (18, 12), (18, 10)],
             (7, 6): [(8, 6), (6, 6), (7, 7), (7, 5)], (23, 18): [(24, 18), (22, 18), (23, 19), (23, 17)],
             (24, 2): [(25, 2), (23, 2), (24, 3), (24, 1)], (21, 14): [(22, 14), (20, 14), (21, 15), (21, 13)],
             (8, 13): [(9, 13), (7, 13), (8, 14), (8, 12)], (22, 13): [(23, 13), (21, 13), (22, 14), (22, 12)],
             (9, 8): [(10, 8), (8, 8), (9, 9), (9, 7)], (8, 0): [(9, 0), (7, 0), (8, 1)],
             (23, 8): [(24, 8), (22, 8), (23, 9), (23, 7)], (26, 13): [(27, 13), (25, 13), (26, 14), (26, 12)],
             (10, 15): [(11, 15), (9, 15), (10, 16), (10, 14)], (8, 19): [(9, 19), (7, 19), (8, 18)],
             (11, 14): [(12, 14), (10, 14), (11, 15), (11, 13)], (9, 18): [(10, 18), (8, 18), (9, 19), (9, 17)],
             (15, 19): [(16, 19), (14, 19), (15, 18)], (14, 9): [(15, 9), (13, 9), (14, 10), (14, 8)],
             (12, 9): [(13, 9), (11, 9), (12, 10), (12, 8)], (11, 19): [(12, 19), (10, 19), (11, 18)],
             (15, 12): [(16, 12), (14, 12), (15, 13), (15, 11)], (13, 12): [(14, 12), (12, 12), (13, 13), (13, 11)],
             (25, 3): [(26, 3), (24, 3), (25, 4), (25, 2)], (2, 19): [(3, 19), (1, 19), (2, 18)],
             (0, 15): [(1, 15), (0, 16), (0, 14)], (24, 14): [(25, 14), (23, 14), (24, 15), (24, 13)],
             (3, 10): [(4, 10), (2, 10), (3, 11), (3, 9)], (1, 14): [(2, 14), (0, 14), (1, 15), (1, 13)],
             (4, 13): [(5, 13), (3, 13), (4, 14), (4, 12)], (28, 2): [(29, 2), (27, 2), (28, 3), (28, 1)],
             (2, 13): [(3, 13), (1, 13), (2, 14), (2, 12)], (29, 16): [(28, 16), (29, 17), (29, 15)],
             (5, 0): [(6, 0), (4, 0), (5, 1)], (29, 3): [(28, 3), (29, 4), (29, 2)],
             (3, 16): [(4, 16), (2, 16), (3, 17), (3, 15)], (6, 15): [(7, 15), (5, 15), (6, 16), (6, 14)],
             (16, 9): [(17, 9), (15, 9), (16, 10), (16, 8)], (16, 10): [(17, 10), (15, 10), (16, 11), (16, 9)],
             (7, 14): [(8, 14), (6, 14), (7, 15), (7, 13)], (6, 18): [(7, 18), (5, 18), (6, 19), (6, 17)],
             (19, 6): [(20, 6), (18, 6), (19, 7), (19, 5)], (18, 2): [(19, 2), (17, 2), (18, 3), (18, 1)],
             (17, 10): [(18, 10), (16, 10), (17, 11), (17, 9)], (22, 17): [(23, 17), (21, 17), (22, 18), (22, 16)],
             (25, 15): [(26, 15), (24, 15), (25, 16), (25, 14)], (20, 1): [(21, 1), (19, 1), (20, 2), (20, 0)],
             (18, 17): [(19, 17), (17, 17), (18, 18), (18, 16)], (16, 2): [(17, 2), (15, 2), (16, 3), (16, 1)],
             (24, 15): [(25, 15), (23, 15), (24, 16), (24, 14)], (22, 4): [(23, 4), (21, 4), (22, 5), (22, 3)],
             (21, 4): [(22, 4), (20, 4), (21, 5), (21, 3)], (8, 7): [(9, 7), (7, 7), (8, 8), (8, 6)],
             (23, 1): [(24, 1), (22, 1), (23, 2), (23, 0)], (22, 11): [(23, 11), (21, 11), (22, 12), (22, 10)],
             (9, 6): [(10, 6), (8, 6), (9, 7), (9, 5)], (11, 7): [(12, 7), (10, 7), (11, 8), (11, 6)],
             (10, 5): [(11, 5), (9, 5), (10, 6), (10, 4)], (14, 16): [(15, 16), (13, 16), (14, 17), (14, 15)],
             (12, 0): [(13, 0), (11, 0), (12, 1)], (11, 8): [(12, 8), (10, 8), (11, 9), (11, 7)],
             (10, 16): [(11, 16), (9, 16), (10, 17), (10, 15)], (0, 19): [(1, 19), (0, 18)],
             (24, 16): [(25, 16), (23, 16), (24, 17), (24, 15)], (14, 7): [(15, 7), (13, 7), (14, 8), (14, 6)],
             (13, 5): [(14, 5), (12, 5), (13, 6), (13, 4)], (12, 19): [(13, 19), (11, 19), (12, 18)],
             (26, 12): [(27, 12), (25, 12), (26, 13), (26, 11)], (1, 18): [(2, 18), (0, 18), (1, 19), (1, 17)],
             (0, 6): [(1, 6), (0, 7), (0, 5)], (15, 6): [(16, 6), (14, 6), (15, 7), (15, 5)],
             (13, 18): [(14, 18), (12, 18), (13, 19), (13, 17)], (1, 7): [(2, 7), (0, 7), (1, 8), (1, 6)],
             (0, 9): [(1, 9), (0, 10), (0, 8)], (24, 13): [(25, 13), (23, 13), (24, 14), (24, 12)],
             (3, 4): [(4, 4), (2, 4), (3, 5), (3, 3)], (2, 4): [(3, 4), (1, 4), (2, 5), (2, 3)],
             (5, 9): [(6, 9), (4, 9), (5, 10), (5, 8)], (4, 7): [(5, 7), (3, 7), (4, 8), (4, 6)],
             (28, 4): [(29, 4), (27, 4), (28, 5), (28, 3)], (6, 6): [(7, 6), (5, 6), (6, 7), (6, 5)],
             (5, 6): [(6, 6), (4, 6), (5, 7), (5, 5)], (4, 18): [(5, 18), (3, 18), (4, 19), (4, 17)],
             (7, 7): [(8, 7), (6, 7), (7, 8), (7, 6)], (5, 19): [(6, 19), (4, 19), (5, 18)],
             (19, 15): [(20, 15), (18, 15), (19, 16), (19, 14)], (17, 3): [(18, 3), (16, 3), (17, 4), (17, 2)],
             (7, 16): [(8, 16), (6, 16), (7, 17), (7, 15)], (21, 16): [(22, 16), (20, 16), (21, 17), (21, 15)],
             (20, 8): [(21, 8), (19, 8), (20, 9), (20, 7)], (19, 0): [(20, 0), (18, 0), (19, 1)],
             (18, 8): [(19, 8), (17, 8), (18, 9), (18, 7)], (17, 16): [(18, 16), (16, 16), (17, 17), (17, 15)],
             (29, 18): [(28, 18), (29, 19), (29, 17)], (21, 13): [(22, 13), (20, 13), (21, 14), (21, 12)],
             (7, 4): [(8, 4), (6, 4), (7, 5), (7, 3)], (22, 2): [(23, 2), (21, 2), (22, 3), (22, 1)],
             (9, 15): [(10, 15), (8, 15), (9, 16), (9, 14)], (8, 1): [(9, 1), (7, 1), (8, 2), (8, 0)],
             (23, 11): [(24, 11), (22, 11), (23, 12), (23, 10)], (29, 8): [(28, 8), (29, 9), (29, 7)],
             (10, 12): [(11, 12), (9, 12), (10, 13), (10, 11)], (25, 8): [(26, 8), (24, 8), (25, 9), (25, 7)],
             (26, 1): [(27, 1), (25, 1), (26, 2), (26, 0)], (11, 1): [(12, 1), (10, 1), (11, 2), (11, 0)],
             (9, 17): [(10, 17), (8, 17), (9, 18), (9, 16)], (15, 18): [(16, 18), (14, 18), (15, 19), (15, 17)],
             (14, 14): [(15, 14), (13, 14), (14, 15), (14, 13)], (12, 10): [(13, 10), (11, 10), (12, 11), (12, 9)],
             (11, 18): [(12, 18), (10, 18), (11, 19), (11, 17)], (15, 15): [(16, 15), (14, 15), (15, 16), (15, 14)],
             (13, 11): [(14, 11), (12, 11), (13, 12), (13, 10)], (2, 16): [(3, 16), (1, 16), (2, 17), (2, 15)],
             (0, 0): [(1, 0), (0, 1)], (8, 14): [(9, 14), (7, 14), (8, 15), (8, 13)],
             (1, 13): [(2, 13), (0, 13), (1, 14), (1, 12)], (24, 12): [(25, 12), (23, 12), (24, 13), (24, 11)],
             (4, 14): [(5, 14), (3, 14), (4, 15), (4, 13)], (28, 3): [(29, 3), (27, 3), (28, 4), (28, 2)],
             (2, 10): [(3, 10), (1, 10), (2, 11), (2, 9)], (5, 15): [(6, 15), (4, 15), (5, 16), (5, 14)],
             (29, 2): [(28, 2), (29, 3), (29, 1)], (3, 19): [(4, 19), (2, 19), (3, 18)],
             (6, 12): [(7, 12), (5, 12), (6, 13), (6, 11)], (29, 11): [(28, 11), (29, 12), (29, 10)],
             (27, 17): [(28, 17), (26, 17), (27, 18), (27, 16)], (17, 4): [(18, 4), (16, 4), (17, 5), (17, 3)],
             (16, 12): [(17, 12), (15, 12), (16, 13), (16, 11)], (6, 19): [(7, 19), (5, 19), (6, 18)],
             (19, 9): [(20, 9), (18, 9), (19, 10), (19, 8)], (18, 3): [(19, 3), (17, 3), (18, 4), (18, 2)],
             (17, 9): [(18, 9), (16, 9), (17, 10), (17, 8)], (20, 2): [(21, 2), (19, 2), (20, 3), (20, 1)],
             (18, 14): [(19, 14), (17, 14), (18, 15), (18, 13)], (22, 5): [(23, 5), (21, 5), (22, 6), (22, 4)],
             (17, 17): [(18, 17), (16, 17), (17, 18), (17, 16)], (16, 0): [(17, 0), (15, 0), (16, 1)],
             (23, 0): [(24, 0), (22, 0), (23, 1)], (22, 8): [(23, 8), (21, 8), (22, 9), (22, 7)],
             (16, 15): [(17, 15), (15, 15), (16, 16), (16, 14)], (9, 5): [(10, 5), (8, 5), (9, 6), (9, 4)],
             (23, 13): [(24, 13), (22, 13), (23, 14), (23, 12)], (24, 7): [(25, 7), (23, 7), (24, 8), (24, 6)],
             (11, 6): [(12, 6), (10, 6), (11, 7), (11, 5)], (10, 2): [(11, 2), (9, 2), (10, 3), (10, 1)],
             (14, 17): [(15, 17), (13, 17), (14, 18), (14, 16)], (12, 1): [(13, 1), (11, 1), (12, 2), (12, 0)],
             (11, 11): [(12, 11), (10, 11), (11, 12), (11, 10)], (10, 17): [(11, 17), (9, 17), (10, 18), (10, 16)],
             (28, 18): [(29, 18), (27, 18), (28, 19), (28, 17)], (24, 17): [(25, 17), (23, 17), (24, 18), (24, 16)],
             (14, 4): [(15, 4), (13, 4), (14, 5), (14, 3)], (13, 4): [(14, 4), (12, 4), (13, 5), (13, 3)],
             (12, 12): [(13, 12), (11, 12), (12, 13), (12, 11)], (1, 17): [(2, 17), (0, 17), (1, 18), (1, 16)],
             (0, 7): [(1, 7), (0, 8), (0, 6)], (15, 1): [(16, 1), (14, 1), (15, 2), (15, 0)],
             (13, 17): [(14, 17), (12, 17), (13, 18), (13, 16)], (26, 14): [(27, 14), (25, 14), (26, 15), (26, 13)],
             (1, 6): [(2, 6), (0, 6), (1, 7), (1, 5)], (0, 10): [(1, 10), (0, 11), (0, 9)],
             (17, 13): [(18, 13), (16, 13), (17, 14), (17, 12)], (27, 0): [(28, 0), (26, 0), (27, 1)],
             (3, 7): [(4, 7), (2, 7), (3, 8), (3, 6)], (2, 5): [(3, 5), (1, 5), (2, 6), (2, 4)],
             (1, 11): [(2, 11), (0, 11), (1, 12), (1, 10)], (24, 11): [(25, 11), (23, 11), (24, 12), (24, 10)],
             (5, 8): [(6, 8), (4, 8), (5, 9), (5, 7)], (4, 0): [(5, 0), (3, 0), (4, 1)],
             (28, 5): [(29, 5), (27, 5), (28, 6), (28, 4)], (6, 7): [(7, 7), (5, 7), (6, 8), (6, 6)],
             (5, 5): [(6, 5), (4, 5), (5, 6), (5, 4)], (4, 19): [(5, 19), (3, 19), (4, 18)],
             (21, 18): [(22, 18), (20, 18), (21, 19), (21, 17)], (16, 3): [(17, 3), (15, 3), (16, 4), (16, 2)],
             (6, 10): [(7, 10), (5, 10), (6, 11), (6, 9)], (5, 18): [(6, 18), (4, 18), (5, 19), (5, 17)],
             (19, 14): [(20, 14), (18, 14), (19, 15), (19, 13)], (17, 2): [(18, 2), (16, 2), (17, 3), (17, 1)],
             (7, 19): [(8, 19), (6, 19), (7, 18)], (20, 9): [(21, 9), (19, 9), (20, 10), (20, 8)],
             (19, 3): [(20, 3), (18, 3), (19, 4), (19, 2)], (18, 9): [(19, 9), (17, 9), (18, 10), (18, 8)],
             (27, 15): [(28, 15), (26, 15), (27, 16), (27, 14)], (21, 12): [(22, 12), (20, 12), (21, 13), (21, 11)],
             (20, 4): [(21, 4), (19, 4), (20, 5), (20, 3)], (8, 15): [(9, 15), (7, 15), (8, 16), (8, 14)],
             (22, 3): [(23, 3), (21, 3), (22, 4), (22, 2)], (25, 10): [(26, 10), (24, 10), (25, 11), (25, 9)],
             (9, 14): [(10, 14), (8, 14), (9, 15), (9, 13)], (8, 2): [(9, 2), (7, 2), (8, 3), (8, 1)],
             (23, 10): [(24, 10), (22, 10), (23, 11), (23, 9)], (10, 13): [(11, 13), (9, 13), (10, 14), (10, 12)],
             (9, 3): [(10, 3), (8, 3), (9, 4), (9, 2)], (11, 0): [(12, 0), (10, 0), (11, 1)],
             (9, 16): [(10, 16), (8, 16), (9, 17), (9, 15)], (14, 15): [(15, 15), (13, 15), (14, 16), (14, 14)],
             (12, 11): [(13, 11), (11, 11), (12, 12), (12, 10)], (28, 17): [(29, 17), (27, 17), (28, 18), (28, 16)],
             (15, 14): [(16, 14), (14, 14), (15, 15), (15, 13)], (14, 2): [(15, 2), (13, 2), (14, 3), (14, 1)],
             (13, 10): [(14, 10), (12, 10), (13, 11), (13, 9)], (2, 17): [(3, 17), (1, 17), (2, 18), (2, 16)],
             (26, 18): [(27, 18), (25, 18), (26, 19), (26, 17)], (0, 1): [(1, 1), (0, 2), (0, 0)],
             (3, 12): [(4, 12), (2, 12), (3, 13), (3, 11)], (25, 19): [(26, 19), (24, 19), (25, 18)],
             (1, 12): [(2, 12), (0, 12), (1, 13), (1, 11)], (29, 9): [(28, 9), (29, 10), (29, 8)],
             (4, 15): [(5, 15), (3, 15), (4, 16), (4, 14)], (3, 1): [(4, 1), (2, 1), (3, 2), (3, 0)],
             (2, 11): [(3, 11), (1, 11), (2, 12), (2, 10)], (24, 6): [(25, 6), (23, 6), (24, 7), (24, 5)],
             (24, 10): [(25, 10), (23, 10), (24, 11), (24, 9)], (5, 14): [(6, 14), (4, 14), (5, 15), (5, 13)],
             (29, 1): [(28, 1), (29, 2), (29, 0)], (3, 18): [(4, 18), (2, 18), (3, 19), (3, 17)],
             (6, 13): [(7, 13), (5, 13), (6, 14), (6, 12)], (29, 14): [(28, 14), (29, 15), (29, 13)],
             (7, 8): [(8, 8), (6, 8), (7, 9), (7, 7)], (6, 16): [(7, 16), (5, 16), (6, 17), (6, 15)],
             (20, 16): [(21, 16), (19, 16), (20, 17), (20, 15)], (19, 8): [(20, 8), (18, 8), (19, 9), (19, 7)],
             (18, 0): [(19, 0), (17, 0), (18, 1)], (17, 8): [(18, 8), (16, 8), (17, 9), (17, 7)],
             (16, 16): [(17, 16), (15, 16), (16, 17), (16, 15)], (20, 3): [(21, 3), (19, 3), (20, 4), (20, 2)],
             (18, 15): [(19, 15), (17, 15), (18, 16), (18, 14)], (27, 12): [(28, 12), (26, 12), (27, 13), (27, 11)],
             (21, 2): [(22, 2), (20, 2), (21, 3), (21, 1)], (8, 9): [(9, 9), (7, 9), (8, 10), (8, 8)],
             (23, 3): [(24, 3), (22, 3), (23, 4), (23, 2)], (22, 9): [(23, 9), (21, 9), (22, 10), (22, 8)],
             (25, 11): [(26, 11), (24, 11), (25, 12), (25, 10)], (9, 4): [(10, 4), (8, 4), (9, 5), (9, 3)],
             (7, 11): [(8, 11), (6, 11), (7, 12), (7, 10)], (23, 12): [(24, 12), (22, 12), (23, 13), (23, 11)],
             (10, 3): [(11, 3), (9, 3), (10, 4), (10, 2)], (24, 3): [(25, 3), (23, 3), (24, 4), (24, 2)],
             (12, 2): [(13, 2), (11, 2), (12, 3), (12, 1)], (11, 10): [(12, 10), (10, 10), (11, 11), (11, 9)],
             (29, 17): [(28, 17), (29, 18), (29, 16)], (29, 10): [(28, 10), (29, 11), (29, 9)],
             (24, 18): [(25, 18), (23, 18), (24, 19), (24, 17)], (14, 5): [(15, 5), (13, 5), (14, 6), (14, 4)],
             (13, 3): [(14, 3), (12, 3), (13, 4), (13, 2)], (12, 13): [(13, 13), (11, 13), (12, 14), (12, 12)],
             (1, 16): [(2, 16), (0, 16), (1, 17), (1, 15)], (3, 13): [(4, 13), (2, 13), (3, 14), (3, 12)],
             (15, 0): [(16, 0), (14, 0), (15, 1)], (28, 15): [(29, 15), (27, 15), (28, 16), (28, 14)],
             (13, 16): [(14, 16), (12, 16), (13, 17), (13, 15)], (25, 2): [(26, 2), (24, 2), (25, 3), (25, 1)],
             (1, 5): [(2, 5), (0, 5), (1, 6), (1, 4)], (0, 11): [(1, 11), (0, 12), (0, 10)],
             (27, 16): [(28, 16), (26, 16), (27, 17), (27, 15)], (3, 6): [(4, 6), (2, 6), (3, 7), (3, 5)],
             (2, 2): [(3, 2), (1, 2), (2, 3), (2, 1)], (1, 10): [(2, 10), (0, 10), (1, 11), (1, 9)],
             (4, 1): [(5, 1), (3, 1), (4, 2), (4, 0)], (28, 6): [(29, 6), (27, 6), (28, 7), (28, 5)],
             (26, 11): [(27, 11), (25, 11), (26, 12), (26, 10)], (6, 4): [(7, 4), (5, 4), (6, 5), (6, 3)],
             (5, 4): [(6, 4), (4, 4), (5, 5), (5, 3)], (26, 10): [(27, 10), (25, 10), (26, 11), (26, 9)],
             (25, 14): [(26, 14), (24, 14), (25, 15), (25, 13)], (16, 4): [(17, 4), (15, 4), (16, 5), (16, 3)],
             (6, 11): [(7, 11), (5, 11), (6, 12), (6, 10)], (5, 17): [(6, 17), (4, 17), (5, 18), (5, 16)],
             (19, 17): [(20, 17), (18, 17), (19, 18), (19, 16)], (25, 1): [(26, 1), (24, 1), (25, 2), (25, 0)],
             (17, 1): [(18, 1), (16, 1), (17, 2), (17, 0)], (7, 18): [(8, 18), (6, 18), (7, 19), (7, 17)],
             (20, 10): [(21, 10), (19, 10), (20, 11), (20, 9)], (19, 2): [(20, 2), (18, 2), (19, 3), (19, 1)],
             (18, 6): [(19, 6), (17, 6), (18, 7), (18, 5)], (24, 8): [(25, 8), (23, 8), (24, 9), (24, 7)],
             (21, 11): [(22, 11), (20, 11), (21, 12), (21, 10)], (20, 5): [(21, 5), (19, 5), (20, 6), (20, 4)],
             (27, 13): [(28, 13), (26, 13), (27, 14), (27, 12)], (22, 0): [(23, 0), (21, 0), (22, 1)],
             (9, 13): [(10, 13), (8, 13), (9, 14), (9, 12)], (8, 3): [(9, 3), (7, 3), (8, 4), (8, 2)],
             (23, 5): [(24, 5), (22, 5), (23, 6), (23, 4)], (25, 4): [(26, 4), (24, 4), (25, 5), (25, 3)],
             (10, 10): [(11, 10), (9, 10), (10, 11), (10, 9)], (9, 2): [(10, 2), (8, 2), (9, 3), (9, 1)],
             (16, 13): [(17, 13), (15, 13), (16, 14), (16, 12)], (27, 11): [(28, 11), (26, 11), (27, 12), (27, 10)],
             (11, 3): [(12, 3), (10, 3), (11, 4), (11, 2)], (14, 12): [(15, 12), (13, 12), (14, 13), (14, 11)],
             (12, 4): [(13, 4), (11, 4), (12, 5), (12, 3)], (15, 9): [(16, 9), (14, 9), (15, 10), (15, 8)],
             (14, 3): [(15, 3), (13, 3), (14, 4), (14, 2)], (13, 9): [(14, 9), (12, 9), (13, 10), (13, 8)],
             (26, 19): [(27, 19), (25, 19), (26, 18)], (0, 2): [(1, 2), (0, 3), (0, 1)],
             (28, 14): [(29, 14), (27, 14), (28, 15), (28, 13)], (3, 15): [(4, 15), (2, 15), (3, 16), (3, 14)],
             (1, 3): [(2, 3), (0, 3), (1, 4), (1, 2)], (4, 8): [(5, 8), (3, 8), (4, 9), (4, 7)],
             (3, 0): [(4, 0), (2, 0), (3, 1)], (2, 8): [(3, 8), (1, 8), (2, 9), (2, 7)],
             (5, 13): [(6, 13), (4, 13), (5, 14), (5, 12)], (29, 0): [(28, 0), (29, 1)],
             (28, 8): [(29, 8), (27, 8), (28, 9), (28, 7)], (29, 19): [(28, 19), (29, 18)],
             (6, 2): [(7, 2), (5, 2), (6, 3), (6, 1)], (29, 13): [(28, 13), (29, 14), (29, 12)],
             (16, 14): [(17, 14), (15, 14), (16, 15), (16, 13)], (6, 17): [(7, 17), (5, 17), (6, 18), (6, 16)],
             (20, 17): [(21, 17), (19, 17), (20, 18), (20, 16)], (19, 11): [(20, 11), (18, 11), (19, 12), (19, 10)],
             (18, 1): [(19, 1), (17, 1), (18, 2), (18, 0)], (17, 15): [(18, 15), (16, 15), (17, 16), (17, 14)],
             (16, 17): [(17, 17), (15, 17), (16, 18), (16, 16)], (27, 1): [(28, 1), (26, 1), (27, 2), (27, 0)],
             (20, 12): [(21, 12), (19, 12), (20, 13), (20, 11)], (18, 12): [(19, 12), (17, 12), (18, 13), (18, 11)],
             (23, 17): [(24, 17), (22, 17), (23, 18), (23, 16)], (21, 1): [(22, 1), (20, 1), (21, 2), (21, 0)],
             (26, 2): [(27, 2), (25, 2), (26, 3), (26, 1)], (24, 0): [(25, 0), (23, 0), (24, 1)],
             (8, 10): [(9, 10), (7, 10), (8, 11), (8, 9)], (23, 2): [(24, 2), (22, 2), (23, 3), (23, 1)],
             (22, 14): [(23, 14), (21, 14), (22, 15), (22, 13)], (9, 11): [(10, 11), (8, 11), (9, 12), (9, 10)],
             (23, 15): [(24, 15), (22, 15), (23, 16), (23, 14)], (25, 5): [(26, 5), (24, 5), (25, 6), (25, 4)],
             (10, 0): [(11, 0), (9, 0), (10, 1)], (8, 16): [(9, 16), (7, 16), (8, 17), (8, 15)],
             (12, 3): [(13, 3), (11, 3), (12, 4), (12, 2)], (11, 13): [(12, 13), (10, 13), (11, 14), (11, 12)],
             (24, 19): [(25, 19), (23, 19), (24, 18)], (14, 10): [(15, 10), (13, 10), (14, 11), (14, 9)],
             (13, 2): [(14, 2), (12, 2), (13, 3), (13, 1)], (12, 14): [(13, 14), (11, 14), (12, 15), (12, 13)],
             (25, 18): [(26, 18), (24, 18), (25, 19), (25, 17)], (15, 3): [(16, 3), (14, 3), (15, 4), (15, 2)],
             (13, 15): [(14, 15), (12, 15), (13, 16), (13, 14)], (27, 19): [(28, 19), (26, 19), (27, 18)],
             (1, 4): [(2, 4), (0, 4), (1, 5), (1, 3)], (0, 12): [(1, 12), (0, 13), (0, 11)],
             (28, 13): [(29, 13), (27, 13), (28, 14), (28, 12)], (3, 9): [(4, 9), (2, 9), (3, 10), (3, 8)],
             (2, 3): [(3, 3), (1, 3), (2, 4), (2, 2)], (1, 9): [(2, 9), (0, 9), (1, 10), (1, 8)],
             (4, 2): [(5, 2), (3, 2), (4, 3), (4, 1)], (28, 7): [(29, 7), (27, 7), (28, 8), (28, 6)],
             (2, 14): [(3, 14), (1, 14), (2, 15), (2, 13)], (6, 5): [(7, 5), (5, 5), (6, 6), (6, 4)],
             (5, 3): [(6, 3), (4, 3), (5, 4), (5, 2)], (29, 6): [(28, 6), (29, 7), (29, 5)],
             (26, 15): [(27, 15), (25, 15), (26, 16), (26, 14)], (16, 5): [(17, 5), (15, 5), (16, 6), (16, 4)],
             (6, 8): [(7, 8), (5, 8), (6, 9), (6, 7)], (5, 16): [(6, 16), (4, 16), (5, 17), (5, 15)],
             (19, 16): [(20, 16), (18, 16), (19, 17), (19, 15)], (17, 0): [(18, 0), (16, 0), (17, 1)],
             (7, 13): [(8, 13), (6, 13), (7, 14), (7, 12)], (20, 11): [(21, 11), (19, 11), (20, 12), (20, 10)],
             (19, 5): [(20, 5), (18, 5), (19, 6), (19, 4)], (18, 7): [(19, 7), (17, 7), (18, 8), (18, 6)],
             (22, 18): [(23, 18), (21, 18), (22, 19), (22, 17)], (21, 10): [(22, 10), (20, 10), (21, 11), (21, 9)],
             (20, 6): [(21, 6), (19, 6), (20, 7), (20, 5)], (7, 9): [(8, 9), (6, 9), (7, 10), (7, 8)],
             (18, 18): [(19, 18), (17, 18), (18, 19), (18, 17)], (22, 1): [(23, 1), (21, 1), (22, 2), (22, 0)],
             (21, 7): [(22, 7), (20, 7), (21, 8), (21, 6)], (9, 12): [(10, 12), (8, 12), (9, 13), (9, 11)],
             (8, 4): [(9, 4), (7, 4), (8, 5), (8, 3)], (23, 4): [(24, 4), (22, 4), (23, 5), (23, 3)],
             (26, 0): [(27, 0), (25, 0), (26, 1)], (10, 11): [(11, 11), (9, 11), (10, 12), (10, 10)],
             (9, 1): [(10, 1), (8, 1), (9, 2), (9, 0)], (17, 5): [(18, 5), (16, 5), (17, 6), (17, 4)],
             (25, 6): [(26, 6), (24, 6), (25, 7), (25, 5)], (11, 2): [(12, 2), (10, 2), (11, 3), (11, 1)],
             (10, 6): [(11, 6), (9, 6), (10, 7), (10, 5)], (16, 11): [(17, 11), (15, 11), (16, 12), (16, 10)],
             (14, 13): [(15, 13), (13, 13), (14, 14), (14, 12)], (12, 5): [(13, 5), (11, 5), (12, 6), (12, 4)],
             (0, 16): [(1, 16), (0, 17), (0, 15)], (15, 8): [(16, 8), (14, 8), (15, 9), (15, 7)],
             (14, 0): [(15, 0), (13, 0), (14, 1)], (13, 8): [(14, 8), (12, 8), (13, 9), (13, 7)],
             (12, 16): [(13, 16), (11, 16), (12, 17), (12, 15)], (26, 16): [(27, 16), (25, 16), (26, 17), (26, 15)],
             (0, 3): [(1, 3), (0, 4), (0, 2)], (15, 5): [(16, 5), (14, 5), (15, 6), (15, 4)],
             (3, 14): [(4, 14), (2, 14), (3, 15), (3, 13)], (1, 2): [(2, 2), (0, 2), (1, 3), (1, 1)],
             (28, 12): [(29, 12), (27, 12), (28, 13), (28, 11)], (4, 9): [(5, 9), (3, 9), (4, 10), (4, 8)],
             (3, 3): [(4, 3), (2, 3), (3, 4), (3, 2)], (2, 9): [(3, 9), (1, 9), (2, 10), (2, 8)],
             (27, 7): [(28, 7), (26, 7), (27, 8), (27, 6)], (5, 12): [(6, 12), (4, 12), (5, 13), (5, 11)],
             (4, 4): [(5, 4), (3, 4), (4, 5), (4, 3)], (28, 9): [(29, 9), (27, 9), (28, 10), (28, 8)],
             (26, 5): [(27, 5), (25, 5), (26, 6), (26, 4)], (24, 9): [(25, 9), (23, 9), (24, 10), (24, 8)],
             (6, 3): [(7, 3), (5, 3), (6, 4), (6, 2)], (29, 12): [(28, 12), (29, 13), (29, 11)],
             (8, 8): [(9, 8), (7, 8), (8, 9), (8, 7)], (7, 2): [(8, 2), (6, 2), (7, 3), (7, 1)],
             (7, 10): [(8, 10), (6, 10), (7, 11), (7, 9)], (21, 3): [(22, 3), (20, 3), (21, 4), (21, 2)],
             (20, 18): [(21, 18), (19, 18), (20, 19), (20, 17)], (19, 10): [(20, 10), (18, 10), (19, 11), (19, 9)],
             (17, 14): [(18, 14), (16, 14), (17, 15), (17, 13)], (16, 18): [(17, 18), (15, 18), (16, 19), (16, 17)],
             (21, 19): [(22, 19), (20, 19), (21, 18)], (20, 13): [(21, 13), (19, 13), (20, 14), (20, 12)],
             (18, 13): [(19, 13), (17, 13), (18, 14), (18, 12)], (17, 19): [(18, 19), (16, 19), (17, 18)],
             (23, 16): [(24, 16), (22, 16), (23, 17), (23, 15)], (21, 0): [(22, 0), (20, 0), (21, 1)],
             (8, 11): [(9, 11), (7, 11), (8, 12), (8, 10)], (22, 15): [(23, 15), (21, 15), (22, 16), (22, 14)],
             (9, 10): [(10, 10), (8, 10), (9, 11), (9, 9)], (27, 8): [(28, 8), (26, 8), (27, 9), (27, 7)],
             (23, 14): [(24, 14), (22, 14), (23, 15), (23, 13)], (26, 9): [(27, 9), (25, 9), (26, 10), (26, 8)],
             (10, 1): [(11, 1), (9, 1), (10, 2), (10, 0)], (8, 17): [(9, 17), (7, 17), (8, 18), (8, 16)],
             (26, 8): [(27, 8), (25, 8), (26, 9), (26, 7)], (25, 7): [(26, 7), (24, 7), (25, 8), (25, 6)],
             (11, 12): [(12, 12), (10, 12), (11, 13), (11, 11)], (29, 15): [(28, 15), (29, 16), (29, 14)],
             (15, 17): [(16, 17), (14, 17), (15, 18), (15, 16)], (14, 11): [(15, 11), (13, 11), (14, 12), (14, 10)],
             (13, 1): [(14, 1), (12, 1), (13, 2), (13, 0)], (12, 15): [(13, 15), (11, 15), (12, 16), (12, 14)],
             (11, 17): [(12, 17), (10, 17), (11, 18), (11, 16)], (25, 17): [(26, 17), (24, 17), (25, 18), (25, 16)],
             (15, 2): [(16, 2), (14, 2), (15, 3), (15, 1)], (13, 14): [(14, 14), (12, 14), (13, 15), (13, 13)],
             (27, 18): [(28, 18), (26, 18), (27, 19), (27, 17)], (0, 13): [(1, 13), (0, 14), (0, 12)],
             (3, 8): [(4, 8), (2, 8), (3, 9), (3, 7)], (2, 0): [(3, 0), (1, 0), (2, 1)],
             (1, 8): [(2, 8), (0, 8), (1, 9), (1, 7)], (4, 3): [(5, 3), (3, 3), (4, 4), (4, 2)],
             (28, 0): [(29, 0), (27, 0), (28, 1)], (2, 15): [(3, 15), (1, 15), (2, 16), (2, 14)],
             (27, 4): [(28, 4), (26, 4), (27, 5), (27, 3)], (5, 2): [(6, 2), (4, 2), (5, 3), (5, 1)],
             (29, 5): [(28, 5), (29, 6), (29, 4)], (26, 4): [(27, 4), (25, 4), (26, 5), (26, 3)]}

def output(string):
    sys.stderr.write(', '.join([string]) + "\n")

def timeout(seconds=10.0, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(0, seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

def assignPlayerOrder():
    global playerOrder
    global orderSaved

    playerOrder = list(range(myID,numOfPlayers))+list(range(0,myID))
    orderSaved = True

def deadPlayersWipe(playerID):
    global visitedTiles
    visitedTiles = {temp: tiles for temp, tiles in visitedTiles.items() if tiles != playerID}

def tileValueCalc(locationsOfPlayers, tempVisited, playerID):

    currentID = 1
    copyTiles = set(x for x in tempVisited)
    playerGraphs = {i: {} for i in range(numOfPlayers)}
    while True:

        finished = True
        moves = {}

        for player in playerOrder:
            for move in locationsOfPlayers[player]:
                if move not in copyTiles or (move in moves and id ==1):
                    finished = False
                    copyTiles.add(move)
                    moves[move]= player
        for u, q in moves.items():
            playerGraphs[q][u] = currentID
        if finished:
            break
        locationsOfPlayers = [[i for i, v in moves.items() if v ==g] for g in range(numOfPlayers)]
        currentID+=1

    enemyTiles = sum([len(playerGraphs[i]) for i in range(numOfPlayers) if i != myID])

    myTiles = len(playerGraphs[playerID])

    enemyDist = sum([sum(playerGraphs[i].values()) for i in range(numOfPlayers) if i != playerID])

    value = sum([myTiles*10000000,enemyTiles * -100000, enemyDist])
    return value

@timeout(0.095)
def findNextMove():
    tempVisited = visitedTiles.copy()

    for playerID in playerOrder:
        if deadPlayers.__contains__(playerID)==False:
            neighboursAndValues = []

            x, y =  turnMoves[playerID]

            playerLocation = (x, y)

            for neighbour in NEIGHBOURS[playerLocation]:
                if neighbour not in tempVisited:
                    locationsOfPlayers = [[location] for location in turnMoves.copy()]

                    locationsOfPlayers[myID] = [neighbour]

                    for player in deadPlayers:
                        locationsOfPlayers[player] = []

                    value = tileValueCalc(locationsOfPlayers, tempVisited, myID)
                    neighboursAndValues.append((value, neighbour))
            if myID == playerID:
                tilePicker(playerLocation, neighboursAndValues)


def tilePicker(myLocation, neighboursAndValues):
    directionTranslator(myLocation,(sorted(neighboursAndValues, key=lambda temp: temp[0], reverse = True)[0])[1])

def directionTranslator(current, next):
    global bestDirection
    if current[1] < next[1]:
        bestDirection = "DOWN"
    elif current[1] > next[1]:
        bestDirection = "UP"
    elif current[0] < next[0]:
        bestDirection = "RIGHT"
    else:
        bestDirection = "LEFT"

##################################
# important global variables

visitedTiles = {}

playerOrder = []
orderSaved = False

deadPlayers = []

bestDirection = "LEFT"
#################################

# game loop
while True:
    # n: total number of players (2 to 4).
    # p: your player number (0 to 3).
    numOfPlayers, myID = [int(i) for i in input().split()]

    if orderSaved == False:
        assignPlayerOrder()

    turnMoves = []

    for playerID in range(numOfPlayers):
        x0, y0, x1, y1 = [int(j) for j in input().split()]

        turnMoves.append((x1, y1))

        if deadPlayers.__contains__(playerID) == False:
            if x0==-1:
                deadPlayers.append(playerID)
                deadPlayersWipe(playerID)

            else:
                visitedTiles[(x0,y0)] = playerID
                visitedTiles[(x1,y1)] = playerID

    try:
        findNextMove()
    except TimeoutError as e:
        output("timeout")
        print(bestDirection)

    print(bestDirection)