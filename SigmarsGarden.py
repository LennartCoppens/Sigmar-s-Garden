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
    "Salt":         int("00000000011111", 2),
    "Air":          int("00000000000011", 2),
    "Earth":        int("00000000000101", 2),
    "Fire":         int("00000000001001", 2),
    "Water":        int("00000000010001", 2),
    "Vitae":        int("00000001000000", 2),
    "Mors":         int("00000000100000", 2),
    "Quicksilver":  int("01111100000000", 2),
    "Lead":         int("00000010000000", 2),
    "Tin":          int("00000010000000", 2),
    "Iron":         int("00000010000000", 2),
    "Copper":       int("00000010000000", 2),
    "Silver":       int("00000010000000", 2),
    "Gold":         int("00000000000000", 2)
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


# Game functions
##########################################################################################

def askForInputInt(lower, upper, text):
    while True:
        answer = input(text)
        try:
            if int(answer) >= lower and int(answer) <= upper:
                return int(answer)
            else:
                print("Input out of bounds")
        except ValueError:
            print("Unvalid input")

def boardSize(field):
    board = [[]]
    for y, _ in enumerate(field):
        if y:
            board.append([])
        for x, _ in enumerate(field[y]):
            if y+x >= (len(field)-1) / 2 and y+x <= len(field)-1 + ((len(field)-1) / 2):
                board[y].append('')
    return board

def canCombine(a, b):
    aCanTakeB = (possibleCombinations[a] >> elementsIndexed.index(b)) & 1
    bCanTakeA = (possibleCombinations[b] >> elementsIndexed.index(a)) & 1
    return aCanTakeB == 1 and bCanTakeA == 1

hexNeighbours = [(-1, 0), (-1, 1), (0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]   # (row, cell) offsets of the 6 neighbours

def elementFree(row, cell, field):
    freeCells = 0
    for dRow, dCell in hexNeighbours:
        r, c = row + dRow, cell + dCell
        if not (0 <= r < len(field) and 0 <= c < len(field[r])):
            freeCells += 1                                          # Outside the grid counts as free
        elif not field[r][c]:
            freeCells += 1
        else:
            freeCells = 0                                          # Empty cell
        if freeCells >= 3:
            return True
    return False

def boardToField(row, cell):
    # Converts the row/cell you see on the printed board to the index in currentField
    return row, cell + max(0, 5 - row)

def readChoice(label):
    row = askForInputInt(0, len(boardSize(currentField))-1, f"{label} element: (row)")
    cell = askForInputInt(0, len(boardSize(currentField)[row])-1, f"{label} element: (cell)")
    row, cell = boardToField(row, cell)
    return {'row': row, 'cell': cell}

def removeElements(elem1, elem2 = False):
    global elementsOnField
    currentField[elem1["row"]][elem1["cell"]] = 0
    elementsOnField -=1
    if elem2:
        currentField[elem2["row"]][elem2["cell"]] = 0
        elementsOnField -= 1
    printField(currentField)


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

    def randomElementPair(listOfElements = leftoverElements):
        firstElement = randomElement()
        secondElement = randomElement()
        while not canCombine(firstElement, secondElement) or not listOfElements[secondElement]:
            secondElement = elementsIndexed[(elementsIndexed.index(secondElement)+1)%(len(elementsIndexed)-1)]
        return (firstElement, secondElement)

    def positionFree(row, cell, field):
        freeCells = 0
        for dRow, dCell in hexNeighbours:
            r, c = row + dRow, cell + dCell
            if not (0 <= r < len(field) and 0 <= c < len(field[r])):
                freeCells += 1                                          # Outside the grid counts as free
            elif not field[r][c] == 1:
                freeCells += 1
            else:
                freeCells = 0                                          # Empty cell
            if freeCells >= 3:
                return True
        return False

    def allFreePositions(field):
        freePositions = []
        for y, _ in enumerate(field):
            for x, cell in enumerate(field[y]):
                if cell == 1 and positionFree(y,x,field):
                    freePositions.append((y,x))
        return freePositions



    insertElement(round(numOfRows/2)-1, round(numOfColums/2)-1)     # Insert Gold in the middle of the field to start

    nextPositionsToFill = allFreePositions(field)
    while len(nextPositionsToFill):
        a, b = randomElementPair()
        ya, xa = nextPositionsToFill[randint(0, len(nextPositionsToFill)-1)]
        yb, xb = nextPositionsToFill[randint(0, len(nextPositionsToFill)-1)]
        while ya == yb and xa == xb:
            yb, xb = nextPositionsToFill[randint(0, len(nextPositionsToFill)-1)]
        insertElement(ya, xa, a)
        insertElement(yb, xb, b)
        nextPositionsToFill = allFreePositions(field)

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
        r"'-._ _.-'"
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
        leadToGold = 0
        currentField = generateField()
        printField(currentField)
        elementsOnField = 0
        for y in currentField:
            for x in y:
                if x:
                    elementsOnField += 1

        while gameGoing:
            if elementsOnField:

                print("Choose two elements")
                firstChoice = readChoice("First")
                element1 = currentField[firstChoice['row']][firstChoice['cell']]
                print(element1)

                if element1 == "Gold" and leadToGold >= 5:
                    if elementFree(firstChoice["row"], firstChoice["cell"], currentField):
                        removeElements(firstChoice)
                    else:
                        print("Gold is not free")
                else:
                    secondChoice = readChoice("Second")
                    element2 = currentField[secondChoice['row']][secondChoice['cell']]
                    print(element2)

                    if not (element1 and element2):
                        print("One of the chosen cells is empty")
                    elif firstChoice == secondChoice:
                        print("You chose the same cell twice")
                    elif not canCombine(element1, element2):
                        print(f"{element1} and {element2} can't be combined")
                    elif not elementFree(firstChoice["row"], firstChoice["cell"], currentField):
                        print(f"The first element ({element1}) is not free")
                    elif not elementFree(secondChoice["row"], secondChoice["cell"], currentField):
                        print(f"The second element ({element2}) is not free")
                    elif element1 == "Quicksilver" or element2 == "Quicksilver":
                        metal = element2 if element1 == "Quicksilver" else element1
                        if elementsIndexed.index(metal) <= elementsIndexed.index("Lead") + leadToGold:
                            leadToGold += 1
                            removeElements(firstChoice, secondChoice)
                        else:
                            print(f"{metal} is not the next metal to remove")
                    else:
                        removeElements(firstChoice, secondChoice)

            else:
                print("You won!")
                gameGoing = False



