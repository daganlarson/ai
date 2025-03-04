AIMA defines depth-limited search recursively. It works better with our search animation environment if we define it iteratively. To help you understand how this is done, here is pseudocode for an iterative version.

1. Set the fringe to be an empty stack
2. Set the closed list to be an empty dictionary
3. Construct a node with the problem's initial state and push it onto the fringe
4. Create a cutoff flag, and set it to False
5. While the fringe is not empty:
    - pop node N from the fringe
        - if contains the goal state:
            - call the callback with halt=True
            - return 
        - if is not on the closed list:
            - place it on the closed list 
            - call the callback with halt=False
        - if the depth of is < limit:
            - expand node and put its successors into the fringe
        - if the depth of >= limit: 
            - DON'T expand , and mark the cutoff flag to true
6. If the fringe became empty and cutoff became true, return 'cutoff'
7. Otherwise, the fringe became empty, we didn't cut off, nor did we find the goal, so return None