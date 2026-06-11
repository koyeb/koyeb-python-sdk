# InstanceAvailability


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**regions** | [**Dict[str, RegionAvailability]**](RegionAvailability.md) |  | [optional] 
**availability** | [**AvailabilityLevel**](AvailabilityLevel.md) |  | [optional] [default to AvailabilityLevel.UNKNOWN]

## Example

```python
from koyeb.api_async.models.instance_availability import InstanceAvailability

# TODO update the JSON string below
json = "{}"
# create an instance of InstanceAvailability from a JSON string
instance_availability_instance = InstanceAvailability.from_json(json)
# print the JSON string representation of the object
print(InstanceAvailability.to_json())

# convert the object into a dict
instance_availability_dict = instance_availability_instance.to_dict()
# create an instance of InstanceAvailability from a dict
instance_availability_from_dict = InstanceAvailability.from_dict(instance_availability_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


