# ServiceViewApp


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 

## Example

```python
from koyeb.api_async.models.service_view_app import ServiceViewApp

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceViewApp from a JSON string
service_view_app_instance = ServiceViewApp.from_json(json)
# print the JSON string representation of the object
print(ServiceViewApp.to_json())

# convert the object into a dict
service_view_app_dict = service_view_app_instance.to_dict()
# create an instance of ServiceViewApp from a dict
service_view_app_from_dict = ServiceViewApp.from_dict(service_view_app_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


