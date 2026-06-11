# UpdateUserSettingsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**failed_deployment_email_notification** | **bool** | (Optional) Toggle failed deployment email notification. | [optional] 

## Example

```python
from koyeb.api_async.models.update_user_settings_request import UpdateUserSettingsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateUserSettingsRequest from a JSON string
update_user_settings_request_instance = UpdateUserSettingsRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateUserSettingsRequest.to_json())

# convert the object into a dict
update_user_settings_request_dict = update_user_settings_request_instance.to_dict()
# create an instance of UpdateUserSettingsRequest from a dict
update_user_settings_request_from_dict = UpdateUserSettingsRequest.from_dict(update_user_settings_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


