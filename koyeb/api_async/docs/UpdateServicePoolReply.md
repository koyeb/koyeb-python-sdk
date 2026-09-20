# UpdateServicePoolReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**service_pool** | [**ServicePool**](ServicePool.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.update_service_pool_reply import UpdateServicePoolReply

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateServicePoolReply from a JSON string
update_service_pool_reply_instance = UpdateServicePoolReply.from_json(json)
# print the JSON string representation of the object
print(UpdateServicePoolReply.to_json())

# convert the object into a dict
update_service_pool_reply_dict = update_service_pool_reply_instance.to_dict()
# create an instance of UpdateServicePoolReply from a dict
update_service_pool_reply_from_dict = UpdateServicePoolReply.from_dict(update_service_pool_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


