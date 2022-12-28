# This file contains the options that you should modify to solve Question 2

def question2_1():
    #TODO: Choose options that would lead to the desired results 
    return {
        # seek the near terminal state (reward = +1.0) via the shortest dangerous path
        # moving besides the row of -10 state 
        # (i.e. the path that has the highest probability of reaching the near terminal state)
        
        "noise": 0.0,
        "discount_factor": 1.0, #discount factor is the weight of future rewards 
        "living_reward": -5.0 #give a negative reward to encourage the agent to reach the terminal state as soon as possible
    }

def question2_2():
    #TODO: Choose options that would lead to the desired results
    return {
        # seek the near terminal state (reward = +1.0) via the longest safe path
        # moving away from the row of -10 state
        # wants to make also go away the reward +1
        "noise": 0.2,
        "discount_factor": 0.2, #decrease the discount factor to make the factor decrease as we go furthur (gamma^2, gamma^3 ..etc) and instead of going to +10, go to +1
        "living_reward": -1.0 #give it normal reward to encourage the agent to reach the terminal state in the long safe path, but not the longest(not to +10)
    }

def question2_3():
    #TODO: Choose options that would lead to the desired results
    # seek the near terminal state (reward = +10.0) via the shortest dangerous path
        # moving besides the row of -10 state 
    return {
        "noise": 0.0,
        "discount_factor": 1.2, #increase the discount factor more than one, to make the factor increase as we go furthur (gamma^2, gamma^3 ..etc) 
        # to don't make the agent more greedy and instead of going to the near terminal state it will go to the furthur one terminal state
        "living_reward": -5.0 #give a negative reward to encourage the agent to reach the terminal state as soon as possible
    }

def question2_4():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.2,
        "discount_factor": 1.19, #difference between question2_2(to reach +1) and question2_4(to reach +10) is the discount factor, should be bigger to go furthur
        "living_reward": -2.0  #give a negative reward smaller than question2_2(to reach +1) to encourage the agent to reach the furthur terminal state
        }

def question2_5():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.0,
        "discount_factor": 1.0,
        "living_reward": 20.0 #why go to terminal while you can get a high reward as we go forever in the grid
        # so i give a very high positive reward to encourage the agent to not go to the terminal state
    }

def question2_6():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.0,
        "discount_factor": 1.0,
        "living_reward": -20.0 #to reach the terminal state as soon as possible so i give a very high negative reward 
    }