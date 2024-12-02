"""
Skeleton implementation of AStar algorithm.
"""

from queue import PriorityQueue

# Find an optimal path from start to goal
#
class AStar:
    Infinity = float("inf")

    def __init__(self):
        """Initialize the AStar algorithm with start and goal nodes."""
        self.reset()

    def reset(self):
        self.cameFrom = {}
        self.gScore = {}
        self.fscore = {}

    def neighbors(self, node):
        """Return the neighbors of node"""
        raise NotImplementedError("neighbors method is not implemented")
    
    def cost(self, node1, node2):
        """Return the cost to traverse the edge from node1 to node2"""
        raise NotImplementedError("cost method is not implemented")
    
    def heuristic(self, node1, node2):
        """Return an estimate of the cost to traverse from node1 to node2"""
        raise NotImplementedError("heuristic method is not implemented")
    
    def getPath(self, start, goal):
        """
        Find the least cost path from start to goal.

        start is the start node
        goal is the goal node

        n is a function that takes a node and returns a list of all the neighbors
        of that node

        c is a cost function that takes two nodes and returns the cost to
        traverse the edge between them. If there is no edge between them then
        infinity should be returned.

        h is a heuristic function that takes two nodes and returns an estimate
        of the cost to traverse between them.
        """
        q = PriorityQueue()
        self.gScore[start] = 0
        self.fScore[start] = self.heuristic(start, goal)

        def reconstruct_path(node):
            path = [node]
            while node in self.cameFrom:
                node = self.cameFrom[node]
                path.append(node)

            path.reverse()
            return path

        # Queue items are tuples of score, id of node, and node. This ensures that the tuples
        # can be uniquely sorted without having to order nodes themselves.
        q.put_nowait((self.fscore[start], id(start), start))

        while not q.empty():
            score, _, current = q.get_nowait()
            if score > self.fScore[current]:
                # Old node, discard it.
                continue
            if current == goal:
                return reconstruct_path(self.cameFrom, current)

            for neighbor in n(current):
                tentativeScore = self.gScore[current] + self.cost(current, neighbor)
                if tentativeScore < self.gScore.get(neighbor, AStar.Infinity):
                    self.cameFrom[neighbor] = current
                    self.gScore[neighbor] = tentativeScore
                    self.fScore[neighbor] = tentativeScore + self.heuristic(neighbor, goal)
                    q.put_nowait((self.fScore[neighbor], id(neighbor), neighbor))

        return None
