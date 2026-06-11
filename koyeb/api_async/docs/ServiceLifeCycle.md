# ServiceLifeCycle


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delete_after_sleep** | **int** |  | [optional] 
**delete_after_create** | **int** |  | [optional] 

## Example

```python
from koyeb.api_async.models.service_life_cycle import ServiceLifeCycle

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceLifeCycle from a JSON string
service_life_cycle_instance = ServiceLifeCycle.from_json(json)
# print the JSON string representation of the object
print(ServiceLifeCycle.to_json())

# convert the object into a dict
service_life_cycle_dict = service_life_cycle_instance.to_dict()
# create an instance of ServiceLifeCycle from a dict
service_life_cycle_from_dict = ServiceLifeCycle.from_dict(service_life_cycle_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


