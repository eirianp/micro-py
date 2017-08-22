#!/usr/bin/env python

'''
Eirian Owen Perkins
http://plv.colorado.edu/ads/2017-4555-grader
'''

import sys
import re

#DEBUG = True
DEBUG = False

def usage():
    print sys.argv[0], "<file.py>"

class Interp(object):
    def __init__(self, script=None):
        self._environment = {}
        self._script = script
        self._linecount = 0

        self._operators = "+-*/"
        self._id = re.compile("[a-zA-Z_][a-zA-Z0-9_]*")

    def syntax_error(self, script):
        print 'Invalid syntax line', self._linecount, "\n\t", " ".join(script)

    def unbound_var(self, var):
        print 'Unbound variable on line', self._linecount, "\n\t", var

    def is_operator(self, item):
        if str(item) in self._operators:
            return True
        return False

    def is_identifier(self, item):
        m = self._id.match(item)
        if m == None:
            return False
        return True

    def parse(self, script=None):
        res = True
        self._linecount += 1
        if script == None:
            script = self._script
        if script == None:
            print "Empty file"
            return False

        if "=" in script:
            # do some error checking
            if len(script) < 3 or not script.index("=") == 1:
                self.syntax_error(script)
                return False
            res = self.assign_stmt(script[0], script[2:])

        if "print" in script:
            # do some error checking
            if len(script) < 2 or not script.index("print") == 0:
                self.syntax_error(script)
                return False
            res = self.print_stmt(script[1:])
        return res

    def assign_stmt(self, left, right):
        if DEBUG:
            print "assigning", right, "to", left
        if not self.is_identifier(left):
            self.syntax_error(str(left) + " = " + " ".join(right))
            return False
        value = self.evaluate(right)
        if value == False:
            return value
        self._environment[left] = value
        return True

    def evaluate(self, other):
        # first, convert variables, integers to integers
        # all variables must be assigned before reference (check environment for values)
        othercpy = other
        for index, item in enumerate(other):
            if self.is_operator(item):
                continue
            if self.is_identifier(item):
                if item in self._environment:
                    other[index] = self._environment[item]
                else:
                    self.unbound_var(item)
                    return False
            else:
                try:
                    other[index] = int(item)
                except ValueError:
                    self.syntax_error(" ".join([str(x) for x in othercpy]))

        while "*" in other:
            index = other.index("*")
            left = other[index - 1]
            right = other[index + 1]
            other = other[0 : index-1] + [ left*right ] + other[index+2:]

        while "/" in other:
            index = other.index("/")
            left = other[index - 1]
            right = other[index + 1]
            other = other[0 : index-1] + [ left/right ] + other[index+2:]

        while "+" in other:
            index = other.index("+")
            if index == 0:
                other = other[1:]
                break
            left = other[index - 1]
            right = other[index + 1]
            other = other[0 : index-1] + [ left+right ] + other[index+2:]

        while "-" in other:
            index = other.index("-")
            if index == 0:
                other[1] = -other[1]
                other = other[1:]
                break
            left = other[index - 1]
            right = other[index + 1]
            other = other[0 : index-1] + [ left-right ] + other[index+2:]

        return other[0]

    def print_stmt(self, other):
        if DEBUG:
            print "printing", other
        value = self.evaluate(other)
        if value == False:
            return value
        # not a mistake, it should print a value to screen
        print value
        return True


def opsplitter(line):
    return re.split("([+-/*=])", line.replace(" ", ""))

if __name__ == "__main__":
    if not len(sys.argv) == 2:
        usage()
        sys.exit(0)

    # TODO: check that file is valid
    # (skipping check because this is a toy)
    p = Interp()
    with open(sys.argv[1], 'r') as f:
        for line in f:
            line = line.strip().split()
            #line = opsplitter(line.strip()) # need to change interpretter code to get this working properly
            if line:
                res = p.parse(line)
                # quit on first error
                # XXX remove lines below to see more errors
                if not res:
                    break
    
