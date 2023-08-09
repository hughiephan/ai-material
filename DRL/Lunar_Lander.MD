# Deep Reinforcement Learning with Lunar Lander

## Step:

```python
!apt install swig cmake
!pip install -r https://raw.githubusercontent.com/huggingface/deep-rl-class/main/notebooks/unit1/requirements-unit1.txt
!sudo apt-get update
!sudo apt-get install -y python3-opengl
!apt install ffmpeg
!apt install xvfb
!pip3 install pyvirtualdisplay

# !apt-get install python-opengl -y
# !apt install xvfb -y
# !pip install pyvirtualdisplay
!pip install piglet
# from pyvirtualdisplay import Display

import gym
from IPython import display
import matplotlib.pyplot as plt
%matplotlib inline

import os
import gymnasium
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
from pyvirtualdisplay import Display
import gymnasium as gym
# os.kill(os.getpid(), 9)
```

## Step:

```python
virtual_display = Display(visible=0, size=(1400, 900))
virtual_display.start()
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

## Step:
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
