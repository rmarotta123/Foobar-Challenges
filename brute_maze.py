"""At some point I got frustrated trying to find the most efficient solution so I made this program to brute force it.
For every wall in the maze, it finds the shortest path through the maze where the wall is a path instead. A lot of the documentation 
on this code is not updated."""
class Node:
    def __init__(self, is_wall):
        self.is_wall = is_wall     # Bool denoting whether node is path (False) or wall (True)
        self.distance = 1000    # Distance from starting node. Default is set to arbitrary large number
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
    height = len(map)
    width = len(map[0])
    path_lengths = []

    for row in range(height):
        for column in range(width):
            if map[row][column] == 1:
                get_distance(map, (row, column), path_lengths)


    return min(path_lengths)


def get_distance(map, wall_cords, paths):
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
    maze_matrix[wall_cords[0]][wall_cords[1]].is_wall = False
    # Make list of all nodes in the matrix
    unvisited = [node for row in maze_matrix for node in row]

    # Manually set distance of start node to 1 so it will be pulled first in the recursive function
    maze_matrix[0][0].distance = 1

    # Call recursive function.
    # List is sorted in reverse order so that the lowest distance node is always the next to be popped
    _calculate_distance(maze_matrix, paths, sorted(unvisited, reverse=True), [])
    maze_matrix[wall_cords[0]][wall_cords[1]].is_wall = True


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
            if column > 0:
                matrix[row][column].left = matrix[row][column - 1]

            if column < len(matrix[row]) - 1:
                matrix[row][column].right = matrix[row][column + 1]

            if row > 0:
                matrix[row][column].up = matrix[row - 1][column]

            if row < len(matrix) - 1:
                matrix[row][column].down = matrix[row + 1][column]


def _calculate_distance(matrix, paths, unvisited, visited):
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
        if next_node and next_node not in visited and next_node.is_wall is False:
            distance = cur_node.distance + 1
            if distance < next_node.distance:
                next_node.distance = distance

    # Add current node to visited list so that it cannot be visited again
    visited.append(cur_node)

    # If there are more nodes to visit, call function again
    if unvisited:
        return _calculate_distance(matrix, paths, sorted(unvisited, reverse=True), visited)

    # Otherwise return end node's distance
    else:
        paths.append(matrix[len(matrix) - 1][len(matrix[0]) - 1].distance)
