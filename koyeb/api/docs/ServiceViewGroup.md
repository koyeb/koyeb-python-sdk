# ServiceViewGroup


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**by** | [**ServiceViewGroupBy**](ServiceViewGroupBy.md) |  | [optional] [default to ServiceViewGroupBy.NO_GROUP]
**key** | **str** |  | [optional] 
**label** | **str** |  | [optional] 
**count** | **int** |  | [optional] 

## Example

```python
from koyeb.api.models.service_view_group import ServiceViewGroup

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceViewGroup from a JSON string
service_view_group_instance = ServiceViewGroup.from_json(json)
# print the JSON string representation of the object
print(ServiceViewGroup.to_json())

# convert the object into a dict
service_view_group_dict = service_view_group_instance.to_dict()
# create an instance of ServiceViewGroup from a dict
service_view_group_from_dict = ServiceViewGroup.from_dict(service_view_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


