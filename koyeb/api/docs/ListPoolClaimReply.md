# ListPoolClaimReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**claims** | [**List[PoolClaim]**](PoolClaim.md) |  | [optional] 
**limit** | **int** |  | [optional] 
**offset** | **int** |  | [optional] 
**count** | **int** |  | [optional] 
**has_next** | **bool** |  | [optional] 

## Example

```python
from koyeb.api.models.list_pool_claim_reply import ListPoolClaimReply

# TODO update the JSON string below
json = "{}"
# create an instance of ListPoolClaimReply from a JSON string
list_pool_claim_reply_instance = ListPoolClaimReply.from_json(json)
# print the JSON string representation of the object
print(ListPoolClaimReply.to_json())

# convert the object into a dict
list_pool_claim_reply_dict = list_pool_claim_reply_instance.to_dict()
# create an instance of ListPoolClaimReply from a dict
list_pool_claim_reply_from_dict = ListPoolClaimReply.from_dict(list_pool_claim_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


