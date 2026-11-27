# AppLifeCycle


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delete_when_empty** | **bool** | If true, the app is deleted once it has no service left: either when its last service is deleted or, for an app that never had a service, once it is older than 15 minutes. | [optional] 

## Example

```python
from koyeb.api.models.app_life_cycle import AppLifeCycle

# TODO update the JSON string below
json = "{}"
# create an instance of AppLifeCycle from a JSON string
app_life_cycle_instance = AppLifeCycle.from_json(json)
# print the JSON string representation of the object
print(AppLifeCycle.to_json())

# convert the object into a dict
app_life_cycle_dict = app_life_cycle_instance.to_dict()
# create an instance of AppLifeCycle from a dict
app_life_cycle_from_dict = AppLifeCycle.from_dict(app_life_cycle_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


