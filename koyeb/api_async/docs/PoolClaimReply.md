# PoolClaimReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**claim_id** | **str** |  | [optional] 
**service_id** | **str** |  | [optional] 
**prewarmed** | **bool** |  | [optional] 

## Example

```python
from koyeb.api_async.models.pool_claim_reply import PoolClaimReply

# TODO update the JSON string below
json = "{}"
# create an instance of PoolClaimReply from a JSON string
pool_claim_reply_instance = PoolClaimReply.from_json(json)
# print the JSON string representation of the object
print(PoolClaimReply.to_json())

# convert the object into a dict
pool_claim_reply_dict = pool_claim_reply_instance.to_dict()
# create an instance of PoolClaimReply from a dict
pool_claim_reply_from_dict = PoolClaimReply.from_dict(pool_claim_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


