from itertools import combinations

def findAllCombos(target: int, amount: int, banned: list[int]):
    # generate all combinations
    allcombinations = []
    NUMLIST = [i for i in range(1, 9+1) if ((i < target) and not(i in banned))]
    for i in list(combinations(NUMLIST, amount)):
        if sum(i) == target:
            allcombinations.append([str(j) for j in i])

    # print each combo
    for combo in allcombinations:
        print(" ".join(combo))

    if not(allcombinations):
        print("Not Possible")
        return

    # find required numbers
    required = findRequired(NUMLIST, allcombinations)

    if not(required):
        print("No Required Numbers")
    else:
        print("Required Numbers: " + ", ".join(required))

    return

def findRequired(NUMLIST: list[int], combinations: list[str]) -> list[tuple[int]]:
    required = []

    if not(combinations):
        return required

    for num in NUMLIST:
        consistent = True
        for combo in combinations:
            if not(str(num) in combo):
                consistent = False
                break
        if consistent:
            required.append(str(num))

    return required

def getTarget() -> int:
    rawTarget: str = input("Input target: ")
    if (rawTarget == "" or rawTarget == "exit"): return 0
    return int(rawTarget)

def getNumbersRequired() -> int:
    rawRequired = ""
    while (rawRequired == ""):
        rawRequired = input("Numbers Required: ")
        if (rawRequired == "exit"):         return 0
        if (not(rawRequired.isnumeric())):  rawRequired = ""
    
    return int(rawRequired)

def getBannedNumbers() -> list[int]:
    rawBanned = ""
    while True:
        rawBanned = input("Banned Numbers (e.g. 1 2 3): ")
        if len(rawBanned) > 1 and not(" " in rawBanned):
            continue
        
        if (rawBanned == ""): return []
        try:
            banned = [int(i) for i in rawBanned.split(" ")]
            return banned
        except ValueError:
            continue
    return

if __name__ == "__main__":
    print("----- Killer Sudoku Cage Solver -----")
    print("Type 'exit' to stop")
    while True:
        target = getTarget()
        if (target == 0):           break

        numbersRequired = getNumbersRequired()
        if (numbersRequired == 0):  break

        banned = getBannedNumbers()

        findAllCombos(target, numbersRequired, banned)
        print("-------------------------------------")
    
    print("Ending...")

