# UpdateServicePool


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**size** | **int** |  | [optional] 
**definition** | [**DeploymentDefinition**](DeploymentDefinition.md) |  | [optional] 

## Example

```python
from koyeb.api.models.update_service_pool import UpdateServicePool

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateServicePool from a JSON string
update_service_pool_instance = UpdateServicePool.from_json(json)
# print the JSON string representation of the object
print(UpdateServicePool.to_json())

# convert the object into a dict
update_service_pool_dict = update_service_pool_instance.to_dict()
# create an instance of UpdateServicePool from a dict
update_service_pool_from_dict = UpdateServicePool.from_dict(update_service_pool_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


