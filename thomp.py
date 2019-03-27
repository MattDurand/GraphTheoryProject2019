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
    nfastack = []

    for c in pofix:
        if c == '.':

            # Pop 2 NFAs off the stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            # Connect first NFAs accept state to the seconds initial state
            nfa1.accept.edge1 = nfa2.initial
            # Push the new NFA to the stack
            nfastack.append(nfa(nfa1.initial, nfa2.accept))

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

        elif c == '*':

            # Pop a single NFA from the stack
            nfa1 = nfastack.pop()
            # Create new initial and accept states
            initial = state()
            accept = state()
            # Join the new initial state to nfa1s initial state and the new accept state
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            # Join the old accept state to the new accept state and nfa1s initial state
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
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

print(compile("ab.cd.|"))
print(compile("aa.*"))