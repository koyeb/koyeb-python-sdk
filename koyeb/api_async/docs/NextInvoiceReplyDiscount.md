# NextInvoiceReplyDiscount


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | [**NextInvoiceReplyDiscountType**](NextInvoiceReplyDiscountType.md) |  | [optional] [default to NextInvoiceReplyDiscountType.PERCENT_OFF]
**name** | **str** |  | [optional] 
**amount** | **str** |  | [optional] 

## Example

```python
from koyeb.api_async.models.next_invoice_reply_discount import NextInvoiceReplyDiscount

# TODO update the JSON string below
json = "{}"
# create an instance of NextInvoiceReplyDiscount from a JSON string
next_invoice_reply_discount_instance = NextInvoiceReplyDiscount.from_json(json)
# print the JSON string representation of the object
print(NextInvoiceReplyDiscount.to_json())

# convert the object into a dict
next_invoice_reply_discount_dict = next_invoice_reply_discount_instance.to_dict()
# create an instance of NextInvoiceReplyDiscount from a dict
next_invoice_reply_discount_from_dict = NextInvoiceReplyDiscount.from_dict(next_invoice_reply_discount_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


