# NextInvoiceReplyLinePeriod


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start** | **datetime** |  | [optional] 
**end** | **datetime** |  | [optional] 

## Example

```python
from koyeb.api_async.models.next_invoice_reply_line_period import NextInvoiceReplyLinePeriod

# TODO update the JSON string below
json = "{}"
# create an instance of NextInvoiceReplyLinePeriod from a JSON string
next_invoice_reply_line_period_instance = NextInvoiceReplyLinePeriod.from_json(json)
# print the JSON string representation of the object
print(NextInvoiceReplyLinePeriod.to_json())

# convert the object into a dict
next_invoice_reply_line_period_dict = next_invoice_reply_line_period_instance.to_dict()
# create an instance of NextInvoiceReplyLinePeriod from a dict
next_invoice_reply_line_period_from_dict = NextInvoiceReplyLinePeriod.from_dict(next_invoice_reply_line_period_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


