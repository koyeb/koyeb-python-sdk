# GetArchiveReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**archive** | [**Archive**](Archive.md) |  | [optional] 

## Example

```python
from koyeb.api.models.get_archive_reply import GetArchiveReply

# TODO update the JSON string below
json = "{}"
# create an instance of GetArchiveReply from a JSON string
get_archive_reply_instance = GetArchiveReply.from_json(json)
# print the JSON string representation of the object
print(GetArchiveReply.to_json())

# convert the object into a dict
get_archive_reply_dict = get_archive_reply_instance.to_dict()
# create an instance of GetArchiveReply from a dict
get_archive_reply_from_dict = GetArchiveReply.from_dict(get_archive_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


