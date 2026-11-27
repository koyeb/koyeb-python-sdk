# ServiceViewSource


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | [**ServiceViewSourceType**](ServiceViewSourceType.md) |  | [optional] [default to ServiceViewSourceType.UNKNOWN]
**reference** | **str** |  | [optional] 

## Example

```python
from koyeb.api_async.models.service_view_source import ServiceViewSource

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceViewSource from a JSON string
service_view_source_instance = ServiceViewSource.from_json(json)
# print the JSON string representation of the object
print(ServiceViewSource.to_json())

# convert the object into a dict
service_view_source_dict = service_view_source_instance.to_dict()
# create an instance of ServiceViewSource from a dict
service_view_source_from_dict = ServiceViewSource.from_dict(service_view_source_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


