from itertools import combinations
from typing import List, Dict, Any


def findAllCombos(target: int, amount: int, banned: List[int]) -> Dict[str, Any]:
    """
    Find all combinations of 'amount' numbers that sum to 'target', excluding banned numbers.
    
    Args:
        target: Target sum for the combination
        amount: Number of elements in each combination
        banned: List of numbers to exclude (must be 1-9, no duplicates)
    
    Returns:
        Dictionary with 'combinations' (list of lists), 'required_numbers', and 'error' (if any)
    """

    return_dict = {
        "combinations": [],
        "required_numbers": [],
        "error": ""
    }

    # Validate target range
    if not isValidTarget(target):
        return_dict["error"] = f"Target must be between 1 and {SUM_MAX}, got {target}"
        return return_dict
    
    # Validate and filter banned numbers
    valid_banned = processBanned(banned)
    
    # Create available numbers list (1-9 excluding banned, below target)
    NUMLIST = [i for i in range(1, 10) if i < target and i not in valid_banned]
    
    # Check if we can even form a combination with 'amount' numbers
    min_sum = sum(range(1, amount + 1))
    max_sum = sum(range(target - amount + 1, target + 1))
    
    if target < min_sum or target > max_sum:
        return_dict["error"] = f"Target {target} cannot be achieved with {amount} numbers"
        return return_dict
    
    # Generate all valid combinations
    all_combinations = []
    for combo in combinations(NUMLIST, amount):
        if sum(combo) == target:
            all_combinations.append(list(combo))  # Use list instead of string
    
    # If no combinations found, return error
    if not all_combinations:
        return_dict["error"] = f"No combinations found for target={target}, amount={amount}"
        return return_dict
    
    # Find required numbers (numbers that appear in ALL combinations)
    required = findRequired(NUMLIST, all_combinations)
    
    return_dict["combinations"] = all_combinations
    return_dict["required_numbers"] = required
    return_dict["error"] = None

    return return_dict


def findRequired(NUMLIST: List[int], combinations: List[List[int]]) -> List[int]:
    """
    Find numbers that appear in all given combinations.
    
    Args:
        NUMLIST: Available numbers (1-9)
        combinations: List of combination lists (not strings!)
    
    Returns:
        List of integers that appear in every combination
    """
    if not combinations:
        return []
    
    count: dict(int, int) = {i: 0 for i in NUMLIST}

    required: List[int] = []

    for combo in combinations:
        for number in combo:
            count[number] += 1
    
    for num, freq in count.items():
        if freq == len(combinations):
            required.append(num)

    return required


def getTarget() -> int:
    """Get target input from user with validation."""
    rawTarget: str = input(f"Input target (1-{SUM_MAX}): ")
    if rawTarget.strip() in ["", "exit", "EXIT", "quit", "QUIT"]: 
        return 0
    try:
        target = int(rawTarget)
        if not isValidTarget(target):
            print(f"Error: Target must be between 1 and {SUM_MAX}")
            return 0
        return target
    except ValueError:
        print(f"Error: '{rawTarget}' is not a valid integer")
        return 0


def getNumbersRequired() -> int:
    """Get number of required elements input from user."""
    while True:
        rawRequired = input("Numbers Required (1-9): ")
        if rawRequired.strip() in ["", "exit", "EXIT", "quit", "QUIT"]:
            return 0
        try:
            required = int(rawRequired)
            if not (1 <= required <= 9):
                print(f"Error: Numbers Required must be between 1 and 9")
                continue
            return required
        except ValueError:
            print(f"Error: '{rawRequired}' is not a valid integer")


def getBannedNumbers() -> List[int]:
    """Get banned numbers input from user with validation."""
    while True:
        rawBanned = input("Banned Numbers (e.g. 1 2 3, or enter none): ")
        if rawBanned.strip() in ["", "exit", "EXIT", "quit", "QUIT"]:
            return []
        
        try:
            # Split by whitespace and filter empty strings
            banned = [int(x) for x in rawBanned.split() if x]
            
            # Validate all banned numbers are in range 1-9 and unique
            invalid_banned = [b for b in banned if not (1 <= b <= 9)]
            duplicates = len(banned) - len(set(banned))
            
            if invalid_banned:
                print(f"Error: Banned numbers must be between 1 and 9. Found: {invalid_banned}")
                continue
            
            if duplicates > 0:
                banned_set = set(banned)
                for b in banned_set:
                    count = banned.count(b)
                    if count > 1:
                        print(f"Error: Duplicate banned number(s): {b} appears {count} time(s)")
                        continue
            
            return banned
        except ValueError:
            print(f"Error: Invalid number(s) in input")


def isValidTarget(target: int) -> bool:
    """Check if target is within valid range."""
    return 1 <= target <= SUM_MAX


def processBanned(banned: List[int]) -> List[int]:
    """Validate banned numbers are unique and in valid range."""
    # Filter to only keep valid banned numbers (1-9)
    valid = [b for b in banned if 1 <= b <= 9]
    # Remove duplicates while preserving order of first occurrence
    seen = set()
    for num in valid:
        seen.add(num)
        
    return list(seen)


def printResults(results: Dict[str, Any]):
    """Display the results in a formatted way."""
    if results.get("error"):
        print(f"Error: {results['error']}")
        return
    
    # Print combinations
    print("\nFound Combinations:")
    for i, combo in enumerate(results["combinations"], 1):
        print(f"  {i}. {combo}")
    
    if results.get("required_numbers"):
        print(f"Required Numbers: {', '.join(map(str, results['required_numbers']))}")
    else:
        print("Required Numbers: None")


# Constants
SUM_MAX = 45


if __name__ == "__main__":
    print("----- Killer Sudoku Cage Solver -----")
    print("Type 'exit', 'quit' to stop\n")
    
    while True:
        target = getTarget()
        if target == 0:
            break
        
        numbersRequired = getNumbersRequired()
        if (numbersRequired == 0):
            break

        banned = getBannedNumbers()
        
        # Find all valid combinations
        results = findAllCombos(target, numbersRequired, banned)
        
        # Display results
        printResults(results)
        
        print("\n-------------------------------------")
    
    print("Ending...")