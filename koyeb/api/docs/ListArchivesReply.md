# ListArchivesReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**archives** | [**List[Archive]**](Archive.md) |  | [optional] 
**limit** | **int** |  | [optional] 
**offset** | **int** |  | [optional] 
**count** | **int** |  | [optional] 
**has_next** | **bool** |  | [optional] 

## Example

```python
from koyeb.api.models.list_archives_reply import ListArchivesReply

# TODO update the JSON string below
json = "{}"
# create an instance of ListArchivesReply from a JSON string
list_archives_reply_instance = ListArchivesReply.from_json(json)
# print the JSON string representation of the object
print(ListArchivesReply.to_json())

# convert the object into a dict
list_archives_reply_dict = list_archives_reply_instance.to_dict()
# create an instance of ListArchivesReply from a dict
list_archives_reply_from_dict = ListArchivesReply.from_dict(list_archives_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


