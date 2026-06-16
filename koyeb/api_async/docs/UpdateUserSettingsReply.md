# UpdateUserSettingsReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**settings** | [**UserSettings**](UserSettings.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.update_user_settings_reply import UpdateUserSettingsReply

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateUserSettingsReply from a JSON string
update_user_settings_reply_instance = UpdateUserSettingsReply.from_json(json)
# print the JSON string representation of the object
print(UpdateUserSettingsReply.to_json())

# convert the object into a dict
update_user_settings_reply_dict = update_user_settings_reply_instance.to_dict()
# create an instance of UpdateUserSettingsReply from a dict
update_user_settings_reply_from_dict = UpdateUserSettingsReply.from_dict(update_user_settings_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


