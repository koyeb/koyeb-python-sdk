# DeploymentStrategy


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | [**DeploymentStrategyType**](DeploymentStrategyType.md) |  | [optional] [default to DeploymentStrategyType.DEPLOYMENT_STRATEGY_TYPE_INVALID]

## Example

```python
from koyeb.api_async.models.deployment_strategy import DeploymentStrategy

# TODO update the JSON string below
json = "{}"
# create an instance of DeploymentStrategy from a JSON string
deployment_strategy_instance = DeploymentStrategy.from_json(json)
# print the JSON string representation of the object
print(DeploymentStrategy.to_json())

# convert the object into a dict
deployment_strategy_dict = deployment_strategy_instance.to_dict()
# create an instance of DeploymentStrategy from a dict
deployment_strategy_from_dict = DeploymentStrategy.from_dict(deployment_strategy_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


