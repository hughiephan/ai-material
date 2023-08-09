# Deep Reinforcement Learning with Lunar Lander

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
```python
obs = env.reset()
img = plt.imshow(env.render('rgb_array'))
for _ in range(100):
    img.set_data(env.render('rgb_array')) # just update the data
    display.display(plt.gcf())
    display.clear_output(wait=True)
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()
```
