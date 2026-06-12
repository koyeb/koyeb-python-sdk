# CreateAccessTokenReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**token** | **str** |  | [optional] 

## Example

```python
from koyeb.api_async.models.create_access_token_reply import CreateAccessTokenReply

# TODO update the JSON string below
json = "{}"
# create an instance of CreateAccessTokenReply from a JSON string
create_access_token_reply_instance = CreateAccessTokenReply.from_json(json)
# print the JSON string representation of the object
print(CreateAccessTokenReply.to_json())

# convert the object into a dict
create_access_token_reply_dict = create_access_token_reply_instance.to_dict()
# create an instance of CreateAccessTokenReply from a dict
create_access_token_reply_from_dict = CreateAccessTokenReply.from_dict(create_access_token_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


