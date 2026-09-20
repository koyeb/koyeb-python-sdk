# InstanceTypeUsage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**instance_type** | **str** |  | [optional] 
**used** | **int** |  | [optional] 
**limit** | **int** |  | [optional] 

## Example

```python
from koyeb.api_async.models.instance_type_usage import InstanceTypeUsage

# TODO update the JSON string below
json = "{}"
# create an instance of InstanceTypeUsage from a JSON string
instance_type_usage_instance = InstanceTypeUsage.from_json(json)
# print the JSON string representation of the object
print(InstanceTypeUsage.to_json())

# convert the object into a dict
instance_type_usage_dict = instance_type_usage_instance.to_dict()
# create an instance of InstanceTypeUsage from a dict
instance_type_usage_from_dict = InstanceTypeUsage.from_dict(instance_type_usage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


