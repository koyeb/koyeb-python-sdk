# PoolClaimRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pool_id** | **str** |  | [optional] 
**request_id** | **str** |  | [optional] 

## Example

```python
from koyeb.api_async.models.pool_claim_request import PoolClaimRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PoolClaimRequest from a JSON string
pool_claim_request_instance = PoolClaimRequest.from_json(json)
# print the JSON string representation of the object
print(PoolClaimRequest.to_json())

# convert the object into a dict
pool_claim_request_dict = pool_claim_request_instance.to_dict()
# create an instance of PoolClaimRequest from a dict
pool_claim_request_from_dict = PoolClaimRequest.from_dict(pool_claim_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


