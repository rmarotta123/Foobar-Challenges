class Node:
    def __init__(self, is_wall):
        self.is_wall = is_wall     # Bool denoting whether node is path (False) or wall (True)
        self.distance = 1000        # Distance from starting node without considering walls. Set to arbitrary large num
        self.wall_distance = 1000     # Distance with considering walls. Set to arbitrary large num
        self.jumped = False         # Bool denoting if a wall has been passed through

        self.left = None        # Attributes containing nodes that are directly adjacent
        self.right = None
        self.up = None
        self.down = None


def solution(map):
    """
    Main function
    :param map: input maze
    :return: shortest distance
    """
    # Create a matrix of node objects
    maze_matrix = []
    get_matrix(maze_matrix, map)

    # Manually set starting point's distances
    maze_matrix[0][0].distance = 1
    maze_matrix[0][0].wall_distance = 1

    # Create a list of nodes from retrieved matrix and send to recursive function
    unvisited = [node for row in maze_matrix for node in row]
    nowall_calculate_distance(sorted(unvisited, key=lambda node: node.distance, reverse=True), [])

    # Recreate list of nodes with updated distances and pass to second recursive function
    unvisited = [node for row in maze_matrix for node in row]
    wall_calculate_distance(sorted(unvisited, key=lambda node: node.wall_distance, reverse=True), [])

    # Return distance found in second recursion of exit point
    short_dist = maze_matrix[len(map) - 1][len(map[0]) - 1].wall_distance
    return short_dist


def get_matrix(matrix, maze):
    """
    Function that creates a matrix with dimensions equiv to input maze.
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


def nowall_calculate_distance(unvisited, visited):
    """
    Recursive function that takes in maze nodes and calculates their shortest distance from the start.
    This recursion does not allow passing through walls.
    :param unvisited: list of nodes that havent passed through sorted by distance attribute
    :param visited: empty list
    :return: calls the function again if there are still unvisited nodes
    """
    # Pop whatever node is at the end of the unvisited list
    cur_node = unvisited.pop()
    for direction in ["up", "down", "left", "right"]:

        # For readability, cur_node.direction shortened to next_node
        next_node = getattr(cur_node, direction)

        # If connected node is not a wall, check if its distance can be shortened
        # If it can, update its distance
        if next_node and next_node.is_wall is False and next_node not in visited:
            distance = cur_node.distance + 1
            if distance < next_node.distance:
                next_node.distance = distance

        visited.append(cur_node)

    if unvisited:
        return nowall_calculate_distance(sorted(unvisited, key=lambda node: node.distance, reverse=True), [])


def wall_calculate_distance(unvisited, visited):
    """
    Recursive function that takes in maze nodes and calculates their shortest distance from the start.
    This recursion does take walls into account. If a wall can be passed but a wall has already previously been passed,
    the distance calculated by the above recursion is used instead
    :param unvisited: list of nodes that havent passed through sorted by wall_distance attribute
    :param visited: empty list
    :return: calls the function again if there are unvisited nodes
    """
    cur_node = unvisited.pop()
    for direction in ["up", "down", "left", "right"]:
        next_node = getattr(cur_node, direction)

        # Ensure next_node exists and hasn't been passed through function yet
        if next_node and next_node not in visited:
            distance = cur_node.wall_distance + 1

            # If going from path to path, update distance if it can be shortened
            if cur_node.is_wall is False and next_node.is_wall is False:
                if distance < next_node.wall_distance:
                    next_node.wall_distance = distance

                    # If a wall has been previously jumped, update next node
                    if cur_node.jumped:
                        next_node.jumped = True

                # If same distance was reached by a path where jumped = False, that is the more efficient route
                elif distance == next_node.wall_distance and cur_node.jumped is False:
                    next_node.jumped = False

            # Allow passing through wall normally if jumped is False
            elif cur_node.is_wall is False and next_node.is_wall and cur_node.jumped is False:
                if distance < next_node.wall_distance:
                    next_node.wall_distance = distance

            # If jumped is True, use cur_node's distance calculated from previous recursion
            elif cur_node.is_wall is False and next_node.is_wall and cur_node.jumped:
                distance = cur_node.distance + 1
                if distance < next_node.wall_distance:
                    next_node.wall_distance = distance

            # If going from wall to node, update next_node's jumped
            elif cur_node.is_wall and next_node.is_wall is False:
                if distance < next_node.wall_distance:
                    next_node.wall_distance = distance
                    next_node.jumped = True

    if unvisited:
        wall_calculate_distance(sorted(unvisited, key=lambda node: node.wall_distance, reverse=True), [])


print(solution([[0, 1, 1, 1, 0, 0, 0],
                [0, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0],
                [0, 0, 0, 1, 1, 1, 0]]))
