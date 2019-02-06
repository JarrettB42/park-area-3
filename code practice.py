import random

"""
Problem 1: Determine whether a circular array of relative indices is composed of a single complete cycle.

Clarification:
The array fits in memory, and the size is known
Relative index means: add the current *value* to the current *index*
current = index
next    = current + array[index]
If next >= len(array), it "wraps" back to 0 and continues on
next    = (current + array[index]) % len(array)
Relative index can be negative, so you would go left
Values can be positive, negative, or 0
We didn't ask for max/min value size

Thoughts:
If you hit a 0, you're stuck
There's still some ambiguity on the definition of "single complete cycle"
If I visit every element, but end on 0, should that be true or false?

Assumption:
We must start and end on index 0. This could be extended by wrapping
the following functions in a loop over each index in the array

Examples:
[1, 1, 1] true
[1, 1, 0] false
[2, 1, 1] false
[2, 2, -1] true
[5, 2,  1] false
"""

def next_relative_index(index, array):
    return (index + array[index]) % len(array) # wrap around left/right
#def

# My first thought was to do N jumps, then see if I'm back at index 0.
# I have to make sure I don't revisit index 0 in the middle of the cycle.
# If I do, the cycle is too short, and I return false.
# But if I don't, then I must have seen every element.
# If I didn't see every element, then I saw a duplicate,
# but if I saw a duplicate before getting back to index 0
# I would be stuck in a smaller loop, and wouldn't make it back to index 0
# Time Complexity: O(N)
# Space Complexity: O(1)
def is_complete_cycle_counting(array):
    #TODO: validate array?
    current_index = 0
    for i in range(len(array)-1):  # jump N-1 times
        current_index = next_relative_index(current_index, array) # make the jump
        if current_index == 0: # if we see 0 before the end
            return False       # the cycle was too short
    current_index = next_relative_index(current_index, array) # make the last jump
    # if we made it back to index 0 after N total jumps, it's 1 full cycle
    return current_index == 0
#def

# None of us asked about modifying the array, whoops.
# Since the indexing is relative, if you find a 0, that's the end of the cycle.
# Since we can edit the array, if we write 0 to every index we visit,
# we can just count our jumps until we find a 0.
# If we jump N times, since we're marking visits with a 0, it must be a complte cycle.
# Sentinels are a cool concept.
# Time Complexity: O(N)
# Space Complexity: O(1)
def is_complete_cycle_sentinel(array):
    jumps = 0
    index = 0
    while array[index] != 0: # until we find a 0
        next_index = next_relative_index(index, array) # store the next index
        array[index] = 0     # drop a sentinel
        index = next_index   # make the jump
        jumps += 1           # count the jump
    #while
    return jumps == len(array) # if we made N jumps, it's a complete cycle
#def

# A third way to do this would be to create a boolean array of equal length.
# After you make a jump, check if you have been here before.
# If no, set the visit flag to true and jump again.
# If yes, the cycle is done.
# If every flag is true, you visited every index, return true.
# If *any* flag is false, it's not a complete cycle, return false.
# This is probably the most natural way to think about / approach the problem.
# Main downside is the extra memory you need for the flag array.
# You could use bitflags, but that's still O(N)
# For further simplicity, I'll just use a hashset and store each visited index.
# If my current index is in the visited set, I've hit a cycle.
# If the length of the visited set is equal to the length of the array, I visited every index.
# However, if the last node is 0, it's a false positive (assumption)
# So I *also* need to check if I made it back the start (0 index)
# Time Complexity: O(N)
# Space Complexity: O(N)
def is_complete_cycle_flags(array):
    index = 0
    visited = set()
    while index not in visited:
        visited.add(index)
        index = next_relative_index(index, array) # make the jump
    #while
    return len(visited) == len(array) and index == 0
#def

test_arrays = [
    [1, 1,  1], # true
    [1, 1,  0], # false
    [2, 1,  1], # false
    [2, 2, -1], # true
    [5, 2,  1]  # false
]

print("Testing Relative Cycles...\n")

for test_array in test_arrays:
    print(test_array)
    print(is_complete_cycle_flags(test_array))
    print(is_complete_cycle_counting(test_array))
    print(is_complete_cycle_sentinel(test_array))
#for

