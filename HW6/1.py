import numpy as np
import gym
from gym import wrappers
import matplotlib.pyplot as plt
import logging
import math
from collections import defaultdict
import pandas as pd

def maxAction(Q, state):
    values = np.array([Q[state, a] for a in range(2)])
    action = np.argmax(values)
    return action

# discretize the spaces
poleThetaSpace = np.linspace(-0.24, 0.24, 10)
poleThetaVelSpace = np.linspace(-math.radians(50), math.radians(50), 10)
cartPosSpace = np.linspace(-4.8, 4.8, 10)
cartVelSpace = np.linspace(-.5, .5, 10)

def plot_running_avg(totalrewards, stats2):
    N = len(totalrewards)
    running_avg = np.empty(N)
    for t in range(N):
        running_avg[t] = np.mean(totalrewards[max(0, t - 100):(t + 1)])
    plt.plot(running_avg)
    plt.title("Running Average")

    df = pd.DataFrame(stats2).T
    ax = df.plot(kind="bar", title="Histogram visited pair (s,a)", stacked=True)
    ax.legend(["Right", "Left"])
    ax.set_xlabel("States")
    ax.set_ylabel("Times")

    plt.show()

def getState(observation):
    cartX, cartXdot, cartTheta, cartThetadot = observation
    cartX = int(np.digitize(cartX, cartPosSpace))
    cartXdot = int(np.digitize(cartXdot, cartVelSpace))
    cartTheta = int(np.digitize(cartTheta, poleThetaSpace))
    cartThetadot = int(np.digitize(cartThetadot, poleThetaVelSpace))

    return (cartX, cartXdot, cartTheta, cartThetadot)

if __name__ == '__main__':
    env = gym.make('CartPole-v0')
    # model hyperparameters
    GAMMA = 1
    ALPHA = 0.01
    EPS = 0.8

    # construct state space
    states = []
    for i in range(len(cartPosSpace) + 1):
        for j in range(len(cartVelSpace) + 1):
            for k in range(len(poleThetaSpace) + 1):
                for l in range(len(poleThetaVelSpace) + 1):
                    states.append((i, j, k, l))

    Q = {}
    for state in states:
        for action in range(2):
            Q[state, action] = 0

    numGames = 110000
    totalRewards = np.zeros(numGames)
    stats2 = defaultdict(lambda: np.zeros(env.action_space.n))
    for i in range(numGames):
        if (i + 1) % 5000 == 0:
            print("\rEpisode %d/%d, Reward %d, Size %d, States %d" % (i + 1, numGames, totalRewards[i-1], len(state), len(states)), end='', flush=True)
        #if i % 5000 == 0:
        #    print('starting game ', i, "reward",totalRewards[i-1], "state size", len(state), "states", len(states))

        done = False
        epRewards = 0
        observation = env.reset()
        while not done:
            state = getState(observation)
            rand = np.random.random()
            #if np.random.uniform() < EPS:
             #   action = env.action_space.sample()  # epsilon greedy
            #else:
              #  action = maxAction(Q, state)

            action = maxAction(Q, state) if rand < (1 - EPS) else env.action_space.sample()
            observation_, reward, done, info = env.step(action)
            epRewards += reward
            state_ = getState(observation_)
            action_ = maxAction(Q, state_)
            stats2[state][action] += 1
            Q[state, action] = Q[state, action] + ALPHA * (reward + GAMMA * Q[state_, action_] - Q[state, action])
            observation = observation_
        if EPS - 2 / numGames > 0:
            EPS -= 2 / numGames
            #EPS = 1.0 / np.sqrt(i + 1)
        else:
            EPS = 0
        totalRewards[i] = epRewards
        #print(epRewards)
    plot_running_avg(totalRewards, stats2)

    logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                        format="%(message)s")

    logging.info(Q)






