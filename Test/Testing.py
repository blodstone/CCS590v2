'''
Created on Mar 31, 2011

@author: Blodstone
'''
import numpy
class TridiagonalMatrix:
    def __init__(self, numberOfDepthIndex):
        self.vectorX = numpy.zeros ((numberOfDepthIndex, 1), float)
    
    def matrix_solution (self, numberOfDepthIndex, entryA, entryB,entryC,
    vectorB):
        self.vectorV = vectorB. copy()
        
        self.vectorMainDiagonal = entryB. copy()
        self.vectorSubDiagonal = entryA. copy ()
        self.vectorSupDiagonal = entryC.copy ()
        
        for depthIndex in range (1, numberOfDepthIndex):
            self.variableM = self.vectorMainDiagonal [depthIndex - 1][0] /
            self.vectorSubDiagonal [depthIndex][0]
        
            self.vectorMainDiagonal [depthIndex][0] =
            self.vectorMainDiagonal [depthIndex][0] * (self.vectorMainDiagonal
            [depthIndex - 1][0] / self.vectorSubDiagonal [depthIndex][0]) -
            self.vectorSupDiagonal [depthIndex - 1][0]
            
            self.vectorSupDiagonal [depthIndex][0] = self.vectorSupDiagonal
            [depthIndex][0] * (self.vectorMainDiagonal [depthIndex - 1][0] /
            self.vectorSubDiagonal [depthIndex][0])
            
            self.vectorV [depthIndex][0] = self.vectorV [depthIndex][0] *
            (self.vectorMainDiagonal [depthIndex - 1][0] / self.vectorSubDiagonal
            [depthIndex][0]) - self.vectorV [depthIndex - 1][0]
            
            self.vectorX [numberOfDepthIndex - 1][0] = self.vectorV
            [numberOfDepthIndex - 1][0] / self.vectorMainDiagonal [numberOfDepthIndex -
            1][0]
        for depthIndex in range (numberOfDepthIndex - 2, -1, -1):
            self.vectorX [depthIndex][0] = (self.vectorV [depthIndex][0] -
            (self.vectorSupDiagonal [depthIndex][0]) * self.vectorX [depthIndex +
            1][0])/(self.vectorMainDiagonal [depthIndex][0])
        return self.vectorX