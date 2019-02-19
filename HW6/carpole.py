import gym
import numpy as np
import math
from collections import deque
from gym import wrappers
env = gym.make('CartPole-v0')
bestLength = 0
episode_lengths =[]
best_weights = np.zeros(4)
for i in range(100):
    new_weights = np.random.uniform(-1,1,4) #observation = env.reset() #vector with the position the velocity angle of the pole and velocity on the pole
    length=[]
    for j in range(100):
        observation = env.reset()
        done=False
        cnt=0
        while not done:
            # env.render()
            cnt += 1
            action = 1 if np.dot(observation,new_weights)> 0 else 0 # if it positive we're gonna moving to the right, if it's negative left instead


            observation, reward, done, _ = env.step(action)

            if done:
                break
        length.append(cnt)
    average = float(sum(length)/len(length))
    if average > bestLength:
        bestLength =average
        best_weights=new_weights
    episode_lengths.append(average)
    if i % 10 ==0:
        print("best length is ", bestLength)
done=False
cnt=0
#env = wrappers.Monitor(env,'Movie',force=True)
observation = env.reset()

while 1:
    env.render()
    cnt+=1
    action = 1 if np.dot(observation, best_weights) > 0 else 0
    observation, reward, done, _ = env.step(action)
    
print("game lasted: ", cnt," moves")












