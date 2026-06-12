# ListUserOrganizationsReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**organizations** | [**List[Organization]**](Organization.md) |  | [optional] 
**limit** | **int** |  | [optional] 
**offset** | **int** |  | [optional] 
**has_next** | **bool** |  | [optional] 

## Example

```python
from koyeb.api_async.models.list_user_organizations_reply import ListUserOrganizationsReply

# TODO update the JSON string below
json = "{}"
# create an instance of ListUserOrganizationsReply from a JSON string
list_user_organizations_reply_instance = ListUserOrganizationsReply.from_json(json)
# print the JSON string representation of the object
print(ListUserOrganizationsReply.to_json())

# convert the object into a dict
list_user_organizations_reply_dict = list_user_organizations_reply_instance.to_dict()
# create an instance of ListUserOrganizationsReply from a dict
list_user_organizations_reply_from_dict = ListUserOrganizationsReply.from_dict(list_user_organizations_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


