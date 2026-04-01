# GetProjectReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project** | [**Project**](Project.md) |  | [optional] 

## Example

```python
from koyeb.api.models.get_project_reply import GetProjectReply

# TODO update the JSON string below
json = "{}"
# create an instance of GetProjectReply from a JSON string
get_project_reply_instance = GetProjectReply.from_json(json)
# print the JSON string representation of the object
print(GetProjectReply.to_json())

# convert the object into a dict
get_project_reply_dict = get_project_reply_instance.to_dict()
# create an instance of GetProjectReply from a dict
get_project_reply_from_dict = GetProjectReply.from_dict(get_project_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


