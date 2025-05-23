import sys
from crossword import *


#import os
#os.chdir("lab5Crossword")

class CrosswordGenerator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generator.
        """
        self.crossword : Crossword = crossword
        self.domains : dict[Variable, set[str]] = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword with assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save_as_image(self, assignment, filename):
        """
        Save crossword with assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var, words in self.domains.items():
            remove = set[str]()
            for word in words:
                if len(word) != var.length:
                    remove.add(word)
            words.difference_update(remove)
         
    def revise(self, X, Y):
        """
        Make variable `X` arc consistent with variable `Y`.
        To do so, remove values from `self.domains[X]` for which there is no
        possible corresponding value for `Y` in `self.domains[Y]`.

        Return True if a revision was made to the domain of `X`; return
        False if no revision was made.
        """
        revised = False

        if crossword.overlaps.get(X) != None:
            c1, c2 = crossword.overlaps.get(X)
            for word1 in self.domains.get(X):
                valid = False
                for word2 in self.domains.get(Y):
                    if word1[c1] == word2[c2]:
                        valid = True 
                        break
                if not valid:
                    revised = True
                    self.domains.get(X).pop(word1)
        return revised
                
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
           
            arcs = []
            for d1 in self.domains:
                for d2 in self.domains:
                    arcs.append((d1, d2))
            '''
            arcs = []
            for var1 in self.domains.keys():
                for var2 in self.crossword.neighbors(var1):
                    arcs.append((var1, var2))
             '''

        while len(arcs) != 0:
            Xi, Xj = arcs.pop()
            self.revise(Xi, Xj)

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.domains.keys():
            if assignment.get(var) is None:
                return False     
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for var1, word1 in assignment.items():
            for var2, word2 in assignment.items():
                if var1 is not var2:
                    overlaps = self.crossword.overlaps.get((var1, var2))
                    if overlaps is not None and word1[overlaps[0]] != word2[overlaps[1]]:
                        return False 
        return True

    def select_unassigned_variable(self, assignment: dict[Variable, str]):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = dict[Variable, list]()
        for var, words in self.domains.items():
            if assignment.get(var) is None:
                unassigned[var] = words

        #assert(self.assignment_complete(assignment) is False)
        
        min = None
        for var, words in unassigned.items():
            if min is None:
                min = var 
            elif len(words) < len(unassigned[min]):
                min = var 

        return min

    def backtrack(self, assignment: dict[Variable, str]):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a dictionary mapping variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        for word in self.domains.get(var):
            assignment[var] = word
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result 
            assignment.pop(var)
        return None
        



if __name__ == "__main__":
    # Check arguments
    if len(sys.argv) not in [3, 4]:
        sys.exit(f'Usage: {sys.argv[0]} structure words [output]')
    
    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    generator = CrosswordGenerator(crossword)
    assignment = generator.solve()

    # Output result
    if assignment is None:
        print("No solution.")
    else:
        generator.print(assignment)
        if output:
            generator.save_as_image(assignment, output)


