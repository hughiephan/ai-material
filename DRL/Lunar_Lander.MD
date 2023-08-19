# Deep Reinforcement Learning with Lunar Lander

Deep Reinforcement Learning with Gym's Lunar Lander involves training a neural network to navigate a lunar lander environment through trial and error. By using a combination of reward-based learning and deep neural networks, the agent learns optimal strategies for landing the lunar module on a designated landing pad while managing fuel consumption and avoiding crashes.

## Prerequisites

You should run this on Google Colab Notebook or Local Jupyter

![image](https://github.com/hughiephan/DPL/assets/16631121/012cf7da-9497-43f0-a01a-3ba550d61e19)

## What is Lunar Lander v2

Lunar Lander v2 is a toy game based around physics control from gymnasium library

![image](https://github.com/hughiephan/DPL/assets/16631121/3e0fefce-385a-4490-8bac-ee36f7712cd4)

There are four discrete `Actions` available: do nothing, fire left orientation engine, fire main engine, fire right orientation engine.

The `Observation` is an 8-dimensional vector: the coordinates of the lander in x & y, its linear velocities in x & y, its angle, its angular velocity, and two booleans that represent whether each leg is in contact with the ground or not.

The `Reward` for moving from the top of the screen to the landing pad and coming to rest is about 100-140 points. If the lander moves away from the landing pad, it loses reward. If the lander crashes, it receives an additional -100 points. If it comes to rest, it receives an additional +100 points. Each leg with ground contact is +10 points. Firing the main engine is -0.3 points each frame. Firing the side engine is -0.03 points each frame. Solved is 200 points.

![image](https://github.com/hughiephan/DPL/assets/16631121/e82a7e5e-7a25-4421-90f5-06ce57ee22db)

## Step 1: Install Libraries

`Gymnasium` is a toolkit for training RL agents and `stable-baselines3` is a set of reinforcement learning algorithms

```shell
!apt install swig cmake xvfb
!sudo apt-get update && apt-get install -y python3-opengl
!pip3 install stable-baselines3==2.0.0a5 gymnasium[box2d]==0.28.1
```

## Step 2: Import Libraries

Proximal Policy Optimization (PPO) is a reinforcement learning algorithm that iteratively updates an agent's policy by optimizing a surrogate objective function while enforcing a constraint to ensure the policy updates are not too drastic. This is achieved by enforcing a "proximal" constraint on policy updates, ensuring that the new policy doesn't deviate too far from the old policy. 

PPO is a type of actor-critic algorithm, which means that it has two components: an actor and a critic. The actor is responsible for deciding which actions to take, while the critic is responsible for evaluating the actions taken by the actor.

```python
import os
import gymnasium as gym
import matplotlib.pyplot as plt
from IPython import display
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
%matplotlib inline
```

## Step 3: Training

MlpPolicy implements actor critic with a MLP

![image](https://github.com/hughiephan/DPL/assets/16631121/ddce1891-347c-4f87-8ace-13dd91f8259d)

```python
env = make_vec_env('LunarLander-v2', n_envs=1)

model = PPO(
    policy = 'MlpPolicy',
    env = env,
    n_steps = 1024,
    batch_size = 64,
    n_epochs = 4,
    verbose=1)

model.learn(total_timesteps=100)
```

If you want to train more agents, you can change the number of `n_envs`

![image](https://github.com/hughiephan/DPL/assets/16631121/4323b4c1-6967-4577-b743-8d032fea4831)


## Step 4: Render agent actions

Render a video

```python
obs = env.reset()
for _ in range(100):
    img = plt.imshow(env.render('rgb_array'))
    plt.show()
    img.set_data(env.render('rgb_array'))
    display.display(plt.gcf())
    display.clear_output(wait=True)
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()
```

or render by timesteps

```python
obs = env.reset()
for i in range(100):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()
    if (i % 20 == 0): 
      print("At timestep ", i)
      img = plt.imshow(env.render('rgb_array'))
      plt.show()
      img.set_data(env.render('rgb_array'))
```


# References
- Deep RL Course from Hugging Face (Unit 1)
- Gymnasium Documentation
