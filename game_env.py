from game import Game
import numpy as np

class GameEnv(Game):
    def __init__(self, size):
        super().__init__(size)
        self.MOVE_PENALTY = 1
        self.ENEMY_PENALTY = 100 
        self.OBSERVATION_SPACE_VALUES = 6 # player x, player y, distance to enemy
        self.ACTION_SPACE_SIZE = 4#2 #4
        self.done = False

    def _get_distance(self):
        return (abs(self.player["pos"][0] - self.enemy["pos"][0]) + 
                abs(self.player["pos"][1] - self.enemy["pos"][1]), 
                abs(self.player["pos"][0] - self.goal["pos"][0]) +
                abs(self.player["pos"][1] - self.goal["pos"][1]))

    def is_done(self):
        if self.done:
            return True
        self.done = self.player["pos"] == self.enemy["pos"] or self.player["pos"] == self.goal["pos"]
        return self.done

    def get_current_state(self):
        distance, distance2 = self._get_distance()

        # return (*self.player["pos"], distance)
        return (distance, distance2, *self.goal["pos"], *self.player["pos"])

    def get_reward(self):
        if self.is_done():
            if self.player["pos"] == self.enemy["pos"]:
                return -1*300
            else:
                return 500
        else:
            # return int((1 / (self._get_distance()[0] * 10)) + (-1*self._get_distance()[1]))
            # return -100 + int(((1 / self._get_distance()[1]) * 10))
            return -1

    def reset(self):
        super().reset()
        self.done = False
        return self.get_current_state()

    # @return  new_state, reward, done, _
    def step(self, action):
        self.take_action(action, self.player)

        # smallest_distance = 99999999
        # action = None
        # for i in range(self.ACTION_SPACE_SIZE):
        #     pos = self.simulate_action(i, self.enemy)
        #     if not pos:
        #         continue
        #     distance = abs(self.player["pos"][0] - pos[0]) + \
        #         abs(self.player["pos"][1] - pos[1])
        #     if distance < smallest_distance:
        #         smallest_distance = distance
        #         action = i

        # self.take_action(action, self.enemy)

        # action = np.random.choice(self.get_possible_actions(self.goal))
        # self.take_action(action, self.goal)

        new_state = self.get_current_state()
        reward = self.get_reward()
        done = self.is_done()

        return new_state, reward, done, None
