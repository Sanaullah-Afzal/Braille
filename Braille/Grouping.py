from math import dist
import math


def min_distance(arr):
    """Calculate Minimum - Vertical / Horizontal / Diagonal - Distances between Pixels"""
    min_horizontal = float('inf')
    min_vertical = float('inf')
    min_diagonal = float('inf')

    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            # Horizontal distance
            if arr[i][0] == arr[j][0]:
                distance = abs(arr[i][1] - arr[j][1])
                min_horizontal = min(min_horizontal, distance)

            # Vertical distance
            elif arr[i][1] == arr[j][1]:
                distance = abs(arr[i][0] - arr[j][0])
                min_vertical = min(min_vertical, distance)

            # Diagonal distance
            elif abs(arr[i][0] - arr[j][0]) == abs(arr[i][1] - arr[j][1]):
                distance = dist(arr[i], arr[j])
                min_diagonal = min(min_diagonal, distance)

    max_vertical = min_vertical * 2
    max_diagonal = math.sqrt(max_vertical ** 2 + min_vertical ** 2)
    return min_horizontal, min_vertical, min_diagonal, max_vertical, max_diagonal


def row_wise(arr: list[tuple[int, int]]):
    """Grouping the Dots for Every 3 Rows (Makes a Line of Braille Code)"""
    lines = []
    count = 1
    prev = arr[0][0]
    start = 0
    for i in range(len(arr)):
        if arr[i][0] > prev:
            count += 1
            prev = arr[i][0]
        if count > 3:
            group = arr[start:i]
            lines.append(group)
            count = 1
            start = i
            prev = arr[i][0]
        if i == len(arr) - 1:
            group = arr[start:i+1]
            lines.append(group)

    return lines


def column_wise(arr: list[tuple[int, int]]):
    """Grouping the Lines for Every 2 Adjacent Columns (Makes a Character of Braille Code)"""
    min_hor, min_ver, min_dia, max_ver, max_dia = min_distance(arr)
    groups = {}
    # Compare ALL Tuples
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            # Chessboard Distance Between 2 points
            distance = math.sqrt((arr[j][0] - arr[i][0]) ** 2 + (arr[j][1] - arr[i][1]) ** 2)
            if i not in groups and arr[i] != (0, 0):
                groups[i] = set()
                groups[i].add(arr[i])
            # If Distance Satisfies the Criteria to be in the same 3x2 Matrix
            if distance == min_ver or distance == max_ver or distance == min_dia or distance == max_dia:
                if j not in groups[i]:
                    groups[i].add(arr[j])
                    arr[j] = (0, 0)

    return groups


def find_char(s: set, min_ver: float, min_dia: float, max_ver: float, max_dia: float):
    """Find the English Alphabet Corresponding to Each Group"""
    if len(s) == 1:
        return 'a'

    if len(s) == 2:
        sec = s.pop()
        fir = s.pop()
        if dist(fir, sec) == min_ver:
            return 'c' if fir[0] == sec[0] else 'b'
        if dist(fir, sec) == min_dia:
            return 'e' if (fir[0] > sec[0] and fir[1] > sec[1]) or (fir[0] < sec[0] and fir[1] < sec[1]) else 'i'

        return 'k'

    if len(s) == 3:
        thi = s.pop()
        sec = s.pop()
        fir = s.pop()
        if fir[1] == sec[1] == thi[1]:
            return 'l'
        if dist(fir, sec) == min_ver and dist(fir, thi) == min_dia:
            if sec[1] == thi[1]:
                return 'd'
            elif fir[1] == sec[1]:
                return 'h'
        if dist(fir, sec) == dist(fir, thi) == min_ver:
            return 'f'
        if dist(fir, sec) == min_dia and dist(fir, thi) == min_ver:
            return 'j'
        if dist(fir, sec) == min_ver and dist(fir, thi) == max_ver:
            return 'm'
        if dist(fir, sec) == min_dia and dist(fir, thi) == max_ver:
            return 'o'
        if dist(fir, sec) == min_dia and dist(fir, thi) == max_dia:
            return 's'
        if dist(fir, sec) == max_ver and dist(fir, thi) == max_dia:
            return 'u'

    if len(s) == 4:
        fou = s.pop()
        thi = s.pop()
        sec = s.pop()
        fir = s.pop()
        if fir[1] == thi[1] and sec[1] == fou[1]:
            if dist(fir, thi) == dist(sec, fou) == min_ver:
                if sec[0] == thi[0]:
                    return 't'
                else:
                    return 'g'
            elif dist(fir, thi) == dist(sec, fou) == max_ver:
                return 'x'
        if fir[1] == fou[1] and sec[1] == thi[1] and dist(fir, sec) == min_ver and dist(thi, fou) == min_dia:
            return 'n'
        if fir[1] == thi[1] == fou[1]:
            if dist(fir, sec) == min_ver:
                return 'p'
            elif dist(fir, sec) == min_dia:
                return 'w'
        if fir[1] == sec[1] == fou[1]:
            return 'r'
        if fir[1] == sec[1] == thi[1]:
            return 'v'

        return 'z'

    if len(s) == 5:
        fif = s.pop()
        fou = s.pop()
        thi = s.pop()
        sec = s.pop()
        fir = s.pop()
        if sec[1] == thi[1] == fif[1]:
            return 'y'
        elif fir[1] == thi[1] == fif[1]:
            return 'q'

    return '-'
