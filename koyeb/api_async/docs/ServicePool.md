# ServicePool


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**organization_id** | **str** |  | [optional] 
**workspace_id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**size** | **int** |  | [optional] 
**ready_count** | **int** |  | [optional] 
**definition** | [**DeploymentDefinition**](DeploymentDefinition.md) |  | [optional] 
**status** | [**ServicePoolStatus**](ServicePoolStatus.md) |  | [optional] [default to ServicePoolStatus.UNSPECIFIED]
**messages** | **List[str]** |  | [optional] 
**generation** | **str** |  | [optional] 
**customer_id** | **str** |  | [optional] 

## Example

```python
from koyeb.api_async.models.service_pool import ServicePool

# TODO update the JSON string below
json = "{}"
# create an instance of ServicePool from a JSON string
service_pool_instance = ServicePool.from_json(json)
# print the JSON string representation of the object
print(ServicePool.to_json())

# convert the object into a dict
service_pool_dict = service_pool_instance.to_dict()
# create an instance of ServicePool from a dict
service_pool_from_dict = ServicePool.from_dict(service_pool_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


