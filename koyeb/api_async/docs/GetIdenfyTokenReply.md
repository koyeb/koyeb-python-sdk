# GetIdenfyTokenReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**auth_token** | **str** |  | [optional] 

## Example

```python
from koyeb.api_async.models.get_idenfy_token_reply import GetIdenfyTokenReply

# TODO update the JSON string below
json = "{}"
# create an instance of GetIdenfyTokenReply from a JSON string
get_idenfy_token_reply_instance = GetIdenfyTokenReply.from_json(json)
# print the JSON string representation of the object
print(GetIdenfyTokenReply.to_json())

# convert the object into a dict
get_idenfy_token_reply_dict = get_idenfy_token_reply_instance.to_dict()
# create an instance of GetIdenfyTokenReply from a dict
get_idenfy_token_reply_from_dict = GetIdenfyTokenReply.from_dict(get_idenfy_token_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


