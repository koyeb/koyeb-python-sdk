# ListProjectsReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**projects** | [**List[Project]**](Project.md) |  | [optional] 
**limit** | **int** |  | [optional] 
**offset** | **int** |  | [optional] 

## Example

```python
from koyeb.api.models.list_projects_reply import ListProjectsReply

# TODO update the JSON string below
json = "{}"
# create an instance of ListProjectsReply from a JSON string
list_projects_reply_instance = ListProjectsReply.from_json(json)
# print the JSON string representation of the object
print(ListProjectsReply.to_json())

# convert the object into a dict
list_projects_reply_dict = list_projects_reply_instance.to_dict()
# create an instance of ListProjectsReply from a dict
list_projects_reply_from_dict = ListProjectsReply.from_dict(list_projects_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


