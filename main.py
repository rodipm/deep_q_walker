import sys
import signal
import random
import gym
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import matplotlib.pyplot as plt
from collections import deque
from copy import deepcopy

from dqn_agent import DQNAgent
from game_env import GameEnv

EPISODES = 500_000

###################################
PLAY = False
LOAD_MODEL = True
###################################

load_file_name = "./save/walker_small_10.h5"
save_file_name = "./save/walker_small_10.h5"
play_file_name = "./save/walker_small_10.h5"

scores = []

plt.ion()


def display_graphics():
    plt.plot(scores)
    plt.show()
    plt.pause(0.05)


def play_game(_agent, preview=True):
    print("Play game")
    agent = deepcopy(_agent)

    agent.load(play_file_name)
    for _ in range(20 if not preview else 1):
        state = env.reset()
        # env.seed(0)
        state = np.reshape(state, [1, state_size])
        score = 0
        for e in range(400):
            env.render()
            action = agent.play(state)
            next_state, reward, done, _ = env.step(action)
            score += reward
            state = np.reshape(next_state, [1, state_size])
            if done:
                print(score)
                break


if __name__ == "__main__":
    env = GameEnv(400)
    state_size = env.OBSERVATION_SPACE_VALUES
    action_size = env.ACTION_SPACE_SIZE
    agent = DQNAgent(state_size, action_size)
    done = False
    batch_size = 64

    best_score = -1
    render = False

    if PLAY:
        play_game(agent, False)
    else:
        if LOAD_MODEL:
            print("Loading Model...")
            agent.load(load_file_name)
            agent.epsilon = 1.0
            agent.learning_rate = 0.001
            agent.epsilon_decay = 0.990
            agent.gamma = 0.95

        for phase in range(7, 8):
            env.number_of_grids = phase + 3
            agent.epsilon = 1.0
            agent.memory = deque(maxlen=2000)
            phase_scores = deque(maxlen=5)
            for e in range(EPISODES):
                done = False
                state = env.reset()
                # env.seed(0)
                state = np.reshape(state, [1, state_size])
                score = 0
                while not done:
                    # env.render()
                    possible_actions = env.get_possible_actions()
                    action = agent.act(state, possible_actions)
                    # if action not in possible_actions:
                    #     reward = -1*99999
                    #     env.done = True
                    #     done = True
                    # else: 
                    next_state, reward, done, _ = env.step(action)

                    score += reward

                    next_state = np.reshape(next_state, [1, state_size])
                    agent.remember(state, action, reward, next_state, done)
                    state = next_state

                    if done:
                        print("episode: {}/{}, score: {}, e: {:.2}"
                            .format(e, EPISODES, score, agent.epsilon))

                        if score >= best_score:
                            print("Saving Model...")
                            best_score = score
                            agent.save(save_file_name)
                            if e > -1:
                                pass
                                # play_game(agent)

                        scores.append(score)
                        phase_scores.append(score)
                        break

                    if len(agent.memory) > batch_size:
                        agent.replay(batch_size)

                if len(phase_scores) == 5 and np.mean(phase_scores) > 480.0:
                    agent.save("./save/walker_small_10_final.h5")
                    break

                if e % 10 == 0:
                    display_graphics()
                    # pass
