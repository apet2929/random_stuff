def getMultiples(start, max) -> list[int]:
    nums = []
    for i in range(start, max):
        if i % 3 == 0 or i % 5 == 0:
            nums.append(i)
    return nums

def addNums(nums):
    finalNum = 0
    for num in nums:
        finalNum += num
    return finalNum

def addEvenNums(nums):
    sum = 0
    for i in range(len(nums)):
        if nums[i] % 2 == 0:
            sum += nums[i]
    return sum
def fibonacci(max) -> list[int]:
    nums = []
    cont = True
    nums.append(1)
    nums.append(1)
    i = 2
    while cont:
        nums.append(nums[i-2] + nums[i-1])
        if nums[i] > max:
            nums.pop()
            return nums
        i+=1

def findFactors(num):
    factors = []
    for i in range(1, 10000, 2):
        if num % i == 0:
            n = num/i
            if not(i in factors or n in factors):
                factors.append(i)
                factors.append(n)

def findPrimes(nums):
    primes = []
    for i in range(1000):
        if len(findFactors(nums[i])) == 0:
            primes.append(nums[i])
    return primes

def findHighest(nums):
    highest = 0
    for num in nums:
        if num > highest:
            highest = num
    return highest

def findPrimeNumbers(maxNum):
    divideBy = [2, 3, 5, 7, 11]
    primes = divideBy.copy()
    for i in range(13, maxNum):
        prime = True
        for num in divideBy:
            if i % num == 0:
                prime = False
        if prime:
            primes.append(i)

    for num in primes:
        for i in range(11, int(num/2), 2):
            if num % i == 0:
                primes.remove(num)

    return primes

num = 600851475143 
factors = findFactors(num)
print("Factors: " + str(factors))
primeFactors = findPrimes(factors)
print("Prime Factors : " + str(primeFactors))
print(findHighest(primeFactors))
# primes = findPrimeNumbers(600851475143)
# print(primes)
# print(max(primes))
# print(addEvenNums(nums))