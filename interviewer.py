#author Daniel & Ryan
import util, sys
from layout import Layout
from pacman import GameState
from game import GameStateData
from game import Game
from game import Directions
from game import Actions
from random import randint
from random import seed
import featureGenerator
import numpy as np

#TODO
############# Remove this part when featureGenerator.py is finished #######################
class gameData:
    def __init__(self, args, chromosome = None):
        self.initialize(args)
        if chromosome != None:
            while satisfyFeatures(generateFeatures(), self, chromosome) == False:
                self.initialize(args)
    def initialize(self, args):
        self.mazeHeight = args['mazeHeight']
        self.mazeLength = args['mazeLength']
        if args['posPacman'] is None:
            self.posPacman = randint(1, self.mazeLength)
        else:
            self.posPacman = args['posPacman']
        if args['posGhost'] is None:
            self.posGhost = (((self.posPacman-1+randint(1, self.mazeLength-1)))%self.mazeLength) + 1
        else:
            self.posGhost = args['posGhost']
        self.listFood = []
        self.listCapsule = []
        for k in range(1,self.mazeLength+1): #randomization of food and capsules
            if k == self.posPacman or k == self.posGhost:
                continue
            #random.seed(0)
            randomInt = randint(0,2)
            if randomInt == 1:
               self.listCapsule.append(k)
            elif randomInt == 2:
               self.listFood.append(k)



class Feature:
    def __init__(self, closure):
        self.func = closure
    def satisfy(self, gameData):
        return self.func(gameData)

def satisfyFeatures(feature, gameData, chromosome):
    for feature in features:
        if features[feature].satisfy(gameData) is not chromosome[feature]:
            return False
    return True

def isNear(pos1, pos2, near):
    if (abs(pos1 - pos2)<= near):
        return True
    return False

def atEast(pos1, pos2):
    if (pos1 > pos2):
        return True
    return False
    
def atCorner(pos, length):
    if(pos == 1 or pos == length):
        return True
    return False

def pacmanAtCorner(gameData):
    return atCorner(gameData.posPacman, gameData.mazeLength)

def ghostIsNear(gameData):
    return isNear( gameData.posGhost, gameData.posPacman, near = 1 )

def ghostAtEast(gameData):
    return atEast(gameData.posGhost, gameData.posPacman)

def ghostAtCorner(gameData):
    return atCorner(gameData.posGhost, gameData.mazeLength)

def closestFoodIsNear(gameData, near = 1):
    return util.closest(gameData.listFood,args['mazeLength'],gameData) <= near

def closestFoodAtEast(gameData):
    closestList = util.closestList(gameData.listFood,args['mazeLength'],gameData)
    if(len(closestList)==1):
        if(gameData.posPacman > closestList[0]):
            return False
    return True
    
def closestCapsuleIsNear(gameData, near = 1):
    return util.closest(gameData.listCapsule, args['mazeLength'], gameData) == near

def closestCapsuleAtEast(gameData):
    closestList = util.closestList(gameData.listCapsule,args['mazeLength'],gameData)
    if(len(closestList)==1):
        if(gameData.posPacman > closestList[0]):
            return False
    return True
############# Remove this part when featureGenerator.py is finished #######################

def generateChromosome(chromosomeString = '0000000'):
    chromosome = dict.fromkeys(features.keys(),False)
    keys = chromosome.keys()
    for k in range (0,len(keys)):
        if chromosomeString[k] == '0':
            chromosome[keys[k]] = False
        else:
            chromosome[keys[k]] = True
    return chromosome

def generateAllChromosomes(chromosomeNumber):
    allChromosomes = []
    for k in range(0, 2**(chromosomeNumber)):
        binaryvalue = str('{0:07b}'.format(k))
        allChromosomes.append(generateChromosome(binaryvalue))
    return allChromosomes

