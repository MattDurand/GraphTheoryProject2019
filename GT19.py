# Matthew Durand G00346987 - Graph Theory Project

import sys

# User Input
# https://web.microsoftstream.com/video/65df155a-ac29-460b-869d-2de6ffc6c3fc
# https://pythonprogramminglanguage.com/input/

# If user included the Regular Expression and String when running the program
if len(sys.argv) == 3:
    # Saves the Regular Expression and String entered by the user
    userinfix, userstring = f"{sys.argv[1]}", f"{sys.argv[2]}"
    print(userinfix, userstring)

# If Regular Expression and String haven't been entered yet, prompt user for them
elif len(sys.argv) != 3:
    userinfix = input("Enter an Infix Regular Expression (eg a*): ")
    userstring = input("Enter a String: ")

# Shunting Yard Algorithm
# http://www.oxfordmathcenter.com/drupal7/node/628
# https://web.microsoftstream.com/video/cfc9f4a2-d34f-4cde-afba-063797493a90
# https://stackoverflow.com/questions/36870168/operator-precedence-in-regular-expressions
# https://www.tldp.org/LDP/Bash-Beginners-Guide/html/sect_04_01.html


def shunt(infix):
    """The Shunting Yard Algorithm for converting infix regular expressions to postfix"""
    # N starts off with no value
    # n = None
    # Special Character Dictionary, number represents their precedence, higher number means higher precedence
    # Unary Operators have equal precedence
    specials = {'*': 50, '+': 50, '?': 50, '.': 40, '$': 35, '|': 30}

    pofix = ""
    stack = ""

    for c in infix:

        if c == '(':
            # Add '(' to stack
            stack = stack + c
        elif c == ')':
            while stack[-1] != '(':
                # Add the last item on the stack to pofix, then Remove '(' from stack
                pofix, stack = pofix + stack[-1], stack[:-1]
            # Remove '(' from stack
            stack = stack[:-1]

        # Under development, not yet functional
        # For {N} operator, used to remove the curly brackets from the postfix regular expression
        # elif c == '{':
        #     # Add '{' to stack
        #     stack = stack + c
        # elif c == '}':
        #     while stack[-1] != '{':
        #         # Add the last item on the stack to N as nchar , then Remove '{' from stack
        #         pofix, stack = pofix + stack[-1], stack[:-1]
        #         n = stack[-1]
        #     # Remove '{' from stack
        #     stack = stack[:-1]

        elif c in specials:
            # Compare precedence of special characters
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                # Add the last item on the stack to pofix, then Remove it from stack
                pofix, stack = pofix + stack[-1], stack[:-1]
            # Add character to the stack
            stack = stack + c
        else:
            # Add character to Postfix Expression
            pofix = pofix + c

    while stack:
        # Add the last item on the stack to pofix, then Remove '(' from stack
        pofix, stack = pofix + stack[-1], stack[:-1]

    return pofix


# Thompson's Construction
# https://swtch.com/~rsc/regexp/regexp1.html
# https://web.microsoftstream.com/video/5e2a482a-b1c9-48a3-b183-19eb8362abc9

# Represents a state with two arrows, labelled by label
# Use None for a label representing "E" arrows
class state:
    label = None
    edge1 = None
    edge2 = None


# An NFA is represented by its initial and accept states
class nfa:
    initial = None
    accept = None

    # nfa object instance
    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept


def compile(pofix):
    """Compiles a postfix regular expression into an NFA"""
    nfastack = []

    # Enumerate is used to keep track of the index of the current character in the String
    for i, c in enumerate(pofix):

        # Concatenate
        if c == '.':

            # Pop 2 NFAs off the stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            # Connect first NFAs accept state to the seconds initial state
            nfa1.accept.edge1 = nfa2.initial
            # Push the new NFA to the stack
            nfastack.append(nfa(nfa1.initial, nfa2.accept))

        # Or
        elif c == '|':

            # Pop 2 NFAs off the stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            # Create a new initial state, connect it to initial states of
            # the two NFAs popped from the stack
            initial = state()
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial
            # Create a new accept state, connecting the accept states of
            # the two NFAs popped from the stack to the new accept state
            accept = state()
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept
            # Push the new NFA to the stack
            nfastack.append(nfa(initial, accept))

        # 0 or more
        elif c == '*':

            # Pop a single NFA from the stack
            nfa1 = nfastack.pop()
            # Create new initial and accept states
            initial = state()
            accept = state()
            # Join the new initial state to nfa1s initial state and to the new accept state
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            # Join the old accept state to the new accept state and to nfa1s initial state
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            # Push the new NFA to the stack
            nfastack.append(nfa(initial, accept))

        # 1 or more
        elif c == '+':

            # Pop a single NFA from the stack
            nfa1 = nfastack.pop()
            # Create new initial and accept states
            initial = state()
            accept = state()
            # Join the new initial state to nfa1s initial state
            initial.edge1 = nfa1.initial
            # Join the old accept state to the new accept state and to nfa1s initial state
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            # Push the new NFA to the stack
            nfastack.append(nfa(initial, accept))

        # 0 or 1
        elif c == '?':

            # Pop a single NFA from the stack
            nfa1 = nfastack.pop()
            # Create new initial and accept states
            initial = state()
            accept = state()
            # Join the new initial state to nfa1s initial state and to the new accept state
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            # Join the old accept state to the new accept state
            nfa1.accept.edge2 = accept
            # Push the new NFA to the stack
            nfastack.append(nfa(initial, accept))

        # 0
        elif c == '$':

            # Pop a single NFA from the stack
            nfa1 = nfastack.pop()
            # Create new initial and accept states
            initial = state()
            accept = state()
            # Join the new initial state to nfa1s initial state and to the new accept state
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            # Push the new NFA to the stack
            nfastack.append(nfa(initial, accept))

        else:
            # Create new initial and accept states
            accept = state()
            initial = state()
            # Join the initial state and the accept state using an arrow labelled c
            initial.label = c
            initial.edge1 = accept
            # Push the new NFA to the stack
            nfastack.append(nfa(initial, accept))

    # nfastack should only have a single nfa on it at this point
    return nfastack.pop()


# https://web.microsoftstream.com/video/6b4ba6a4-01b7-4bde-8f85-b4b96abc902a

def followes(state):
    """Return the set of states that can be reached from state following E arrows"""
    # Create a new set, with state as its only member
    states = set()
    states.add(state)

    # Check if state has arrows labeled E from it
    if state.label is None:
        # Check if edge1 is a state
        if state.edge1 is not None:
            # if there's an edge1 follow it
            states |= followes(state.edge1)
        # Check if edge2 is a state
        if state.edge2 is not None:
            # if there's an edge1 follow it
            states |= followes(state.edge2)

    # Return the set of states
    return states


def match(infix, string):
    """Matches string to infix regular expression"""
    # Shunt and compile the regular expression
    postfix = shunt(infix)
    nfa = compile(postfix)

    # Current set of states and next set of states
    currentstate = set()
    nextstate = set()

    # Add the initial state to the current set
    currentstate |= followes(nfa.initial)

    # Loop through the characters in the string
    for s in string:
        # Loop through the current set of states
        for c in currentstate:
            # Check if that state is labelled s
            if c.label == s:
                # Add the edge1 state to the next set
                nextstate |= followes(c.edge1)
        # Set currentstate to nextstate, and clear out nextstate
        currentstate = nextstate
        nextstate = set()

    # Check if the accept state is in the set of current sets
    return (nfa.accept in currentstate)


print(" RegEx:  ", userinfix, "\n", "String: ", userstring, "\n", "Result: ", match(userinfix, userstring))
