# DeploymentProvisioningInfoStageBuildAttemptBuildStep


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**status** | [**DeploymentProvisioningInfoStageStatus**](DeploymentProvisioningInfoStageStatus.md) |  | [optional] [default to DeploymentProvisioningInfoStageStatus.UNKNOWN]
**messages** | **List[str]** |  | [optional] 
**started_at** | **datetime** |  | [optional] 
**finished_at** | **datetime** |  | [optional] 

## Example

```python
from koyeb.api_async.models.deployment_provisioning_info_stage_build_attempt_build_step import DeploymentProvisioningInfoStageBuildAttemptBuildStep

# TODO update the JSON string below
json = "{}"
# create an instance of DeploymentProvisioningInfoStageBuildAttemptBuildStep from a JSON string
deployment_provisioning_info_stage_build_attempt_build_step_instance = DeploymentProvisioningInfoStageBuildAttemptBuildStep.from_json(json)
# print the JSON string representation of the object
print(DeploymentProvisioningInfoStageBuildAttemptBuildStep.to_json())

# convert the object into a dict
deployment_provisioning_info_stage_build_attempt_build_step_dict = deployment_provisioning_info_stage_build_attempt_build_step_instance.to_dict()
# create an instance of DeploymentProvisioningInfoStageBuildAttemptBuildStep from a dict
deployment_provisioning_info_stage_build_attempt_build_step_from_dict = DeploymentProvisioningInfoStageBuildAttemptBuildStep.from_dict(deployment_provisioning_info_stage_build_attempt_build_step_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


