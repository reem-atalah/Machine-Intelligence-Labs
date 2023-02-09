# Machine-Intelligence-Labs
For many techniques in Machine Intelligence, I have implemented some algorithms in topics:
1. [Search](#search-algorithms)
2. [Constraint Satisfaction Problem](#Constraint-Satisfaction-Problem-CSP)
3. [Games](#Games)
4. [Markov Decision Process](#Markov-Decision-Process-MDP)
5. [Reinforcement Learning](#Reinforcement-Learning-RL)

To understand each problem set, you need to read the 'instructions.pdf' file in each folder

## Search Algorithms 
[`Problem Set - 1`](https://github.com/reem-atalah/Machine-Intelligence-Labs/tree/master/Problem%20Set%201%20-%20Student%20Version)

Search algorithms implemented are:
* Breadth First Search
* Depth First Search
* Uniform Cost Search
* A* Search
* Greedy Best First Search

Those algorithms were used to solve a parking game-implemented within the code-, where each car should move to reach its correct car slot.


## Constraint Satisfaction Problem CSP
[`Problem Set - 2`](https://github.com/reem-atalah/Machine-Intelligence-Labs/tree/master/Problem%20Set%202%20-%20Student%20Version/Problem%20Set%202%20-%20Student%20Version)

To solve CSP, it needs to path through certain steps to ensure that we have reached all the valid values for all variables:
1. 1-Consistency
2. Forward Checking
3. Least Restraining Value
4. Minimum Remaining Values
5. Backtracking Search

## Games 
[`Problem Set - 2`](https://github.com/reem-atalah/Machine-Intelligence-Labs/tree/master/Problem%20Set%202%20-%20Student%20Version/Problem%20Set%202%20-%20Student%20Version)

For adversarial games, where we have two opponents, each player wants to win, so player uses gaming algorithms to maximize its rewards to win .

For all coming algorithms, both players must play optimally 

Some algorithms implemented to solve games problem are:
* Minimax Search
* Alpha Beta Pruning
* Alpha Beta Pruning with Move Ordering
* Expectimax Search

## Markov Decision Process MDP
[`Problem Set - 3`](https://github.com/reem-atalah/Machine-Intelligence-Labs/tree/master/Problem%20Set%203%20-%20Student%20Version/Problem%20Set%203%20-%20Student%20Version)

For a sequential, stochastic, offline game with fully observable environment, we use MDP algorithms. 

MDP algorithms find the best policy -instead of plan, due to noise- to take the maximum rewards.

First initialize some options with some noise of movement and different rewards to reach different ends

Then use **Value Iteration** and **Policy Iteration**

## Reinforcement Learning RL
[`Problem Set - 3`](https://github.com/reem-atalah/Machine-Intelligence-Labs/tree/master/Problem%20Set%203%20-%20Student%20Version/Problem%20Set%203%20-%20Student%20Version)

Similar to MDP but used to solve online game using one of the 3 different approaches:
1. SARSA
2. Q-Learning
3. Approximate Q-Learning





