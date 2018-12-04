def Day1a(instr):
    """
    Assumes string input of digits

    Review a sequence of digits and find the sum of all digits that match the 
    next digit in the list. The list is circular, so the digit after the last 
    digit is the first digit in the list.

    For example:

    1122     produces a sum of 3 (1 + 2) because the first digit (1) matches the
             second digit and the third digit (2) matches the fourth digit
    1111     produces 4 because each digit (all 1) matches the next
    1234     produces 0 because no digit matches the next
    91212129 produces 9 because the only digit that matches the next one is the 
             last digit, 9
    """
    # Convert input string to list
    m = str2list(instr)

    # Loop over elements, add them to the sum if their right-hand neighbor is 
    # the same
    outsum = 0
    for a, b in zip(m, m[1:] + m):
        if a == b:
            outsum += a
    
    return outsum

def Day1b(instr):
    """
    Assumes string input of digits
    Assumes input string has an even number of digits

    Consider the digit halfway around the circular list. That is, if your list 
    contains 10 items, only include a digit in your sum if the digit 10/2 = 5 
    steps forward matches it. Fortunately, your list has an even number of 
    elements.

    For example:

    1212     produces 6, the list contains 4 items, and all four digits match 
             the digit 2 items ahead
    1221     produces 0, because every comparison is between a 1 and a 2
    123425   produces 4, because both 2s match each other, but no other digit 
             has a match
    123123   produces 12
    12131415 produces 4
    """
    # Convert input string to list
    m = str2list(instr)

    # Loop over all digits, checking ndigits/2 steps forward to see if the digit
    # matches. If it matches, add it to the total
    outsum = 0
    ndigits = len(m)
    checkstep = ndigits//2
    checkidx = [(x+checkstep) % ndigits for x in range(ndigits)]
    for ii in range(ndigits):
        if m[ii] == m[checkidx[ii]]:
            outsum += m[ii]

    return outsum

def str2list(instr):
    """
    Convert a string of digits to a list of integers
    """
    return [int(x) for x in instr.strip()]