def testChromosomes(chromosomeNumber, args, testlimit):
    allChromosomes = generateAllChromosomes(chromosomeNumber)
    features = generateFeatures()
    badChromosomes = []
    goodChromosomes = []
    for k in allChromosomes:
        gameStates = []
        for x in range (0, testlimit):
            data = gameData(args)
            if(satisfyFeatures(features, data, k)):
                gameStates.append(data)
        if len(gameStates) == 0:
            badChromosomes.append(k)
        else:
            goodChromosomes.append(k)
    #print "The contradictory chromosomes are:"
    #printChromosomeList(badChromosomes)
    return goodChromosomes, badChromosomes


def printChromosome(chromosome):
    binarystring = ""
    for x in chromosome.values():
        if x:
            binarystring+= '1'
        else:
            binarystring+= '0'
    print binarystring

def printChromosomeList(chromosomes):
    for k in chromosomes:
        printChromosome(k)

def generateFeatures():
    features = {}
    features['ghostIsNear'] = Feature(ghostIsNear)
    features['ghostAtEast'] = Feature(ghostAtEast)
    features['closestFoodIsNear'] = Feature(closestFoodIsNear)
    features['closestFoodAtEast'] = Feature(closestFoodAtEast)
    features['closestCapsuleIsNear'] = Feature(closestCapsuleIsNear)
    features['closestCapsuleAtEast'] = Feature(closestCapsuleAtEast)
    #features['pacmanAtCorner'] = Feature(pacmanAtCorner)
    return features
    
def generateLayout(gameData):
    height = gameData.mazeHeight
    length = gameData.mazeLength
    posPacman = gameData.posPacman 
    posGhost = gameData.posGhost 
    listFood = gameData.listFood
    listCapsule = gameData.listCapsule

    layoutText = [None]*(2+height)
    wall = "%"*(length+2)
    layoutText[0] = wall
    layoutText[height+1] = wall

    for x in range(1,(height+1)):
        row = "%"

        for k in range(1,(length+1)):
            if k == posPacman:
                row += "P"
            elif k == posGhost:
                row += "G"
            elif k in listFood:
                row += "."
            elif k in listCapsule:
                row += "o"
            else:
                row += " "

        row += "%"
        layoutText[x] = row

    return Layout(layoutText)

def generateGameState(args): 
    layout =  generateLayout(args)
    gameState = GameState()
    numGhostAgents = 1
    gameState.initialize(layout, numGhostAgents)
    return gameState
    

def getAction(gameState):
    import pacmanAgents, qlearningAgents
    pacmanAgent = pacmanAgents.GreedyAgent()
    action = pacmanAgent.getAction(gameState)
    return action

def default(string):
  return string + ' [Default: %default]'

def readCommand(argv):

    from optparse import OptionParser

    usageStr = ""
    parser = OptionParser(usageStr)

    parser.add_option('--mazeLength', dest = 'mazeLength', type='int',
                      help = default('the length of the maze'), default = 10)
    parser.add_option('--mazeHeight', dest = 'mazeHeight', type='int',
                      help = default('the height of the maze'), default = 1)
    parser.add_option('--posPacman', dest = 'posPacman', type='int',
                      help = default('the position of pacman in a horizontal maze'), default = None)
    parser.add_option('--posGhost', dest = 'posGhost', type='int',
                      help = default('the position of the ghost in a horizontal maze'), default = None)
    parser.add_option('--numLayouts' ,dest = 'numLayouts', type='int',
                      help = default('the number of layouts to be generated'), default = 10 )

    options, otherjunk = parser.parse_args(argv)

    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))

    args = dict()

    args['mazeLength'] = options.mazeLength
    args['mazeHeight'] = options.mazeHeight
    args['posPacman'] = options.posPacman
    args['posGhost'] = options.posGhost
    args['numLayouts'] = options.numLayouts
    return args

def getFeatures(chromosome):
    fullFeature = ''
    for feature in features:
        if chromosome[feature] is False: 
            fullFeature = fullFeature + 'Not'
        fullFeature = fullFeature + str(feature)+', ' 
    return fullFeature

def chromosome2bit(chromosome):
    l = []
    for x in chromosome.values():
        if x:
            l.append(1)
        else:
            l.append(0)
    return l

args = readCommand( sys.argv[1:] )
features = generateFeatures()

