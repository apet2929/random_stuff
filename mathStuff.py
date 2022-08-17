def square_sum_of_digits(number: int):
    _sum = get_sum_of_digits(number)
    return _sum**2

def get_sum_of_digits(number: int):
    numStr = str(number)
    _sum = 0
    for digit in numStr:
        _sum += int(digit)
    return _sum

def square_sums_until_81(startingNumber):
    seen_numbers: list[int] = []
    recursions = 0
    doContinue = True
    current_number = startingNumber
    while doContinue:
        if recursions > 10000:
            print(f"startingNumber {startingNumber} goes for a long time!")
            return

        current_number = square_sum_of_digits(current_number)
        
        if current_number not in seen_numbers:
            seen_numbers.append(current_number)
        else:
            doContinue = False
            print(startingNumber, ",", seen_numbers)
        recursions += 1


if __name__ == "__main__":
    for i in range(9999999):
        square_sums_until_81(i)
