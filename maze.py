class Node:
    def __init__(self, is_wall):
        self.is_wall = is_wall     # Bool denoting whether node is path (False) or wall (True)
        self.distance = 1000    # Distance from starting node. Default is set to arbitrary large number
        self.jumped = False     # Bool denoting if a wall has been passed through
        self.left = None        # Attributes containing nodes that are directly adjacent
        self.right = None
        self.up = None
        self.down = None

    def __lt__(self, other):
        # Allows node objects to be sorted by distance
        return self.distance < other.distance


def solution(map):
    """
    Main function
    :param map: input maze
    :return: shortest distance
    """
    # Get dimensions of the input maze
    height = len(map) - 1
    width = len(map[0]) - 1

    # Calculate shortest distance from beginning (0, 0) of maze to end (h-1, w-1)
    # Then calculate from the end (h-1, w-1) to the beginning (0, 0)
    for_path = get_distance(map, (0, 0), (height, width))
    back_path = get_distance(map, (height, width), (0, 0))
    
    # Return whichever distance is shorter
    if for_path < back_path:
        return for_path
    else:
        return back_path


def get_distance(map, start, end):
    """
    Function that takes in start and endpoints, runs helper functions to
    create a linked matrix of node objects, then calls recursive function to find shortest
    distance between start and end
    :param map: input maze (list of lists containing 0s and 1s)
    :param start: coordinates of maze starting point (tuple of two integers)
    :param end: coordinates of end point (tuple of two integers)
    :return: shortest distance between start and end
    """
    # Retrieve matrix of linked nodes from helper function
    maze_matrix = []
    _get_matrix(maze_matrix, map)

    # Make list of all nodes in the matrix
    unvisited = [node for row in maze_matrix for node in row]

    # Manually set distance of start node to 1 so it will be pulled first in the recursive function
    maze_matrix[start[0]][start[1]].distance = 1

    # Call recursive function.
    # List is sorted in reverse order so that the lowest distance node is always the next to be popped
    return _calculate_distance(maze_matrix[end[0]][end[1]], sorted(unvisited, reverse=True), [])


def _get_matrix(matrix, maze):
    """
    Helper function that creates a matrix with dimensions equiv to input maze.
    :param matrix: empty list
    :param maze: input maze
    :return: matrix of wall and non-wall nodes
    """
    # Fill matrix with node objects. Create wall nodes where maze[x][y] is 1, non-wall if 0.
    for row in range(0, len(maze)):
        matrix.append([])
        for column in range(0, len(maze[row])):
            if maze[row][column] == 0:
                matrix[row].append(Node(False))
            else:
                matrix[row].append(Node(True))

    # Call helper function to link nodes together
    _link_nodes(matrix)


def _link_nodes(matrix):
    """
    Helper function that links adjacent nodes
    :param matrix: matrix of nodes
    :return: matrix of connected nodes
    """
    # Loop through nodes in matrix and assign adjacent nodes to each other
    # Check first if nodes are on the edge to avoid potential index errors
    for row in range(0, len(matrix)):
        for column in range(0, len(matrix[row])):
            if isinstance(matrix[row][column], Node):
                if column > 0:
                    matrix[row][column].left = matrix[row][column - 1]

                if column < len(matrix[row]) - 1:
                    matrix[row][column].right = matrix[row][column + 1]

                if row > 0:
                    matrix[row][column].up = matrix[row - 1][column]

                if row < len(matrix) - 1:
                    matrix[row][column].down = matrix[row + 1][column]


def _calculate_distance(end, unvisited, visited):
    """
    Recursive function that will continuously update the shortest path
    to each node until all nodes have been visited. Returns the distance attribute of the end node object.
    Uses (I hope) Dijkstra's algorithm to find shortest distance.
    :param end: the end node that corresponds to maze exit
    :param unvisited: list of all nodes in the matrix
    :param visited: empty list
    :return: end node's distance attribute
    """
    # Pop whatever node is at the end of the unvisited list
    cur_node = unvisited.pop()

    # Run this block of code for each direction
    for direction in ["up", "down", "left", "right"]:

        # For readability, cur_node.direction shortened to next_node
        next_node = getattr(cur_node, direction)

        # Check to see if current node has a linked node in that direction and it hasn't been visited
        if next_node and next_node not in visited:

            # If linked node is a wall and a wall has not been passed through yet
            # Check if the path to the next node is shortest one found so far
            # If so, allow it to pass through the wall
            # And update next_node to show it has gone through a wall

            if next_node and next_node.is_wall and cur_node.jumped is False:
                distance = cur_node.distance + 1
                if distance < next_node.distance:
                    next_node.distance = distance
                    next_node.jumped = True

            # If linked node not a wall, check if path is the shortest so far
            # If it is, update next_node's distance
            # If a wall has been jumped at some point on the path, update next_node's jumped attribute

            elif next_node and next_node.is_wall is False:
                distance = cur_node.distance + 1
                if distance < next_node.distance:
                    if cur_node.jumped:
                        next_node.jumped = True
                    next_node.distance = distance

                # If a space has been reached in the same distance without jumping a wall
                # A more efficient path has been found
                # Update next_node's jumped attribute to False
                elif distance == next_node.distance and cur_node.jumped is False:
                    next_node.jumped = False

    # Add current node to visited list so that it cannot be visited again
    visited.append(cur_node)

    # If there are more nodes to visit, call function again
    if unvisited:
        return _calculate_distance(end, sorted(unvisited, reverse=True), visited)

    # Otherwise return end node's distance
    else:
        return end.distance


# The two non-hidden test cases
"""print(solution([[0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 1, 1, 0],
                   [0, 0, 0, 0, 0, 0],
                   [0, 1, 1, 1, 1, 1],
                   [0, 1, 1, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0]]))"""
"""print(solution([[0, 1, 1, 0],
                [0, 0, 0, 1],
                [1, 1, 0, 1],
                [1, 1, 1, 0]]))"""
# Maze I created that algorithim isn't solving correctly
print(solution([[0, 1, 1, 1, 0, 0, 0],
                [0, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0],
                [0, 0, 0, 1, 1, 1, 0]]))

