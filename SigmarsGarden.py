###################
# Sigmar's Garden #
###################

# author: Lennart Coppens
# version: 1.0


#                 SAEFWVMQLTICSG    
# Salt          : 11111000000000
# Air           : 11000000000000
# Earth         : 10001000000000
# Fire          : 10100000000000
# Water         : 10010000000000
# Vitae         : 00000100000000
# Mors          : 00001000000000
# Quicksilver   : 00000000111110
# Lead          : 00000001000000
# Tin           : 00000001000000
# Iron          : 00000001000000
# Copper        : 00000001000000
# Silver        : 00000001000000
# Gold          : 00000000000000


elementsIndexed = [
    "Salt",
    "Air",
    "Earth",
    "Fire",
    "Water",
    "Vitae",
    "Mors",
    "Quicksilver",
    "Lead",
    "Tin",
    "Iron",
    "Copper",
    "Silver",
    "Gold"
]
possibleCombinations = {
    "Salt": 15872,
    "Air": 12288,
    "Earth": 8192,
    "Fire": 16384,
    "Water": 10240,
    "Vitae": 32768,
    "Mors": 8192,
    "Quicksilver": 3072,
    "Lead": 4096,
    "Tin": 4096,
    "Iron": 4096,
    "Copper": 4096,
    "Silver": 4096,
    "Gold": 0
}

elementAmounts = {
    "Salt": 4,
    "Air": 8,
    "Earth": 8,
    "Fire": 8,
    "Water": 8,
    "Vitae": 4,
    "Mors": 4,
    "Quicksilver": 5,
    "Lead": 1,
    "Tin": 1,
    "Iron": 1,
    "Copper": 1,
    "Silver": 1,
    "Gold": 1
}

elementSymbols = {
    # name:        (symbol, color)
    "Salt":        ("🜔", "\033[97m"),        # white
    "Air":         ("🜁", "\033[38;5;195m"),  # very light blue
    "Fire":        ("🜂", "\033[91m"),        # red
    "Water":       ("🜄", "\033[36m"),        # teal
    "Earth":       ("🜃", "\033[92m"),        # green
    "Quicksilver": ("☿", "\033[37m"),        # silver-grey
    "Lead":        ("♄", "\033[90m"),        # dark grey
    "Tin":         ("♃", "\033[37m"),        # light grey
    "Iron":        ("♂", "\033[31m"),        # dark red
    "Copper":      ("♀", "\033[38;5;208m"),  # orange
    "Silver":      ("☽", "\033[37m"),        # silver-grey
    "Gold":        ("☉", "\033[93m"),       # yellow
    "Vitae":       ("⍋", "\033[38;5;218m"), # pink
    "Mors":        ("⍒", "\033[90m"),       # dark grey
}

resetColor = "\033[0m"

testField = [
    [0,0,0,0,0,1,1,0,0,0,0],
    [0,0,0,0,1,1,1,0,0,0,1],
    [0,0,0,1,0,1,1,0,0,1,1],
    [0,0,1,0,1,1,1,1,1,0,1],
    [0,1,1,1,1,1,0,1,1,0,1],
    [0,0,0,1,0,1,1,1,1,1,1],
    [0,0,0,1,1,0,1,1,1,1,0],
    [0,0,1,1,1,1,0,0,0,0,0],
    [0,1,1,1,1,0,0,0,0,0,0],
    [1,1,0,0,1,0,0,0,0,0,0],
    [1,1,1,1,1,0,0,0,0,0,0]
]


# Field generation
##########################################################################################


numOfRows = 11
numOfColums = 11

def generateField(fieldTemplate = testField, elementsPool = elementAmounts):
    from random import randint
    import copy

    field = copy.deepcopy(fieldTemplate)
    leftoverElements = copy.deepcopy(elementsPool)

    def insertElement(row, colum, element = 'Gold'):
        if leftoverElements[element]:                               # Check if the element is available
            field[row][colum] = element                             # Add it to the correct position in the field
            leftoverElements[element] -= 1                          # Subtract 1 from available elements
            return True                                             # Return True if succesfull
        return False                                                # Return False if not succesfull

    def randomElement(listOfElements = leftoverElements):
        availableElements = list(i for i in listOfElements if listOfElements[i])    # Makes a list of all keys in the dictionary where the value doesn't equal zero         
        return availableElements[randint(0, len(availableElements)-1)]              # Takes a random index from this list and returns the corresponding element


    insertElement(round(numOfRows/2)-1, round(numOfColums/2)-1)     # Insert Gold in the middle of the field to start

    for y in range(len(field)):
        for x in range(len(field[y])):
            if field[y][x] == 1:
                insertElement(y, x, randomElement())
    return field


# Field visualization
##########################################################################################

def printField(field):
    SIZE = 6  # cells along each edge of the big hexagon

    CELL = [
        r" _.-'-._ ",
        r"|       |",
        r"|       |",
        r"'-._ _.-' ",
    ]

    rows = 2 * SIZE - 1
    canvas = [[" "] * (rows * 8 + 2) for _ in range(rows * 3 + 1)]

    def fieldToTerminalFormat(fieldList):
        outputField = [[''] * ((2*SIZE - 1) - abs(row - (SIZE - 1)))
                    for row in range(2*SIZE - 1)]
        for y, row in enumerate(fieldList):
            for x, cell in enumerate(row):
                if SIZE - 1 <= x + y <= 3*SIZE - 3:
                    outputField[y][x + min(0, y - (SIZE - 1))] = cell
        return outputField

    def draw(x, y, lines, element):
        # x, y are canvas (character) coordinates; element is the cell's content
        for dy, line in enumerate(lines):
            for dx, ch in enumerate(line):
                if ch != " ":
                    canvas[y + dy][x + dx] = ch
        if element:
            symbol, color = elementSymbols[element]
            canvas[y+1][x+4] = f"{color}{symbol}{resetColor}"

    terminalField = fieldToTerminalFormat(field)

    for r in range(rows):
        distance_from_middle = abs(r - (SIZE - 1))
        cells_in_row = rows - distance_from_middle

        for c in range(cells_in_row):
            x = distance_from_middle * 4 + c * 8
            y = r * 3
            draw(x, y, CELL, terminalField[r][c])

    for line in canvas:
        print("".join(line).rstrip())

    return


# Gameloop
##########################################################################################

newGame = False
gameGoing = False
quitGame = False

while not quitGame:
    gameGoing = newGame or gameGoing

    while not (newGame or quitGame):
        answer = input("Wanna start a new game? [y/n]")
        newGame = answer == 'y'
        quitGame = answer == 'n'

    if gameGoing:
        newGame = False
        currentField = generateField()
        printField(currentField)
        gameGoing = False
