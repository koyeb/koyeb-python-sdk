# LoginMethodReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**method** | [**LoginMethodReplyMethod**](LoginMethodReplyMethod.md) |  | [optional] [default to LoginMethodReplyMethod.KOYEB]

## Example

```python
from koyeb.api_async.models.login_method_reply import LoginMethodReply

# TODO update the JSON string below
json = "{}"
# create an instance of LoginMethodReply from a JSON string
login_method_reply_instance = LoginMethodReply.from_json(json)
# print the JSON string representation of the object
print(LoginMethodReply.to_json())

# convert the object into a dict
login_method_reply_dict = login_method_reply_instance.to_dict()
# create an instance of LoginMethodReply from a dict
login_method_reply_from_dict = LoginMethodReply.from_dict(login_method_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


