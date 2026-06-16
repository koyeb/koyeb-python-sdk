# UpdateOrganizationNameReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**organization** | [**Organization**](Organization.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.update_organization_name_reply import UpdateOrganizationNameReply

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateOrganizationNameReply from a JSON string
update_organization_name_reply_instance = UpdateOrganizationNameReply.from_json(json)
# print the JSON string representation of the object
print(UpdateOrganizationNameReply.to_json())

# convert the object into a dict
update_organization_name_reply_dict = update_organization_name_reply_instance.to_dict()
# create an instance of UpdateOrganizationNameReply from a dict
update_organization_name_reply_from_dict = UpdateOrganizationNameReply.from_dict(update_organization_name_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


