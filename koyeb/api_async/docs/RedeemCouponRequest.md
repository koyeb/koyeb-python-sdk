# RedeemCouponRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** |  | [optional] 

## Example

```python
from koyeb.api_async.models.redeem_coupon_request import RedeemCouponRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RedeemCouponRequest from a JSON string
redeem_coupon_request_instance = RedeemCouponRequest.from_json(json)
# print the JSON string representation of the object
print(RedeemCouponRequest.to_json())

# convert the object into a dict
redeem_coupon_request_dict = redeem_coupon_request_instance.to_dict()
# create an instance of RedeemCouponRequest from a dict
redeem_coupon_request_from_dict = RedeemCouponRequest.from_dict(redeem_coupon_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


