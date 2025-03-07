# I am using Turtle library for this project.
# I am using a Queue to note down the last 5 Coordinates of each ant i.e. where the pheromone is currently active.
# If any ant's coordinates overlap with that present in the queue then I am using a Random function to get any random number between 0 and 1 which when is greater than 0.8 belongs to 20% probability and if less than equal to 0.8 belongs to 80% probablility.
# There are two methods "move" and "move_dash" defined for the movement of the ant.
# "move" denotes the usual movement when no pheromone is detected i.e. it turns right when a white square is detected and turns left when a black square is detected and then moves.
# "move_dash" denotes the movement when pheromone is detected and it moves forward.
# "add_ant" method adds the ants to the "ants" list.
# "get_coordinate" method tells the present coordinate of the ant.
# "invert" method inverts the colour of the coordinate its told to.
# "check_and_bounce" method reverses the direction of the ant if it hits a boundary
# "check_collision" method checks if two ants are about to collide or not by checking the distance between them.
# "handle_collision" method handles the collision situation by reversing the direction of the ant 
# If an ant goes on a pheromone of its own or on others then the queue which contains the coordinate of this location gets updated to (1001,1001) which is out of the screen and the queue of the ant which is currently at this location gets the coordinate added.
# I used random to get random coordinates for both ants and also to get random probability to check how to move
# "maps" is a dictionary used to store the colour of squares

import turtle
from collections import deque
import random



queue1 = deque()
queue2 = deque()


class Ant:
    def __init__(self, x, y):
        self.turtle = turtle.Turtle()
        self.turtle.shape("square")
        self.turtle.shapesize(0.5)
        self.turtle.speed(0)
        self.turtle.penup()
        self.turtle.setpos(x, y)
        self.turtle.pendown()

    def move(self, step, maps, other_ant=None):  
        pos = self.get_coordinate()
        if pos not in maps or maps[pos] == "white":
            self.turtle.fillcolor("black")
            self.turtle.stamp()
            self.invert(maps, "black")
            self.turtle.right(90)
        else:
            self.turtle.fillcolor("white")
            self.turtle.stamp()
            self.invert(maps, "white")
            self.turtle.left(90)
        self.turtle.forward(step)
        self.check_and_bounce()

        if other_ant and self.check_collision(other_ant): # Check collision after move
            self.handle_collision(other_ant)


    def move_dash(self, step, maps, other_ant=None): 
        pos = self.get_coordinate()
        if maps[pos] == "white":
            self.turtle.fillcolor("black")
            self.turtle.stamp()
            self.invert(maps, "black")
        else:
            self.turtle.fillcolor("white")
            self.turtle.stamp()
            self.invert(maps, "white")
        self.turtle.forward(step)
        self.check_and_bounce()

        if other_ant and self.check_collision(other_ant): # Check collision after move
            self.handle_collision(other_ant)
            

    def check_and_bounce(self):
        x = self.turtle.xcor()
        y = self.turtle.ycor()

        if x > 500 or x < -500:
            self.turtle.setheading(-self.turtle.heading())
        if y > 500 or y < -500:
            self.turtle.setheading(-self.turtle.heading())

    def get_coordinate(self):
        return (round(self.turtle.xcor()), round(self.turtle.ycor()))

    def invert(self, maps, color):
        maps[self.get_coordinate()] = color

    def check_collision(self, other_ant, distance_threshold=10):
        x1, y1 = self.get_coordinate()
        x2, y2 = other_ant.get_coordinate()
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        return distance < distance_threshold

    def handle_collision(self, other_ant):
        self.turtle.setheading(-self.turtle.heading())  # Reverse direction
        other_ant.turtle.setheading(-other_ant.turtle.heading())
        self.turtle.forward(20)  # Move a little to separate
        other_ant.turtle.forward(20)

class LangtonSimulation:
    def __init__(self, width=1000, height=1000):
        self.window = turtle.Screen()
        self.window.bgcolor("white")
        self.window.screensize(width, height)
        self.window.tracer(0)
        self.maps = {}  # Dictionary to store cell colors
        self.ants = []  
        
    def add_ant(self, x, y):
        ant = Ant(x, y)
        self.ants.append(ant)

    def run(self, max_steps=1000):
        step = 10  # Distance the ant will move
        step_count = 0

        try:
            while step_count < max_steps:               
                first_ant_coordinate = self.ants[0].get_coordinate()
                second_ant_coordinate = self.ants[1].get_coordinate()

                if first_ant_coordinate in queue1:           
                    random_number = random.random()
                    a=0
                    for j in range(len(queue1)):
                        if queue1[j] == first_ant_coordinate:
                            a=j
                    if random_number>=(0.8-(4-a)*0.16):
                        self.ants[0].move(step, self.maps, self.ants[1])
                    else:
                        self.ants[0].move_dash(step, self.maps, self.ants[1])
                    for i in range(len(queue1)):
                        if queue1[i] == first_ant_coordinate:
                            queue1[i] = (1001,1001)
                elif first_ant_coordinate in queue2:
                    random_number = random.random()
                    b=0
                    for k in range(len(queue2)):
                        if queue2[k] == first_ant_coordinate:
                            b=k
                    if random_number>=(0.8-(4-b)*0.16):
                        self.ants[0].move_dash(step, self.maps, self.ants[1])
                    else:
                        self.ants[0].move(step, self.maps, self.ants[1])
                    for i in range(len(queue2)):
                        if queue2[i] == first_ant_coordinate:
                            queue2[i] = (1001,1001) 
                else:
                    self.ants[0].move(step, self.maps, self.ants[1])
                        
                if second_ant_coordinate in queue2:           
                    random_number = random.random()
                    a=0
                    for j in range(len(queue2)):
                        if queue1[j] == second_ant_coordinate:
                            a=j
                    if random_number>=(0.8-(4-a)*0.16):
                        self.ants[1].move(step, self.maps, self.ants[0])
                    else:
                        self.ants[1].move_dash(step, self.maps, self.ants[0])
                    for i in range(len(queue2)):
                        if queue1[i] == second_ant_coordinate:
                            queue1[i] = (1001,1001)
                elif second_ant_coordinate in queue1:
                    random_number = random.random()
                    b=0
                    for k in range(len(queue1)):
                        if queue1[k] == second_ant_coordinate:
                            b=k
                    if random_number>=(0.8-(4-b)*0.16):
                        self.ants[1].move_dash(step, self.maps, self.ants[0])
                    else:
                        self.ants[1].move(step, self.maps, self.ants[0])
                    for i in range(len(queue1)):
                        if queue1[i] == second_ant_coordinate:
                            queue1[i] = (1001,1001)
                else:
                    self.ants[1].move(step, self.maps, self.ants[0])
                
                queue1.append(first_ant_coordinate)
                queue2.append(second_ant_coordinate)

                if len(queue1) > 5:
                    queue1.popleft()
                    queue2.popleft()
               
                step_count += 1
                self.window.update()
        except turtle.Terminator:
            print("Simulation terminated.")

        
        
# Run the simulation
if __name__ == "__main__":
    simulation = LangtonSimulation()
    x1 = random.randint(-200, 200) # Getting random coordinates
    x2 = random.randint(-200, 200)
    y1 = random.randint(-200, 200)
    y2 = random.randint(-200, 200)
    simulation.add_ant(x1, y1)  # Add Ant 1
    simulation.add_ant(x2, y2)   # Add Ant 2
    simulation.run(max_steps=100000)  # Run the simulation

    turtle.mainloop()