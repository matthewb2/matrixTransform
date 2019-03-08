import wireframe as wf
import pygame
import numpy as np

key_to_function = {

    pygame.K_LEFT: (lambda x: x.translateAll([-10, 0, 0])),
    pygame.K_RIGHT:(lambda x: x.translateAll([ 10, 0, 0])),
    pygame.K_DOWN: (lambda x: x.translateAll([0,  10, 0])),
    pygame.K_UP:   (lambda x: x.translateAll([0, -10, 0])),
	pygame.K_EQUALS: (lambda x: x.scaleAll(1.05)),
    pygame.K_MINUS:  (lambda x: x.scaleAll( 0.95)),
    pygame.K_q:      (lambda x: x.rotateAll('X',  0.1)),
    pygame.K_w:      (lambda x: x.rotateAll('X', -0.1)),
    pygame.K_a:      (lambda x: x.rotateAll('Y',  0.1)),
    pygame.K_s:      (lambda x: x.rotateAll('Y', -0.1)),
    pygame.K_z:      (lambda x: x.rotateAll('Z',  0.1)),
    pygame.K_x:      (lambda x: x.rotateAll('Z', -0.1))}


class ProjectionViewer:
    """ Displays 3D objects on a Pygame screen """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Wireframe Display')
        pygame.key.set_repeat(1,10)
        self.background = (10,10,50)

        self.wireframes = {}
        self.displayNodes = True
        self.displayEdges = True
        self.nodeColour = (255,255,255)
        self.edgeColour = (200,200,200)
        self.nodeRadius = 4

    def addWireframe(self, name, wireframe):
        """ Add a named wireframe object. """

        self.wireframes[name] = wireframe

    def run(self):
        """ Create a pygame screen until it is closed. """

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_to_function:
                        key_to_function[event.key](self)

            self.display()
            pygame.display.flip()

    def display(self):
        """ Draw the wireframes on the screen. """

        self.screen.fill(self.background)

        for wireframe in self.wireframes.values():
            if self.displayEdges:
                for n1, n2 in wireframe.edges:
                    pygame.draw.aaline(self.screen, self.edgeColour, wireframe.nodes[n1][:2], wireframe.nodes[n2][:2], 1)

            if self.displayNodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, self.nodeColour, (int(node[0]), int(node[1])), self.nodeRadius, 0)


    def translationMatrix(self, dx, dy, dz):
        """ Return matrix for translation along vector (dx, dy, dz). """

        return np.array([[1,0,0,0],
                         [0,1,0,0],
                         [0,0,1,0],
                         [dx,dy,dz,1]])

    def scaleMatrix(self, sx=0, sy=0, sz=0):
        """ Return matrix for scaling equally along all axes centred on the point (cx,cy,cz). """

        return np.array([[sx, 0,  0,  0],
                         [0,  sy, 0,  0],
                         [0,  0,  sz, 0],
                         [0,  0,  0,  1]])



    def rotateXMatrix(self, radians):
        """ Return matrix for rotating about the x-axis by 'radians' radians """

        c = np.cos(radians)
        s = np.sin(radians)
        return np.array([[1, 0, 0, 0],
                         [0, c,-s, 0],
                         [0, s, c, 0],
                         [0, 0, 0, 1]])
    def rotateYMatrix(self, radians):
        """ Return matrix for rotating about the y-axis by 'radians' radians """

        c = np.cos(radians)
        s = np.sin(radians)
        return np.array([[ c, 0, s, 0],
                         [ 0, 1, 0, 0],
                         [-s, 0, c, 0],
                         [ 0, 0, 0, 1]])
    def rotateZMatrix(self, radians):
        """ Return matrix for rotating about the z-axis by 'radians' radians """

        c = np.cos(radians)
        s = np.sin(radians)
        return np.array([[c,-s, 0, 0],
                         [s, c, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])


    def translateAll(self, vector):
        """ Translate all wireframes along a given axis by d units. """
        matrix = self.translationMatrix(vector[0], vector[1], vector[2])
        for wireframe in self.wireframes.itervalues():
            wireframe.transform(matrix)


    def scaleAll(self, scale):
        """ Scale all wireframes by a given scale, centred on the centre of the screen. """
        center = [self.width/2, self.height/2, 0, 0]
        matrix = self.scaleMatrix(scale, scale, scale)

        for wireframe in self.wireframes.itervalues():
            print wireframe.nodes
            wireframe.scale(center, matrix)

    def rotateAll(self, axis, theta):
        """ Rotate all wireframe about their centre, along a given axis by a given angle. """

        rotateFunction = 'rotate' + axis + 'Matrix'

        for wireframe in self.wireframes.itervalues():
            center = wireframe.findCentre()
            matrix = getattr(self, rotateFunction)(theta)
            wireframe.rotate(center, matrix)

if __name__ == '__main__':
    pv = ProjectionViewer(600, 500)

    cube = wf.Wireframe()
    cube_nodes = [(x,y,z) for x in (50,250) for y in (50,250) for z in (50,250)]
    cube.addNodes(np.array(cube_nodes))
    cube.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])

    pv.addWireframe('cube', cube)
    pv.run()
