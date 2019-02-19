import numpy as np
#from util import plotRunningAverage
import gym
from gym import wrappers
import math

env = gym.make('CartPole-v0')
Q = np.loadtxt("logfile", dtype='f', delimiter=',')


poleThetaSpace = np.linspace(-0.24, 0.24, 10)
poleThetaVelSpace = np.linspace(-math.radians(50), math.radians(50), 10)
cartPosSpace = np.linspace(-4.8, 4.8, 10)
cartVelSpace = np.linspace(-.5, .5, 10)
GAMMA = 1
ALPHA = 0.01
EPS = 0.8

def maxAction(Q, state):
    values = np.array([Q[state, a] for a in range(2)])
    action = np.argmax(values)
    return action

def getState(observation):
    cartX, cartXdot, cartTheta, cartThetadot = observation
    cartX = int(np.digitize(cartX, cartPosSpace))
    cartXdot = int(np.digitize(cartXdot, cartVelSpace))
    cartTheta = int(np.digitize(cartTheta, poleThetaSpace))
    cartThetadot = int(np.digitize(cartThetadot, poleThetaVelSpace))

    return (cartX, cartXdot, cartTheta, cartThetadot)

done = False
cnt = 0
#env = wrappers.Monitor(env, 'Movie', force=True)
observation = env.reset()
while not done:
   env.render()
   state = getState(observation)
   rand = np.random.random()
   action = maxAction(Q, state) 
   observation, reward, done, info = env.step(action)
   if done:
       break
env.close()
