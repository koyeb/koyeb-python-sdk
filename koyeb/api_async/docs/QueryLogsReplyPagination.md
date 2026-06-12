# QueryLogsReplyPagination


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**has_more** | **bool** |  | [optional] 
**next_start** | **datetime** |  | [optional] 
**next_end** | **datetime** |  | [optional] 

## Example

```python
from koyeb.api_async.models.query_logs_reply_pagination import QueryLogsReplyPagination

# TODO update the JSON string below
json = "{}"
# create an instance of QueryLogsReplyPagination from a JSON string
query_logs_reply_pagination_instance = QueryLogsReplyPagination.from_json(json)
# print the JSON string representation of the object
print(QueryLogsReplyPagination.to_json())

# convert the object into a dict
query_logs_reply_pagination_dict = query_logs_reply_pagination_instance.to_dict()
# create an instance of QueryLogsReplyPagination from a dict
query_logs_reply_pagination_from_dict = QueryLogsReplyPagination.from_dict(query_logs_reply_pagination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


