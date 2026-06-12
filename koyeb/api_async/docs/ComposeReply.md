# ComposeReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**app** | [**App**](App.md) |  | [optional] 
**services** | [**List[Service]**](Service.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.compose_reply import ComposeReply

# TODO update the JSON string below
json = "{}"
# create an instance of ComposeReply from a JSON string
compose_reply_instance = ComposeReply.from_json(json)
# print the JSON string representation of the object
print(ComposeReply.to_json())

# convert the object into a dict
compose_reply_dict = compose_reply_instance.to_dict()
# create an instance of ComposeReply from a dict
compose_reply_from_dict = ComposeReply.from_dict(compose_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


