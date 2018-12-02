import unittest

'''
After feeling like you've been falling for a few minutes, you look at the device's tiny screen. "Error: Device must be calibrated before first use. Frequency drift detected. Cannot maintain destination lock." Below the message, the device shows a sequence of changes in frequency (your puzzle input). A value like +6 means the current frequency increases by 6; a value like -3 means the current frequency decreases by 3.

For example, if the device displays frequency changes of +1, -2, +3, +1, then starting from a frequency of zero, the following changes would occur:

Current frequency  0, change of +1; resulting frequency  1.
Current frequency  1, change of -2; resulting frequency -1.
Current frequency -1, change of +3; resulting frequency  2.
Current frequency  2, change of +1; resulting frequency  3.
In this example, the resulting frequency is 3.

Here are other example situations:

+1, +1, +1 results in  3
+1, +1, -2 results in  0
-1, -2, -3 results in -6
Starting with a frequency of zero, what is the resulting frequency after all of the changes in frequency have been applied?
'''

def puzzle1(input):
    return sum([int(line) for line in input])

class Puzzle1Test(unittest.TestCase):
    def test(self):
        #+1, +1, +1 results in  3
        self.assertEqual(puzzle1(["+1", "+1", "+1"]), 3)
        #+1, +1, -2 results in  0
        self.assertEqual(puzzle1(["+1", "+1", "-2"]), 0)
        #-1, -2, -3 results in -6
        self.assertEqual(puzzle1(["-1", "-2", "-3"]), -6)

print("The answer to puzzle 1 is {}".format(puzzle1(open('puzzle1.txt').readlines())))

'''--- Part Two ---

You notice that the device repeats the same frequency change list over and over. To calibrate the device, you need to find the first frequency it reaches twice.

For example, using the same list of changes above, the device would loop as follows:

Current frequency  0, change of +1; resulting frequency  1.
Current frequency  1, change of -2; resulting frequency -1.
Current frequency -1, change of +3; resulting frequency  2.
Current frequency  2, change of +1; resulting frequency  3.
(At this point, the device continues from the start of the list.)
Current frequency  3, change of +1; resulting frequency  4.
Current frequency  4, change of -2; resulting frequency  2, which has already been seen.
In this example, the first frequency reached twice is 2. Note that your device might need to repeat its list of frequency changes many times before a duplicate frequency is found, and that duplicates might be found while in the middle of processing the list.

Here are other examples:

+1, -1 first reaches 0 twice.
+3, +3, +4, -2, -4 first reaches 10 twice.
-6, +3, +8, +5, -6 first reaches 5 twice.
+7, +7, -2, -7, -4 first reaches 14 twice.
What is the first frequency your device reaches twice?'''

# We might have to repeat the list of frequency changes, so let's use a generator
def frequency_change_generator(input):
    while True:
        for line in input:
            yield int(line)

'''Naive implementation where we just iterate over the input until we get to a frequency we saw before'''
def puzzle2_naive(input):
    seen_frequencies = [0]
    current_frequency = 0
    change_generator = frequency_change_generator(input)
    for change in change_generator:
        current_frequency += change

        if current_frequency in seen_frequencies:
            return current_frequency

        seen_frequencies.append(current_frequency)

'''(hopefully) less naive implementation. 
if we have an input of 
[U, V, W, X, Y, Z]
we know that the frequencies after each change are
[U, U+V, U+V+W, U+V+W+X, U+V+W+X+Y, U+V+W+X+Y+Z]
If we know that the resulting frequency of the input is A, then we know that the next iteration, the frequencies after each change are
[A+U, A+U+V, A+U+V+W, A+U+V+W+X, A+U+V+W+X+Y, A+U+V+W+X+Y+Z]
And the next iteration it would be
[2A+U, 2A+U+V, 2A+U+V+W, 2A+U+V+W+X, 2A+U+V+W+X+Y, 2A+U+V+W+X+Y+Z]
etc, etc
'''
def puzzle2_maths(input):
    input = [int(n) for n in input]
    # first generate a list with the frequency after each change
    frequencies = [0] + [sum(input[:i+1]) for i in range(len(input))]

    if(len(frequencies) != len(set(frequencies))):
        #that's easy, we already have a duplicate
        return [n for n in frequencies if frequencies.count(n) > 1][0]

    iteration_change = frequencies[-1]
    # drop the last freqency because that's the first frequency of the next iteration
    frequencies = frequencies[:-1]

    double = None

    # For each frequency in the progression, we check if it is possible to get there from another frequency in the progression
    for to_find, start_at in [(i,j) for i in range(len(frequencies)) for j in range(len(frequencies)) if i != j]:
        number_of_iterations = (frequencies[to_find] - frequencies[start_at]) / iteration_change
        # We can only do a positive, whole number of iterations
        if number_of_iterations >= 0 and (number_of_iterations % 1 < 0.0000001):
            # We found a frequency which will repeat itself after a number of iterations.
            # The complete number of steps required to get to this duplicated frequency is equal to the number
            # of iterations multiplied by the length of the iteration, plus the number of steps we are into the
            # current iteration.
            steps = number_of_iterations * len(frequencies) + start_at
            # only store this as a potential answer if the number of steps it takes is less than a previously found duplicate
            if (double is None or steps < double[0]):
                double = (steps, frequencies[to_find])

    assert double is not None, "Did not find a solution for the puzzle :("
    return double[1]

class Puzzle2NaiveTest(unittest.TestCase):
    def test(self):
        #+1, -1 first reaches 0 twice.
        self.assertEqual(puzzle2_naive(["+1", "-1"]), 0)
        #+3, +3, +4, -2, -4 first reaches 10 twice.
        self.assertEqual(puzzle2_naive(["+3", "+3", "+4", "-2", "-4"]), 10)
        #-6, +3, +8, +5, -6 first reaches 5 twice.
        self.assertEqual(puzzle2_naive(["-6", "+3", "+8", "+5", "-6"]), 5)
        #+7, +7, -2, -7, -4 first reaches 14 twice.
        self.assertEqual(puzzle2_naive(["+7", "+7", "-2", "-7", "-4"]), 14)

#print("The answer to puzzle 2 is {}".format(puzzle2_naive(open('puzzle1.txt').readlines())))


class Puzzle2MathTest(unittest.TestCase):
    def test(self):
        #+1, -1 first reaches 0 twice.
        self.assertEqual(puzzle2_maths(["+1", "-1"]), 0)
        #+3, +3, +4, -2, -4 first reaches 10 twice.
        self.assertEqual(puzzle2_maths(["+3", "+3", "+4", "-2", "-4"]), 10)
        #-6, +3, +8, +5, -6 first reaches 5 twice.
        #-6, -3, 5, 10, 4, -2, 1, 9, 14, 8, 2, 5
        self.assertEqual(puzzle2_maths(["-6", "+3", "+8", "+5", "-6"]), 5)
        #+7, +7, -2, -7, -4 first reaches 14 twice.
        # 0, 7, 14, 12, 5, 1, 8, 15, 13, 6, 2, 9, 16, 14
        self.assertEqual(puzzle2_maths(["+7", "+7", "-2", "-7", "-4"]), 14)

print("The answer to puzzle 2 is {}".format(puzzle2_maths(open('puzzle1.txt').readlines())))