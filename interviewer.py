#author Daniel & Ryan
import util
from layout import Layout
from pacman import GameState
from game import GameStateData
from game import Game
from game import Directions
from game import Actions

mazeHeight = 1
mazeLength = 5
posPacman = 1
posGhost = 4
numLayouts = 10
listFood = []
listCapsule = []
seed = 0
gameData = dict(mazeLength = mazeLength, posPacman = posPacman, 
            posGhost = posGhost, listFood = listFood, listCapsule = listCapsule, seed = seed)

usedGameStates = []

def generateGameData(seed):
    gameData = [mazeLength, posPacman, posGhost, listFood, listCapsule]
    return gameData
    
def ghostRule(gameData):
    return True

def generateLayout():
    layoutText = [None]*(2+mazeHeight)

    wall = ""
    for k in range(0,(mazeLength+2)):
        wall += "%"


    layoutText[0] = wall
    layoutText[mazeHeight+1] = wall

    for x in range(1,(mazeHeight+1)):
        row = "%"

        for k in range(1,(mazeLength+1)):
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

def generateGameState(gameData): 
    #gamestate = GameState(generateLayout())
    #layout = generateLayout(gameData)
    layoutName = 'test1D' 
    layout = generateLayout()
    gameState = GameState()
    numGhostAgents = 1
    gameState.initialize(layout, numGhostAgents)
    print gameState
    return gameState
    
def generateGameStates():
    listGameStates = []
    randomSeed = 0
    for repeat in range (0, numLayouts):
        gameData = generateGameData(randomSeed)
        if ghostRule(gameData):
            gameState = generateGameState(gameData)
            if gameState not in usedGameStates:
                listGameStates.append(gameState)
                usedGameStates.append(gameState)
    return listGameStates

def getAction(gameState):
    import pacmanAgents, qlearningAgents
    pacmanAgent = pacmanAgents.GreedyAgent()
    action = pacmanAgent.getAction(gameState)
    return action

def readCommand(argv):

    from outparse import OptionParser

    usageStr = ""
    parser = OptionParser(usageStr)

    parser.add_option('-ml', '--mazeLength', 'mazeLength', type='int', dest= 'mazeLength',
                      help = default('the length of the maze'), default = 5)
    parser.add_option('-mh', '--mazeHeight', 'mazeHeight', type='int', dest= 'mazeHeight',
                      help = default('the height of the maze'), default = 1)
    parser.add_option('-pp', '--posPacman', 'posPacman', type='int', dest= 'posPacman',
                      help = default('the position of pacman in a horizontal maze'), default = None)
    parser.add_option('-pg', '--posGhost', 'posGhost', type='int', dest= 'posGhost',
                      help = default('the position of the ghost in a horizontal maze'), default = None)
    parser.add_option('-nl','--numLayouts' ,'numLayouts', type='int', dest= 'numLayouts',
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
args = readCommand( sys.argv[1:] )
for k in range(0,numLayouts):
    print 'Pacman Action: '+getAction(generateGameState(args))