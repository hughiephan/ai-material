# Deep Reinforcement Learning with Lunar Lander

![image](https://github.com/hughiephan/DPL/assets/16631121/012cf7da-9497-43f0-a01a-3ba550d61e19)

# Prerequisites

You should run this on Google Colab Notebook or Local Jupyter

## Step: Install Libraries

```python
!apt install swig cmake xvfb
!sudo apt-get update && apt-get install -y python3-opengl
!pip3 install pyvirtualdisplay stable-baselines3==2.0.0a5 gymnasium[box2d]==0.28.1
```

## Step: Import Libraries

```python
import os
import gymnasium as gym
import matplotlib.pyplot as plt
from IPython import display
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
from pyvirtualdisplay import Display
%matplotlib inline
```

## Step: Training

```python
env = gym.make("LunarLander-v2")
observation, info = env.reset()
for _ in range(20):
  action = env.action_space.sample()
  observation, reward, terminated, truncated, info = env.step(action)
  if terminated or truncated:
      observation, info = env.reset()

env.close()
env = gym.make("LunarLander-v2")
env.reset()
env = make_vec_env('LunarLander-v2', n_envs=1)

model = PPO(
    policy = 'MlpPolicy',
    env = env,
    n_steps = 1024,
    batch_size = 64,
    n_epochs = 4,
    gamma = 0.999,
    gae_lambda = 0.98,
    ent_coef = 0.01,
    verbose=1)

model.learn(total_timesteps=100)
```

## Step: Render

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

or Render at timesteps:
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