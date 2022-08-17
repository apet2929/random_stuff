class Paige:
    def __init__(self, name):
        self.name = name
        self.sleeping = False
        self.clean = True
        self.hunger = 20
        self.energy = 70
    

    def eat(self):
        self.hunger -= 10
        self.energy += 10

        return self.hunger
    

    def sleep(self):
        self.energy += 10
        self.sleeping = True
    



def cheesecake():
    global sabrina
    urname = str(input("what is your name? "))
    sabrina = Paige(urname)
    print("this kitty is named " + sabrina.name)
    sabrina.sleep()
    print("she is " + str(sabrina.hunger) + " hungry.")
    print("i have " + str(8) + " eggs and " + str(7) + " grass and " + str(6) + " friends.")


cheesecake()

for i in range(10):
    if i == 2 :
        print(i)
    

    elif i < 5 :
        print("eeee")
    

    else :
        print(i ** 2)
    


while sabrina.hunger >= 5:
    sabrina.eat()


print("yee")
