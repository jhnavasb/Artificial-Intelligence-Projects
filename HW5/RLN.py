import gym
import gym_gridworlds
import numpy as np
import pygame
from collections import defaultdict
from matplotlib import pyplot as plt
import pandas as pd
import argparse


width = 10
height = 7
block_size = 80
border = 3

Color = [[255, 255, 255], [0, 0, 0], [224, 224, 224], [128, 128, 128], [64, 64, 64], [255, 0, 0], [255, 96, 208],
         [160, 32, 255], [80, 208, 255], [0, 32, 255], [96, 255, 128], [0, 192, 0], [255, 224, 32], [255, 160, 16]]


def windy(episodes, alpha, gamma, epsilon, auto):
    screen = pygame.display.set_mode((width * block_size + border, height * block_size + border))
    pygame.display.set_caption("Windy")
    grid_world((3, 0), (3, 7), screen)

    env = gym.make('WindyGridworld-v0')  # Example 6.5 Sutton’s book

    if auto:
        Q, stats, stats2, s = Q_learning_r(env, episodes, alpha, gamma, epsilon)
    else:
        Q, stats, stats2 = Q_learning(env, episodes, alpha, gamma, epsilon)

    pygame.display.set_caption("Policy")
    draw_policy(screen, Q)
    plot_episode_stats(stats, stats2, auto)

    input("\nPress Enter to continue and watch the final path.")
    pygame.display.set_caption("Solution")
    grid_world((3, 0), (3, 7), screen)
    obs = env.reset()  # Get initial state
    for a in range(20):
        steps(screen, obs)
        k = np.argmax(Q[obs])
        obs, _, done, _ = env.step(k)  # Get new state and reward after applying the action
        if done:
            break
    plt.show()


def steps(screen, step):
    b = border
    pygame.draw.rect(screen, Color[2], ((step[1] * block_size) + b, (step[0] * block_size) + b, block_size - b, block_size - b))
    pygame.display.flip()


def draw_policy(screen, Q):
    b = border
    block_sizes = block_size / 2
    kb = block_size / 3.5

    for w in range(width):
        for h in range(height):
            kw = 2 * w * block_sizes
            kh = 2 * h * block_sizes
            k = np.argmax(Q[(h, w)])

            if k == 0:
                pygame.draw.polygon(screen, Color[1], (
                (kw + kb - b, kh + kb + block_sizes - b), (kw + kb + block_sizes, kh + kb + block_sizes - b), (kw + kb + (block_sizes / 2) - b, kh + kb)))  #up
            if k == 1:
                pygame.draw.polygon(screen, Color[1], ((kw + kb + b, kh + kb + b), (kw + kb + b, kh + kb + block_sizes), (kw + kb + block_sizes, kh + kb + (block_sizes / 2))))   #right
            if k == 2:
                pygame.draw.polygon(screen, Color[1], ((kw + kb, kh + kb + b), (kw + kb + block_sizes, kh + kb + b), (kw + kb + (block_sizes / 2), kh + kb + block_sizes)))   #down
            if k == 3:
                pygame.draw.polygon(screen, Color[1], ((kw + kb + block_sizes - b, kh + kb + block_sizes + b), (kw + kb + block_sizes - b, kh + kb), (kw + kb + b, kh + kb + (block_sizes / 2))))   #left
            pygame.display.flip()


def grid_world(start, goal, screen):
    screen.fill(Color[8])
    b = border

    for w in range(width):
        for h in range(height):
            pygame.draw.rect(screen, Color[0], ((w * block_size) + b, (h * block_size) + b, block_size - b, block_size - b))

    pygame.draw.rect(screen, Color[5], ((start[1] * block_size) + b, (start[0] * block_size) + b, block_size - b, block_size - b))
    pygame.draw.rect(screen, Color[11], ((goal[1] * block_size) + b, (goal[0] * block_size) + b, block_size - b, block_size - b))
    pygame.display.flip()


def policy_e_greedy(Q, epsilon, n):

    def policy(obs):   #page 125 Sutton - Epsilon - Greedy
        A = np.ones(n, dtype=float) * epsilon / n   #epsilon / |A|
        best_action = np.argmax(Q[obs])   #s
        A[best_action] += (1.0 - epsilon)   #1 - epsilon + (epsilon / A(s))
        return A

    return policy


def S_learning(env, n_episodes, alpha, gamma, epsilon):
    Q = defaultdict(lambda: np.zeros(env.action_space.n))   #super list :D
    stats = np.zeros(n_episodes)   #array to store rewards over time for graph
    policy = policy_e_greedy(Q, epsilon, env.action_space.n)   #create a policy function with specific epsilon

    for episode in range(n_episodes):
        if (episode + 1) % 100 == 0:
            print("\rEpisode %d/%d" % (episode + 1, n_episodes), end='', flush=True)   #print episode each 100

        state = env.reset()   #first state
        action_probs = policy(state)   #get state's policy
        action = np.random.choice(np.arange(len(action_probs)), p=action_probs)   #choose an action "randomly" taking into account the actions probability from the policy

        while True:
            next_state, reward, done, info = env.step(action)   #take a step
            next_action_probs = policy(next_state)   #get next state's policy
            next_action = np.random.choice(np.arange(len(next_action_probs)), p=next_action_probs)   #choose the next action "randomly" taking into account the actions probability from the policy

            stats[episode] += reward   #sum reward for graph

            target = reward + (gamma * Q[next_state][next_action]) - Q[state][action]   #[R + gamma * Q(S',A') - Q(S,A)]
            Q[state][action] += alpha * target   # alpha * [R + gamma * Q(S',A') - Q(S,A)] --> update Q

            if done:
                break   #goal reached

            action = next_action   #update action
            state = next_state   #update state

    return Q, stats


