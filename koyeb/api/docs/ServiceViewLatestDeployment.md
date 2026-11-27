# ServiceViewLatestDeployment


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**state** | [**ServiceViewLatestDeploymentState**](ServiceViewLatestDeploymentState.md) |  | [optional] [default to ServiceViewLatestDeploymentState.NONE]
**id** | **str** |  | [optional] 
**missing** | **bool** |  | [optional] 
**status** | [**DeploymentStatus**](DeploymentStatus.md) |  | [optional] [default to DeploymentStatus.PENDING]
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 

## Example

```python
from koyeb.api.models.service_view_latest_deployment import ServiceViewLatestDeployment

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceViewLatestDeployment from a JSON string
service_view_latest_deployment_instance = ServiceViewLatestDeployment.from_json(json)
# print the JSON string representation of the object
print(ServiceViewLatestDeployment.to_json())

# convert the object into a dict
service_view_latest_deployment_dict = service_view_latest_deployment_instance.to_dict()
# create an instance of ServiceViewLatestDeployment from a dict
service_view_latest_deployment_from_dict = ServiceViewLatestDeployment.from_dict(service_view_latest_deployment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


