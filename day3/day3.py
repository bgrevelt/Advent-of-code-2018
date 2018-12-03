'''
--- Day 3: No Matter How You Slice It ---

The Elves managed to locate the chimney-squeeze prototype fabric for Santa's suit (thanks to someone who helpfully wrote its box IDs on the wall of the warehouse in the middle of the night). Unfortunately, anomalies are still affecting them - nobody can even agree on how to cut the fabric.

The whole piece of fabric they're working on is a very large square - at least 1000 inches on each side.

Each Elf has made a claim about which area of fabric would be ideal for Santa's suit. All claims have an ID and consist of a single rectangle with edges parallel to the edges of the fabric. Each claim's rectangle is defined as follows:

The number of inches between the left edge of the fabric and the left edge of the rectangle.
The number of inches between the top edge of the fabric and the top edge of the rectangle.
The width of the rectangle in inches.
The height of the rectangle in inches.
A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3 inches from the left edge, 2 inches from the top edge, 5 inches wide, and 4 inches tall. Visually, it claims the square inches of fabric represented by # (and ignores the square inches of fabric represented by .) in the diagram below:

...........
...........
...#####...
...#####...
...#####...
...#####...
...........
...........
...........
The problem is that many of the claims overlap, causing two or more claims to cover part of the same areas. For example, consider the following claims:

#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
Visually, these claim the following areas:

........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........
The four square inches marked with X are claimed by both 1 and 2. (Claim 3, while adjacent to the others, does not overlap either of them.)

If the Elves all proceed with their own plans, none of them will have enough fabric. How many square inches of fabric are within two or more claims?
'''
import re
from collections import namedtuple
import unittest
import math

Claim = namedtuple('claim', 'id, from_left, from_top, width, height')

def parse_claims(input):
    return [Claim._make(re.match('#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line).groups()) for line in input]

# return the overlapping coordinates for two claims
def get_overlap(claim1, claim2):
    left1 = int(claim1.from_left)
    top1 = int(claim1.from_top)
    right1 = left1 + int(claim1.width) - 1
    bottom1 = top1 + int(claim1.height) - 1

    left2 = int(claim2.from_left)
    top2 = int(claim2.from_top)
    right2 = left2 + int(claim2.width) - 1
    bottom2 = top2 + int(claim2.height) - 1

    if left1 <= right2 and right1 >= left2 and top1 <= bottom2 and bottom1 >= top2:
        overlap_left = max(left1, left2)
        overlap_right = min(right1, right2)
        overlap_top = max(top1, top2)
        overlap_bottom = min(bottom1, bottom2)
        return [(x,y) for x in range(overlap_left, overlap_right + 1) for y in range(overlap_top, overlap_bottom + 1)]
    else:
        return []

def get_overlapping_coords(input):
    claims = parse_claims(input)
    overlaps = []
    for i, claim1 in enumerate(claims):
        for claim2 in claims[i + 1:]:
            overlaps.extend(get_overlap(claim1, claim2))

    return set(overlaps)

def puzzle1(input):
    return len(get_overlapping_coords(input))

class Puzzle1Test(unittest.TestCase):
    def test(self):
        '''
        #1 @ 1,3: 4x4
        #2 @ 3,1: 4x4
        #3 @ 5,5: 2x2
        Visually, these claim the following areas:

        ........
        ...2222.
        ...2222.
        .11XX22.
        .11XX22.
        .111133.
        .111133.
        ........
        The four square inches marked with X are claimed by both 1 and 2.
        '''
        self.assertEqual(puzzle1(['#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2']), 4)

print('The solution to puzzle 1 is {}'.format(puzzle1(open('input.txt', 'r').readlines())))

def claim_to_coords(claim):
    return [(x+int(claim.from_left),y + int(claim.from_top)) for x in range(int(claim.width)) for y in range(int(claim.height))]

def puzzle2(input):
    overlapping_coordinates = get_overlapping_coords(input)
    claims = parse_claims(input)
    for claim in claims:
        if all([coord not in overlapping_coordinates for coord in claim_to_coords(claim)]):
            return claim.id

print('The solution to puzzle 2 is {}'.format(puzzle2(open('input.txt', 'r').readlines())))