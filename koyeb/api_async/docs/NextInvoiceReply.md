# NextInvoiceReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**stripe_invoice** | **object** |  | [optional] 
**lines** | [**List[NextInvoiceReplyLine]**](NextInvoiceReplyLine.md) |  | [optional] 
**discounts** | [**List[NextInvoiceReplyDiscount]**](NextInvoiceReplyDiscount.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.next_invoice_reply import NextInvoiceReply

# TODO update the JSON string below
json = "{}"
# create an instance of NextInvoiceReply from a JSON string
next_invoice_reply_instance = NextInvoiceReply.from_json(json)
# print the JSON string representation of the object
print(NextInvoiceReply.to_json())

# convert the object into a dict
next_invoice_reply_dict = next_invoice_reply_instance.to_dict()
# create an instance of NextInvoiceReply from a dict
next_invoice_reply_from_dict = NextInvoiceReply.from_dict(next_invoice_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


