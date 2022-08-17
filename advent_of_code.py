def day_1():
    def part_1(lines):
        cnt = 0
        prev_val = 999999999
        for line in lines:
            val = int(line)
            if val > prev_val:
                cnt+=1
            prev_val = val
        return cnt
    
    def part_2(lines):
        cnt = 0
        prev_val = 999999999
        slides: list[int] = [] #   Sum of 3 values
        
        for i in range(len(lines)-2):
            val = int(lines[i]) + int(lines[i+1]) + int(lines[i+2])
            slides.append(val)
        
        return part_1(slides)

    with open("assets/day1.txt") as data:
        lines = data.readlines()
        print(part_2(lines))

def day_2():
    # https://adventofcode.com/2021/day/2
    def part_1(lines):
        x = 0   #   Horizontal position
        d = 0   #   Depth
        
        for line in lines:
            command = line.split()
            if command[0] == "up":
                d -= int(command[1])
            elif command[0] == "down":
                d += int(command[1])
            elif command[0] == "forward":
                x += int(command[1])
        
        print(x, d, x * d)

    def part_2(lines):
        x = 0
        d = 0
        aim = 0

        for line in lines:
            command = line.split()
            if command[0] == "up":
                aim -= int(command[1])
            elif command[0] == "down":
                aim += int(command[1])
            elif command[0] == "forward":
                x += int(command[1]) 
                d += int(command[1]) * aim
            
        print(x, d, x * d)

    with open("assets/day2.txt") as data:
        part_2(data.readlines())

if __name__ == "__main__":
    day_2()