
## Step: Install libraries

```python
pip3 install torch
python -m pip install mlagents
pip install six
pip install importlib-metadata==4.4
```

## Step: Download and install ml-agents examples
Download the source zip file from https://github.com/Unity-Technologies/ml-agents/releases/tag/latest_release . Open command prompt to that directory and run
```
mlagents-learn config/ppo/3DBall.yaml --run-id=first3DBallRun
```

![image](https://github.com/hughiephan/DPL/assets/16631121/de5919d4-0a4f-425e-ad3c-f5a9b6fb9afe)
