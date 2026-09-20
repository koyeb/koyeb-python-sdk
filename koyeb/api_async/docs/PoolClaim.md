# PoolClaim


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**pool_id** | **str** |  | [optional] 
**service_id** | **str** |  | [optional] 
**request_id** | **str** |  | [optional] 
**status** | [**PoolClaimStatus**](PoolClaimStatus.md) |  | [optional] [default to PoolClaimStatus.UNSPECIFIED]
**organization_id** | **str** |  | [optional] 
**workspace_id** | **str** |  | [optional] 
**customer_id** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**fulfilled_at** | **datetime** |  | [optional] 
**released_at** | **datetime** |  | [optional] 
**pool_generation** | **str** |  | [optional] 

## Example

```python
from koyeb.api_async.models.pool_claim import PoolClaim

# TODO update the JSON string below
json = "{}"
# create an instance of PoolClaim from a JSON string
pool_claim_instance = PoolClaim.from_json(json)
# print the JSON string representation of the object
print(PoolClaim.to_json())

# convert the object into a dict
pool_claim_dict = pool_claim_instance.to_dict()
# create an instance of PoolClaim from a dict
pool_claim_from_dict = PoolClaim.from_dict(pool_claim_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


