# ServiceViewRow


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**type** | [**ServiceType**](ServiceType.md) |  | [optional] [default to ServiceType.INVALID_TYPE]
**status** | [**ServiceStatus**](ServiceStatus.md) |  | [optional] [default to ServiceStatus.STARTING]
**messages** | **List[str]** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**app_id** | **str** |  | [optional] 
**app** | [**ServiceViewApp**](ServiceViewApp.md) |  | [optional] 
**active_deployment** | [**ServiceViewActiveDeployment**](ServiceViewActiveDeployment.md) |  | [optional] 
**latest_deployment** | [**ServiceViewLatestDeployment**](ServiceViewLatestDeployment.md) |  | [optional] 
**needs_attention** | **bool** |  | [optional] 
**regions** | **List[str]** |  | [optional] 
**instance_type** | **str** |  | [optional] 
**source** | [**ServiceViewSource**](ServiceViewSource.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.service_view_row import ServiceViewRow

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceViewRow from a JSON string
service_view_row_instance = ServiceViewRow.from_json(json)
# print the JSON string representation of the object
print(ServiceViewRow.to_json())

# convert the object into a dict
service_view_row_dict = service_view_row_instance.to_dict()
# create an instance of ServiceViewRow from a dict
service_view_row_from_dict = ServiceViewRow.from_dict(service_view_row_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