goodChromosomes, badChromosomes = testChromosomes(len(generateChromosome()), args, 1000)
def printContradictRules():
    print 'Contradict rules:'
    for chromosome in badChromosomes:
        print getFeatures(chromosome)

goEastChromosomes = []
goWestChromosomes = []
repeat = 10
successRate = 0.9
for chromosome in goodChromosomes:
    goEast = goWest = 0 
    #print ''
    #print getFeatures(chromosome) 
    for i in range(0,repeat):
        gameState = generateGameState(gameData(args, chromosome))
        action = getAction(gameState)
        if action == 'West':
            goWest = goWest+1
        if action == 'East':
            goEast = goEast+1
        #print gameState
        #print action
        #print 'goEast: '+str(goEast)+', goWest: '+str(goWest)
    if goEast >= repeat*successRate:
        goEastChromosomes.append(chromosome)
    if goWest >= repeat*successRate:
        goWestChromosomes.append(chromosome)
'''
print'\nPacman goes East when: '
for chromosome in goEastChromosomes:
    print generateGameState(gameData(args, chromosome))
    print getFeatures(chromosome)
print'\nPacman goes West when: '
for chromosome in goWestChromosomes:
    print generateGameState(gameData(args, chromosome))
    print getFeatures(chromosome)
'''


def findMI(chromosomes):
    sum_list = [sum(x) for x in zip(*chromosomes)]
    p_list = [float(sum(x))/len(chromosomes) for x in zip(*chromosomes)]
    print sum_list, p_list

def calc_MI(X,Y,bins):
    c_XY = np.histogram2d(X,Y,bins)[0]
    c_X = np.histogram(X,bins)[0]
    c_Y = np.histogram(Y,bins)[0]

    H_X = shan_entropy(c_X)
    H_Y = shan_entropy(c_Y)
    H_XY = shan_entropy(c_XY)

    MI = H_X + H_Y - H_XY
    return MI

def shan_entropy(c):
    c_normalized = c / float(np.sum(c))
    c_normalized = c_normalized[np.nonzero(c_normalized)]
    H = -sum(c_normalized* np.log2(c_normalized))
    return H

def calc_matMI(A):
    n = A.shape[1]
    bins = n  
    matMI = np.zeros((n,n))
    for ix in np.arange(n):
        for jx in np.arange(ix+1, n):
            matMI[ix, jx] = calc_MI(A[:, ix], A[:,jx], bins)
    return matMI

np.set_printoptions(suppress=True, precision=3)

bitLists = []
print'\nPacman goes East: '+str(len(goEastChromosomes))
for chromosome in goEastChromosomes:
    bitChromosome = chromosome2bit(chromosome)
    bitLists.append(bitChromosome)
    print bitChromosome, getFeatures(chromosome)
print calc_matMI(np.array(bitLists))

bitLists = []
print'\nPacman goes West: '+str(len(goWestChromosomes))
for chromosome in goWestChromosomes:
    bitChromosome = chromosome2bit(chromosome)
    bitLists.append(bitChromosome)
    print bitChromosome, getFeatures(chromosome)
print calc_matMI(np.array(bitLists))




'''for k in range(0,args['numLayouts']):
    data = gameData(args)
    features = generateFeatures()
    # TODO
    # randomly generate chromosome until all(most) of the chromosome(features) have the same action
    # then extract the same features in the chromosome and combine them as a new feature
    chromosome = generateChromosome()
    data = gameData(args, chromosome)
    gameState = generateGameState(data)
    print gameState

    fullFeature = ""
    for feature in features:
        if not chromosome[feature]: 
            fullFeature = fullFeature + 'Not'
        fullFeature = fullFeature + str(feature)+', ' 

    print 'When: '+fullFeature+'Pacman goes: ' + getAction(gameState) + "\n"'''

'''
def generateGameStates(gameData):
    listGameStates = []
    randomSeed = 0
    for repeat in range (0, gameData['numLayouts']):
        if ghostRule(gameData):
            gameState = generateGameState(gameData)
            if gameState not in usedGameStates:
                listGameStates.append(gameState)
                usedGameStates.append(gameState)
    return listGameStates
'''
