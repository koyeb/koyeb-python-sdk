# CheckCouponReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**percent_off** | **float** |  | [optional] 
**amount_off** | **str** |  | [optional] 
**currency** | **str** |  | [optional] 

## Example

```python
from koyeb.api.models.check_coupon_reply import CheckCouponReply

# TODO update the JSON string below
json = "{}"
# create an instance of CheckCouponReply from a JSON string
check_coupon_reply_instance = CheckCouponReply.from_json(json)
# print the JSON string representation of the object
print(CheckCouponReply.to_json())

# convert the object into a dict
check_coupon_reply_dict = check_coupon_reply_instance.to_dict()
# create an instance of CheckCouponReply from a dict
check_coupon_reply_from_dict = CheckCouponReply.from_dict(check_coupon_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


