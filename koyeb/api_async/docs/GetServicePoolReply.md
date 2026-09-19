# GetServicePoolReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**service_pool** | [**ServicePool**](ServicePool.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.get_service_pool_reply import GetServicePoolReply

# TODO update the JSON string below
json = "{}"
# create an instance of GetServicePoolReply from a JSON string
get_service_pool_reply_instance = GetServicePoolReply.from_json(json)
# print the JSON string representation of the object
print(GetServicePoolReply.to_json())

# convert the object into a dict
get_service_pool_reply_dict = get_service_pool_reply_instance.to_dict()
# create an instance of GetServicePoolReply from a dict
get_service_pool_reply_from_dict = GetServicePoolReply.from_dict(get_service_pool_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


