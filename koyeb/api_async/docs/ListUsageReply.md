# ListUsageReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**usage** | [**CatalogUsage**](CatalogUsage.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.list_usage_reply import ListUsageReply

# TODO update the JSON string below
json = "{}"
# create an instance of ListUsageReply from a JSON string
list_usage_reply_instance = ListUsageReply.from_json(json)
# print the JSON string representation of the object
print(ListUsageReply.to_json())

# convert the object into a dict
list_usage_reply_dict = list_usage_reply_instance.to_dict()
# create an instance of ListUsageReply from a dict
list_usage_reply_from_dict = ListUsageReply.from_dict(list_usage_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


