# CreateServicePool


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**size** | **int** |  | [optional] 
**definition** | [**DeploymentDefinition**](DeploymentDefinition.md) |  | [optional] 

## Example

```python
from koyeb.api.models.create_service_pool import CreateServicePool

# TODO update the JSON string below
json = "{}"
# create an instance of CreateServicePool from a JSON string
create_service_pool_instance = CreateServicePool.from_json(json)
# print the JSON string representation of the object
print(CreateServicePool.to_json())

# convert the object into a dict
create_service_pool_dict = create_service_pool_instance.to_dict()
# create an instance of CreateServicePool from a dict
create_service_pool_from_dict = CreateServicePool.from_dict(create_service_pool_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


