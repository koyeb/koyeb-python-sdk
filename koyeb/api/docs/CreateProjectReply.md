# CreateProjectReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project** | [**Project**](Project.md) |  | [optional] 

## Example

```python
from koyeb.api.models.create_project_reply import CreateProjectReply

# TODO update the JSON string below
json = "{}"
# create an instance of CreateProjectReply from a JSON string
create_project_reply_instance = CreateProjectReply.from_json(json)
# print the JSON string representation of the object
print(CreateProjectReply.to_json())

# convert the object into a dict
create_project_reply_dict = create_project_reply_instance.to_dict()
# create an instance of CreateProjectReply from a dict
create_project_reply_from_dict = CreateProjectReply.from_dict(create_project_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


