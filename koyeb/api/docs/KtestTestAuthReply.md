# KtestTestAuthReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | **str** |  | [optional] 
**user_id** | **str** |  | [optional] 
**organization_id** | **str** |  | [optional] 
**workspace_id** | **str** |  | [optional] 

## Example

```python
from koyeb.api.models.ktest_test_auth_reply import KtestTestAuthReply

# TODO update the JSON string below
json = "{}"
# create an instance of KtestTestAuthReply from a JSON string
ktest_test_auth_reply_instance = KtestTestAuthReply.from_json(json)
# print the JSON string representation of the object
print(KtestTestAuthReply.to_json())

# convert the object into a dict
ktest_test_auth_reply_dict = ktest_test_auth_reply_instance.to_dict()
# create an instance of KtestTestAuthReply from a dict
ktest_test_auth_reply_from_dict = KtestTestAuthReply.from_dict(ktest_test_auth_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