def Q_learning(env, n_episodes, alpha, gamma, epsilon):
    Q = defaultdict(lambda: np.zeros(env.action_space.n))   #super list :D
    stats = np.zeros(n_episodes)   #array to store rewards over time for graph
    stats2 = defaultdict(lambda: np.zeros(env.action_space.n))
    policy = policy_e_greedy(Q, epsilon, env.action_space.n)   #create a policy function with specific epsilon

    for episode in range(n_episodes):
        if (episode + 1) % 100 == 0:
            print("\rEpisode %d/%d" % (episode + 1, n_episodes), end='', flush=True)   #print episode each 100

        state = env.reset()   #first state

        while True:
            action_probs = policy(state)  # get state's policy
            action = np.random.choice(np.arange(len(action_probs)), p=action_probs)   #choose an action "randomly" taking into account the actions probability from the policy
            next_state, reward, done, info = env.step(action)   #take a step

            stats[episode] += reward   #sum reward for graph
            stats2[state][action] += 1

            target = reward + (gamma * np.max(Q[next_state])) - Q[state][action]   #[R + gamma * maxQ(S',A') - Q(S,A)]
            Q[state][action] += alpha * target   # alpha * [R + gamma * maxQ(S',A') - Q(S,A)] --> update Q

            if done:
                break   #goal reached

            state = next_state   #update state

    return Q, stats, stats2


def Q_learning_r(env, n_episodes, alpha, gamma, epsilon):
    Q = defaultdict(lambda: np.zeros(env.action_space.n))   #super list :D
    stats = defaultdict(lambda: 0)   #array to store rewards over time for graph
    stats2 = defaultdict(lambda: np.zeros(env.action_space.n))
    policy = policy_e_greedy(Q, epsilon, env.action_space.n)   #create a policy function with specific epsilon
    ok = False
    episode = 0

    while not ok:
        #if (episode + 1) % 100 == 0:
        print("\rEpisode %d" % (episode + 1), end='', flush=True)   #print episode each 100

        state = env.reset()   #first state

        while True:
            action_probs = policy(state)  # get state's policy
            action = np.random.choice(np.arange(len(action_probs)), p=action_probs)   #choose an action "randomly" taking into account the actions probability from the policy
            next_state, reward, done, info = env.step(action)   #take a step

            stats[episode] += reward   #sum reward for graph
            stats2[state][action] += 1

            target = reward + (gamma * np.max(Q[next_state])) - Q[state][action]   #[R + gamma * maxQ(S',A') - Q(S,A)]
            Q[state][action] += alpha * target   # alpha * [R + gamma * maxQ(S',A') - Q(S,A)] --> update Q

            if done:
                break   #goal reached

            state = next_state   #update state
        episode += 1

        if episode < n_episodes:
            ok = False
        else:
            ok = validate(Q, env)

    return Q, stats, stats2, episode


def validate(Q, env):
    t = 0
    done = False
    obs = env.reset()  # Get initial state
    while not done and t < 30:
        k = np.argmax(Q[obs])
        obs, _, done, _ = env.step(k)  # Get new state and reward after applying the action
        t += 1

    return done

def plot_episode_stats(stats, stats2, auto):

    if auto:
        plt.plot(list(stats.keys()), list(stats.values()))
    else:
        plt.plot(np.asarray(stats))

    plt.xlabel("Episode")
    plt.ylabel("Episode Reward")
    plt.title("Episode Reward over Time")

    df = pd.DataFrame(stats2).T
    ax = df.plot(kind="bar", title="Histogram visited pair (s,a)", stacked=True)
    ax.legend(["Up", "Right", "Down", "Left"])
    ax.set_xlabel("States")
    ax.set_ylabel("Times")

    #plt.show()
    plt.draw()
    plt.pause(0.001)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--episodes", type=int, required=True,
                    help="number of episodes, or standard episodes for auto")
    ap.add_argument("-a", "--alpha", type=float, required=True,
                    help="learning rate")
    ap.add_argument("-g", "--gamma", type=float, required=True,
                    help="discounting rate")
    ap.add_argument("-e", "--epsilon", type=float, required=True,
                    help="exploration rate")
    ap.add_argument("-t", "--auto", type=int, required=True,
                    help="to get the first path at the minimun episodes, 0 = no, 1 = yes")

    arg = ap.parse_args()
    args = vars(arg)

    pygame.init()
    windy(args["episodes"], args["alpha"], args["gamma"], args["epsilon"], args["auto"])

    end = False
    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True


if __name__ == "__main__":
    main()