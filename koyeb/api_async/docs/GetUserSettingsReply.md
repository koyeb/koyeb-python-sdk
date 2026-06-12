# GetUserSettingsReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**settings** | [**UserSettings**](UserSettings.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.get_user_settings_reply import GetUserSettingsReply

# TODO update the JSON string below
json = "{}"
# create an instance of GetUserSettingsReply from a JSON string
get_user_settings_reply_instance = GetUserSettingsReply.from_json(json)
# print the JSON string representation of the object
print(GetUserSettingsReply.to_json())

# convert the object into a dict
get_user_settings_reply_dict = get_user_settings_reply_instance.to_dict()
# create an instance of GetUserSettingsReply from a dict
get_user_settings_reply_from_dict = GetUserSettingsReply.from_dict(get_user_settings_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


