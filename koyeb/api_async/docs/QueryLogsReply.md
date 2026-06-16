# QueryLogsReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[LogEntry]**](LogEntry.md) |  | [optional] 
**pagination** | [**QueryLogsReplyPagination**](QueryLogsReplyPagination.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.query_logs_reply import QueryLogsReply

# TODO update the JSON string below
json = "{}"
# create an instance of QueryLogsReply from a JSON string
query_logs_reply_instance = QueryLogsReply.from_json(json)
# print the JSON string representation of the object
print(QueryLogsReply.to_json())

# convert the object into a dict
query_logs_reply_dict = query_logs_reply_instance.to_dict()
# create an instance of QueryLogsReply from a dict
query_logs_reply_from_dict = QueryLogsReply.from_dict(query_logs_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


