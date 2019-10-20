import pygame as pg
import numpy as np
import time


class Game:
    def __init__(self, size):
        pg.init()
        self.size = (size, size)
        # self.screen = pg.display.set_mode(self.size)
        self.number_of_grids = 3
        self.grid_size = size//self.number_of_grids
        self.grid_size_y = 10
        self.reset()

    def reset(self):
        self.grid_size = self.size[0]//self.number_of_grids
        self.grid = [[0 for x in range(self.grid_size)]
                    for y in range(self.grid_size)]
                    #  for y in range(self.grid_size_y)]

        enemy_x = np.random.choice([0, self.number_of_grids-1])
        goal_x = 0
        enemy_y = np.random.randint(self.grid_size_y)
        goal_y = np.random.randint(self.grid_size_y)
        if enemy_x == 0:
            goal_x = self.number_of_grids-1

        self.player = {
            "pos": tuple(np.random.randint(self.number_of_grids, size=2))
            # "pos": (self.number_of_grids//2, 0)
        }

        self.enemy = {
            "pos": tuple(np.random.randint(self.number_of_grids, size=2))
            # "pos": (np.random.randint(self.number_of_grids), 0)
            # "pos": (enemy_x, enemy_y)
        }

        self.goal = {
            "pos": tuple(np.random.randint(self.number_of_grids, size=2))
            # "pos": (np.random.randint(self.number_of_grids), 0)
            # "pos": (goal_x, goal_y)
        }

        while self.goal["pos"] == self.enemy["pos"] or self.goal["pos"] == self.player["pos"]:
            self.goal = {
                "pos": tuple(np.random.randint(self.number_of_grids, size=2))
            }
        
    def render(self):
        self.screen.fill((0, 0, 0))

        # render grid
        for y, row in enumerate(self.grid):
            for x, val in enumerate(row):
                color = (255, 255, 255)

                if x == self.player["pos"][0] and y == self.player["pos"][1]:
                    color = (0, 0, 255)
                elif x == self.enemy["pos"][0] and y == self.enemy["pos"][1]:
                    color = (255, 0, 0)
                elif x == self.goal["pos"][0] and y == self.goal["pos"][1]:
                    color = (0, 255, 0)

                pg.draw.rect(self.screen, color, (x*self.grid_size, y *
                                                  self.grid_size, self.grid_size - 1, self.grid_size - 1))

        pg.display.update()

    def get_possible_actions(self, agent=None):
        if not agent:
            agent = self.player

        position = agent["pos"]

        possible_actions = []
        x, y = position
        max_x, max_y = self.number_of_grids,  self.number_of_grids

        if y - 1 >= 0:
            possible_actions.append(0)  # up = 0
        if x + 1 < max_x:
            possible_actions.append(1)  # right = 1
        if y + 1 < max_y:
            possible_actions.append(2)  # down = 2
        if x - 1 >= 0:
            possible_actions.append(3)  # left = 3

        return possible_actions

        # if x + 1 < max_x:
        #     possible_actions.append(0)  # right = 0
        # if x - 1 >= 0:
        #     possible_actions.append(1)  # left = 1
        # return possible_actions

    def take_action(self, action, agent):
        if action not in self.get_possible_actions(agent):
            return

        if action == 0:  # up
            agent["pos"] = tuple(
                np.array(agent["pos"]) + np.array((0, -1)))
        if action == 1:  # right
            agent["pos"] = tuple(
                np.array(agent["pos"]) + np.array((1, 0)))
        if action == 2:  # down
            agent["pos"] = tuple(
                np.array(agent["pos"]) + np.array((0, 1)))
        if action == 3:  # left
            agent["pos"] = tuple(
                np.array(agent["pos"]) + np.array((-1, 0)))


        # if action == 0:  # right
        #     agent["pos"] = tuple(
        #         np.array(agent["pos"]) + np.array((1, 0)))
        # if action == 1:  # left
        #     agent["pos"] = tuple(
        #         np.array(agent["pos"]) + np.array((-1, 0)))

    def simulate_action(self, action, agent):
        if action not in self.get_possible_actions(agent):
            return

        if action == 0:  # up
            return tuple(
                np.array(agent["pos"]) + np.array((0, -1)))
        if action == 1:  # right
            return tuple(
                np.array(agent["pos"]) + np.array((1, 0)))
        if action == 2:  # down
            return tuple(
                np.array(agent["pos"]) + np.array((0, 1)))
        if action == 3:  # left
            return tuple(
                np.array(agent["pos"]) + np.array((-1, 0)))
