# ServiceViewActiveDeployment


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**state** | [**ServiceViewActiveDeploymentState**](ServiceViewActiveDeploymentState.md) |  | [optional] [default to ServiceViewActiveDeploymentState.NONE]
**id** | **str** |  | [optional] 
**missing** | **bool** |  | [optional] 
**status** | [**DeploymentStatus**](DeploymentStatus.md) |  | [optional] [default to DeploymentStatus.PENDING]
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 

## Example

```python
from koyeb.api_async.models.service_view_active_deployment import ServiceViewActiveDeployment

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceViewActiveDeployment from a JSON string
service_view_active_deployment_instance = ServiceViewActiveDeployment.from_json(json)
# print the JSON string representation of the object
print(ServiceViewActiveDeployment.to_json())

# convert the object into a dict
service_view_active_deployment_dict = service_view_active_deployment_instance.to_dict()
# create an instance of ServiceViewActiveDeployment from a dict
service_view_active_deployment_from_dict = ServiceViewActiveDeployment.from_dict(service_view_active_deployment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


