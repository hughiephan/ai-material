
## Step: Install Python
Install Python 3.7.x (it won't work with 3.8, 3.9 and 3.10)

```python
pip3 install torch
python -m pip install mlagents
pip install six
pip install importlib-metadata==4.4
```

## Step: Install Unity
Install Unity 2021 and download the source zip file from https://github.com/Unity-Technologies/ml-agents/releases/tag/latest_release . 

## Step: Training
```
mlagents-learn config/ppo/3DBall.yaml --run-id=first3DBallRun
```

![image](https://github.com/hughiephan/DPL/assets/16631121/de5919d4-0a4f-425e-ad3c-f5a9b6fb9afe)


## References
- https://unity-technologies.github.io/ml-agents/Installation/
