# DeclareStepProgressRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**secret** | **str** |  | [optional] 
**status** | [**DeploymentProvisioningInfoStageStatus**](DeploymentProvisioningInfoStageStatus.md) |  | [optional] [default to DeploymentProvisioningInfoStageStatus.UNKNOWN]
**started_at** | **datetime** |  | [optional] 
**finished_at** | **datetime** |  | [optional] 
**messages** | **List[str]** |  | [optional] 

## Example

```python
from koyeb.api_async.models.declare_step_progress_request import DeclareStepProgressRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DeclareStepProgressRequest from a JSON string
declare_step_progress_request_instance = DeclareStepProgressRequest.from_json(json)
# print the JSON string representation of the object
print(DeclareStepProgressRequest.to_json())

# convert the object into a dict
declare_step_progress_request_dict = declare_step_progress_request_instance.to_dict()
# create an instance of DeclareStepProgressRequest from a dict
declare_step_progress_request_from_dict = DeclareStepProgressRequest.from_dict(declare_step_progress_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


