# Deployment


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**allocated_at** | **datetime** |  | [optional] 
**started_at** | **datetime** |  | [optional] 
**succeeded_at** | **datetime** |  | [optional] 
**terminated_at** | **datetime** |  | [optional] 
**organization_id** | **str** |  | [optional] 
**project_id** | **str** |  | [optional] 
**app_id** | **str** |  | [optional] 
**service_id** | **str** |  | [optional] 
**parent_id** | **str** |  | [optional] 
**child_id** | **str** |  | [optional] 
**status** | [**DeploymentStatus**](DeploymentStatus.md) |  | [optional] [default to DeploymentStatus.PENDING]
**metadata** | [**DeploymentMetadata**](DeploymentMetadata.md) |  | [optional] 
**definition** | [**DeploymentDefinition**](DeploymentDefinition.md) |  | [optional] 
**messages** | **List[str]** |  | [optional] 
**provisioning_info** | [**DeploymentProvisioningInfo**](DeploymentProvisioningInfo.md) |  | [optional] 
**database_info** | [**DeploymentDatabaseInfo**](DeploymentDatabaseInfo.md) |  | [optional] 
**skip_build** | **bool** |  | [optional] 
**role** | [**DeploymentRole**](DeploymentRole.md) |  | [optional] [default to DeploymentRole.INVALID]
**version** | **str** |  | [optional] 
**deployment_group** | **str** |  | [optional] 
**instance_snapshot_id** | **str** |  | [optional] 
**created_by** | **str** | CreatedBy is the user_id of the user that called CreateService or UpdateService. It&#39;s optional because CreateService or UpdateService can be called by a machine, using a token that&#39;s organization scoped, not user scoped. | [optional] 

## Example

```python
from koyeb.api_async.models.deployment import Deployment

# TODO update the JSON string below
json = "{}"
# create an instance of Deployment from a JSON string
deployment_instance = Deployment.from_json(json)
# print the JSON string representation of the object
print(Deployment.to_json())

# convert the object into a dict
deployment_dict = deployment_instance.to_dict()
# create an instance of Deployment from a dict
deployment_from_dict = Deployment.from_dict(deployment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


