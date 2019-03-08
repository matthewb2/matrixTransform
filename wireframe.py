import numpy as np

class Wireframe:
    def __init__(self):
        self.nodes = np.zeros((0, 4))
        self.edges = []

    def addNodes(self, node_array):
        ones_column = np.ones((len(node_array), 1))
        ones_added = np.hstack((node_array, ones_column))
        self.nodes = np.vstack((self.nodes, ones_added))

    def addEdges(self, edgeList):
        self.edges += edgeList

    def outputNodes(self):
        for i in range(self.nodes.shape[1]):
            (x, y, z, _) = self.nodes[:, i]
            print "Node %d: (%.3f, %.3f, %.3f)" % (i, x, y, z)

    def outputEdges(self):
        for i, (start, stop) in enumerate(self.edges):
            node1 = self.nodes[:, start]
            node2 = self.nodes[:, stop]
            print "Edge %d: (%.3f, %.3f, %.3f)" % (i, node1[0], node1[1], node1[2]),
            print "to (%.3f, %.3f, %.3f)" % (node2[0], node2[1], node2[2])

    def findCentre(self):
        #num_nodes = len(self.nodes)
        #mean = np.mean(self.nodes) / num_nodes
        mean = self.nodes.mean(axis=0)     # to take the mean of each col
        print mean
        #print "next"
        return mean

    def transform(self, matrix):
        """ Apply a transformation defined by a given matrix. """
        self.nodes = np.dot(self.nodes, matrix)

    def scale(self, center, matrix):
        """ Scale the wireframe from the centre of the screen """
        for i,node in enumerate(self.nodes):
            self.nodes[i] = center + np.matmul(matrix, node-center)

    def rotate(self, center, matrix):
        for i, node in enumerate(self.nodes):
            self.nodes[i] = center + np.matmul(matrix, node-center)




