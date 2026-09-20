# GetPoolClaimReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**claim** | [**PoolClaim**](PoolClaim.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.get_pool_claim_reply import GetPoolClaimReply

# TODO update the JSON string below
json = "{}"
# create an instance of GetPoolClaimReply from a JSON string
get_pool_claim_reply_instance = GetPoolClaimReply.from_json(json)
# print the JSON string representation of the object
print(GetPoolClaimReply.to_json())

# convert the object into a dict
get_pool_claim_reply_dict = get_pool_claim_reply_instance.to_dict()
# create an instance of GetPoolClaimReply from a dict
get_pool_claim_reply_from_dict = GetPoolClaimReply.from_dict(get_pool_claim_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


