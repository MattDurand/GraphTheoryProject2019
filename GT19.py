# Matthew Durand G00346987 - Graph Theory Project

# Shunting Yard Algorithm
# http://www.oxfordmathcenter.com/drupal7/node/628
# https://web.microsoftstream.com/video/cfc9f4a2-d34f-4cde-afba-063797493a90?referrer=https:%2F%2Flearnonline.gmit.ie%2Fcourse%2Fview.php%3Fid%3D467

def shunt(infix):
    # Special Character precedence
    specials = {'*' : 50, '.': 40, '|': 30}

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
        elif c in specials:
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                # Add the last item on the stack to pofix, then Remove '(' from stack
                pofix, stack = pofix + stack[-1], stack[:-1]
                stack = stack + c
        else:
            pofix = pofix + c # Add character to stack

    while stack[-1] != '(':
        pofix, stack = pofix + stack[-1], stack[:-1] # Add the last item on the stack to pofix, then Remove '(' from stack
    stack = stack[:-1] # Remove '(' from stack

    return pofix