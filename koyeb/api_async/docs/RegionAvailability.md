# RegionAvailability


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**availability** | [**AvailabilityLevel**](AvailabilityLevel.md) |  | [optional] [default to AvailabilityLevel.UNKNOWN]

## Example

```python
from koyeb.api_async.models.region_availability import RegionAvailability

# TODO update the JSON string below
json = "{}"
# create an instance of RegionAvailability from a JSON string
region_availability_instance = RegionAvailability.from_json(json)
# print the JSON string representation of the object
print(RegionAvailability.to_json())

# convert the object into a dict
region_availability_dict = region_availability_instance.to_dict()
# create an instance of RegionAvailability from a dict
region_availability_from_dict = RegionAvailability.from_dict(region_availability_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


