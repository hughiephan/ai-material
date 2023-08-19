# Deep Reinforcement Learning with Lunar Lander

Deep Reinforcement Learning with Gym's Lunar Lander involves training a neural network to navigate a lunar lander environment through trial and error. By using a combination of reward-based learning and deep neural networks, the agent learns optimal strategies for landing the lunar module on a designated landing pad while managing fuel consumption and avoiding crashes.

## Prerequisites

You should run this on Google Colab Notebook or Local Jupyter

![image](https://github.com/hughiephan/DPL/assets/16631121/012cf7da-9497-43f0-a01a-3ba550d61e19)

## Reinforcement Learning
![image](https://github.com/hughiephan/DPL/assets/16631121/3d929e8a-5baa-4a24-9faf-296fa45db9b5)

There are 5 elements – Agent, Environment, Action, Observation, Reward. The idea behind Reinforcement Learning is that an agent (an AI) will learn from the environment by interacting with it (through trial and error) and receiving rewards (negative or positive) as feedback for performing actions.

## Step 1: Install Libraries

`Gymnasium` is a toolkit for training RL agents and `stable-baselines3` is a set of reinforcement learning algorithms

```shell
!apt install swig cmake xvfb
!sudo apt-get update && apt-get install -y python3-opengl
!pip3 install stable-baselines3==2.0.0a5 gymnasium[box2d]==0.28.1
```

## Step 2: Import Libraries

Proximal Policy Optimization (PPO) is a reinforcement learning algorithm that iteratively updates an agent's policy by optimizing a surrogate objective function while enforcing a constraint to ensure the policy updates are not too drastic. This is achieved by enforcing a "proximal" constraint on policy updates, ensuring that the new policy doesn't deviate too far from the old policy.

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

MlpPolicy implements actor critic, using a MLP

![image](https://github.com/hughiephan/DPL/assets/16631121/cf664a4e-5d7f-4af7-9968-db25fa282ae4)

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
