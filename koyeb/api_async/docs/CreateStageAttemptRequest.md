# CreateStageAttemptRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**secret** | **str** |  | [optional] 
**status** | [**DeploymentProvisioningInfoStageStatus**](DeploymentProvisioningInfoStageStatus.md) |  | [optional] [default to DeploymentProvisioningInfoStageStatus.UNKNOWN]
**started_at** | **datetime** |  | [optional] 
**messages** | **List[str]** |  | [optional] 
**steps** | **List[str]** |  | [optional] 

## Example

```python
from koyeb.api_async.models.create_stage_attempt_request import CreateStageAttemptRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateStageAttemptRequest from a JSON string
create_stage_attempt_request_instance = CreateStageAttemptRequest.from_json(json)
# print the JSON string representation of the object
print(CreateStageAttemptRequest.to_json())

# convert the object into a dict
create_stage_attempt_request_dict = create_stage_attempt_request_instance.to_dict()
# create an instance of CreateStageAttemptRequest from a dict
create_stage_attempt_request_from_dict = CreateStageAttemptRequest.from_dict(create_stage_attempt_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