"""
Problem 2: Imagine that there is a large bucket of marbles of various colors.
Describe an algorithm for drawing a marble from a bucket at random.

Clarification:
The list of colors is known
The number of marbles of a given color is known
Therefore, the total number of marbles is known
How the marbles stored is up to us (this is the crux of the problem)
Prioritize speed of drawing a marble.
There are too many marbles to enumerate in memory

Thoughts:
We didn't ask about replacement, so I'll do both versions
The difficulty comes from the uneven distribution of colored marbles
Since we want to draw quickly, I first thought hashmap,
but there's far more marbles that colors.
A different data structure might be better suited to pick a weighted color.
We can calculate the ratio(%) for each color, this *should* be useful...

Approach 1:
We know the total number of marbles.
We know how many are in each color.
We pick a random number between 0 and the total number of marbles.
For each color, if our number is less than the count for that color,
return that color. Otherwise, subtract that count, and check the next color.
This works well when the marble is not replaced,
since we only need to update the count for the color returned and the total count,
which we can do in constant time.
Time and Space both scale with the number of colors (C)
# Time Complexity: O(C)
# Space Complexity: O(C)

Approach 2:
TODO: Binary Search
With replacement: Binary search, no values to update
Time and Space both scale with the number of colors (C)
# Time Complexity: O(log C)
# Space Complexity: O(C)
Without replacement: We have to recalculate the cumulative totals (basically just -1 to each subsequent)
# Time Complexity: O(C log C)
# Space Complexity: O(C)
"""

class BagOfMarbles:
    
    # colors: list of colors
    # counts: list of counts
    # Given 2 parallel lists of colors and counts, initialize the bag of marbles
    # TODO: verify colors/counts
    def __init__(self, colors, counts):
        # 3 parallel lists/arrays
        self.colors = colors
        self.counts = counts
        self.count_marbles()
    #def
    
    def count_marbles(self):
        total = 0
        self.totals = [0] # for binary search method
        for count in self.counts:
            total += count
            self.totals.append(total)
        #for
        self.total = total
    #def
    
    # Adds 1 marble of the given color
    # A dictionary or hashmap would make insertion way faster
    # But the simpler arrays were easier to work with when drawing marbles
    # Time Complexity: O(C)
    def add_marble(self, color):
        self.total += 1                             # add 1 to total
        self.counts[self.colors.index(color)] += 1 # add 1 to specified color
        self.count_marbles() # update cumulative totals for peek()
    #def
    
    # Adds 1 marble of the given color
    # A dictionary or hashmap would make insertion way faster
    # But the simpler arrays were easier to work with when drawing marbles
    # Time Complexity: O(C)
    def remove_marble(self, color):
        self.total -= 1                             # remove 1 from total
        self.counts[self.colors.index(color)] -= 1 # remove 1 from specified color
        self.count_marbles() # update cumulative totals for peek()
    #def
    
    # Lets the caller look at the color of a random marble from the bag
    # They don't get to keep it though, that's my marble
    # Returns a string representing the color
    def peek(self): # Draw & Replace (don't take)
        # Since we're matching on ranges, we have to find where
        # the left bucket is smaller, but the right bucket is larger
        # more than totals[i] but less than totals[i+1]
        # I opted for the range of [0, self.total)
        
        # example:
        # colors:     r,  g,  b,  y
        # counts:    10, 20,  0, 60
        # totals: 0, 10, 30, 30, 90
        #  0- 0: totals 0 edge value
        #  0- 9: totals 1 more than totals[0] but less than totals[1]
        # 10-29: totals 2 more than totals[1] but less than totals[2]
        # 30-30: totals 3 impossible situation
        # 30-89: totals 4 will always be less than totals[C], default case
        # binary search on ranges is weird
        
        if self.total < 1: # there are no more marbles
            return "None"  # should throw an exception here
        #if
        
        marble_index = random.randint(0, self.total-1) # both values are inclusive
        
        start = 0
        right = len(self.totals)-1
        color_index = 0
        done = False
        
        while start<=right and not done:
            color_index = (start + right) // 2 # integer division
            if color_index == 0: # edge case
                done = True
            if marble_index > self.totals[color_index] and marble_index < self.totals[color_index+1]:
                done = True
            else:
                if marble_index <= self.totals[color_index]: # bias downward
                    right = color_index-1
                else:
                    start = color_index+1
        
        return self.colors[color_index]
    #def
    
    # Gives the caller a random marble from the bag
    # They get to keep it, it's removed from the bag
    # Returns a string representing the color
    def take(self): # Draw & Take (update values)
        if self.total < 1: # there are no more marbles
            return "None"  # should throw an exception here
        #if
        marble_index = random.randint(0, self.total-1)
        for index, count in enumerate(self.counts):
            if marble_index < count: # pick this color index
                self.remove_marble(self.colors[index])
                return self.colors[index]
            #if
            marble_index -= count
        #for
        return self.colors[-1] # if we got here, marble_index was too high, pick the last color
    #def
#class

print("\nTesting Bag O' Marbles...\n")

marbles = dict()
marbles["red"] = 2
marbles["green"] = 0
marbles["blue"] = 1
marbles["yellow"] = 9

bag = BagOfMarbles(list(marbles.keys()), list(marbles.values()))

bag.add_marble("green")

print("Staring Bag:", list(zip(bag.colors, bag.counts)), "\n")

for i in range(15):
    print("Replace (Binary Search) =", bag.peek())
    print("Remove  (Linear Search) =", bag.take())
    print()
#for

print("Ending Bag:", list(zip(bag.colors, bag.counts)), "\n")

