# UpdateApp


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**life_cycle** | [**AppLifeCycle**](AppLifeCycle.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.update_app import UpdateApp

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateApp from a JSON string
update_app_instance = UpdateApp.from_json(json)
# print the JSON string representation of the object
print(UpdateApp.to_json())

# convert the object into a dict
update_app_dict = update_app_instance.to_dict()
# create an instance of UpdateApp from a dict
update_app_from_dict = UpdateApp.from_dict(update_app_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


