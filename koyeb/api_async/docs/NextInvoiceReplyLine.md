# NextInvoiceReplyLine


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amount_excluding_tax** | **int** |  | [optional] 
**period** | [**NextInvoiceReplyLinePeriod**](NextInvoiceReplyLinePeriod.md) |  | [optional] 
**plan_nickname** | **str** |  | [optional] 
**price** | [**NextInvoiceReplyLinePrice**](NextInvoiceReplyLinePrice.md) |  | [optional] 
**quantity** | **int** |  | [optional] 

## Example

```python
from koyeb.api_async.models.next_invoice_reply_line import NextInvoiceReplyLine

# TODO update the JSON string below
json = "{}"
# create an instance of NextInvoiceReplyLine from a JSON string
next_invoice_reply_line_instance = NextInvoiceReplyLine.from_json(json)
# print the JSON string representation of the object
print(NextInvoiceReplyLine.to_json())

# convert the object into a dict
next_invoice_reply_line_dict = next_invoice_reply_line_instance.to_dict()
# create an instance of NextInvoiceReplyLine from a dict
next_invoice_reply_line_from_dict = NextInvoiceReplyLine.from_dict(next_invoice_reply_line_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


