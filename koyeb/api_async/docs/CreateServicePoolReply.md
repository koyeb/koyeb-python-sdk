# CreateServicePoolReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**service_pool** | [**ServicePool**](ServicePool.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.create_service_pool_reply import CreateServicePoolReply

# TODO update the JSON string below
json = "{}"
# create an instance of CreateServicePoolReply from a JSON string
create_service_pool_reply_instance = CreateServicePoolReply.from_json(json)
# print the JSON string representation of the object
print(CreateServicePoolReply.to_json())

# convert the object into a dict
create_service_pool_reply_dict = create_service_pool_reply_instance.to_dict()
# create an instance of CreateServicePoolReply from a dict
create_service_pool_reply_from_dict = CreateServicePoolReply.from_dict(create_service_pool_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


