# DeclareStageProgressRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**secret** | **str** |  | [optional] 
**status** | [**DeploymentProvisioningInfoStageStatus**](DeploymentProvisioningInfoStageStatus.md) |  | [optional] [default to DeploymentProvisioningInfoStageStatus.UNKNOWN]
**finished_at** | **datetime** |  | [optional] 
**messages** | **List[str]** |  | [optional] 
**image_pushed** | **bool** |  | [optional] 
**internal_failure** | **bool** |  | [optional] 
**retryable_failure** | **bool** |  | [optional] 

## Example

```python
from koyeb.api_async.models.declare_stage_progress_request import DeclareStageProgressRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DeclareStageProgressRequest from a JSON string
declare_stage_progress_request_instance = DeclareStageProgressRequest.from_json(json)
# print the JSON string representation of the object
print(DeclareStageProgressRequest.to_json())

# convert the object into a dict
declare_stage_progress_request_dict = declare_stage_progress_request_instance.to_dict()
# create an instance of DeclareStageProgressRequest from a dict
declare_stage_progress_request_from_dict = DeclareStageProgressRequest.from_dict(declare_stage_progress_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


