
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

## Step: RollerAgent

- Select the RollerAgent GameObject to show its properties in the Inspector window.
- Drag the Target GameObject in the Hierarchy into the Target field in RollerAgent Script.
- Add a Decision Requester script with the Add Component button. Set the Decision Period to 10. For more information on decisions, see the Agent documentation
- Add a Behavior Parameters script with the Add Component button. Set the Behavior Parameters of the Agent to the following:
- Behavior Name: RollerBall
- Vector Observation > Space Size = 8
- Actions > Continuous Actions = 2

```C
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;
using Unity.MLAgents.Actuators;

public class RollerAgent : Agent
{
    Rigidbody rBody;
    void Start () {
        rBody = GetComponent<Rigidbody>();
    }

    public Transform Target;
    public override void OnEpisodeBegin()
    {
       // If the Agent fell, zero its momentum
        if (this.transform.localPosition.y < 0)
        {
            this.rBody.angularVelocity = Vector3.zero;
            this.rBody.velocity = Vector3.zero;
            this.transform.localPosition = new Vector3( 0, 0.5f, 0);
        }

        // Move the target to a new spot
        Target.localPosition = new Vector3(Random.value * 8 - 4,
                                           0.5f,
                                           Random.value * 8 - 4);
    }

    public override void CollectObservations(VectorSensor sensor)
    {
        // Target and Agent positions
        sensor.AddObservation(Target.localPosition);
        sensor.AddObservation(this.transform.localPosition);

        // Agent velocity
        sensor.AddObservation(rBody.velocity.x);
        sensor.AddObservation(rBody.velocity.z);
    }

    public float forceMultiplier = 10;
    public override void OnActionReceived(ActionBuffers actionBuffers)
    {
        // Actions, size = 2
        Vector3 controlSignal = Vector3.zero;
        controlSignal.x = actionBuffers.ContinuousActions[0];
        controlSignal.z = actionBuffers.ContinuousActions[1];
        rBody.AddForce(controlSignal * forceMultiplier);

        // Rewards
        float distanceToTarget = Vector3.Distance(this.transform.localPosition, Target.localPosition);

        // Reached target
        if (distanceToTarget < 1.42f)
        {
            SetReward(1.0f);
            EndEpisode();
        }

        // Fell off platform
        else if (this.transform.localPosition.y < 0)
        {
            EndEpisode();
        }
    }

    public override void Heuristic(in ActionBuffers actionsOut)
    {
        var continuousActionsOut = actionsOut.ContinuousActions;
        continuousActionsOut[0] = Input.GetAxis("Horizontal");
        continuousActionsOut[1] = Input.GetAxis("Vertical");
    }
}
```

## Step: Target   
```C
using System.Collections;  
using System.Collections.Generic;  
using UnityEngine;  
  
public class Movement : MonoBehaviour  
{  
    Vector3 Vec;  
    // Start is called before the first frame update  
    void Start()  
    {  
          
    }  
  
    public float forceMultiplier = 10;
    void Update()  // Update is called once per frame  
    {  
        Vec = transform.localPosition;  
        Vec.x += Input.GetAxis("Horizontal") * Time.deltaTime * forceMultiplier;  
        Vec.z += Input.GetAxis("Vertical") * Time.deltaTime * forceMultiplier;  
        transform.localPosition = Vec;  
    }  
}  
```

## Step: Rollerball Config

Rollerball_config.yaml

```
behaviors:
  RollerBall:
    trainer_type: ppo
    hyperparameters:
      batch_size: 10
      buffer_size: 100
      learning_rate: 3.0e-4
      beta: 5.0e-4
      epsilon: 0.2
      lambd: 0.99
      num_epoch: 3
      learning_rate_schedule: linear
      beta_schedule: constant
      epsilon_schedule: linear
    network_settings:
      normalize: false
      hidden_units: 128
      num_layers: 2
    reward_signals:
      extrinsic:
        gamma: 0.99
        strength: 1.0
    max_steps: 500000
    time_horizon: 64
    summary_freq: 10000
```

## Step: Training

![image](https://github.com/hughiephan/DPL/assets/16631121/de5919d4-0a4f-425e-ad3c-f5a9b6fb9afe)

```C
mlagents-learn config/rollerball_config.yaml --run-id=RollerBall --resume
```

## References
- https://unity-technologies.github.io/ml-agents/Installation/
- https://unity-technologies.github.io/ml-agents/Getting-Started/
- https://unity-technologies.github.io/ml-agents/Learning-Environment-Create-New/
