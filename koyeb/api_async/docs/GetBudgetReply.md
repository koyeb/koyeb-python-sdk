# GetBudgetReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**budget** | [**Budget**](Budget.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.get_budget_reply import GetBudgetReply

# TODO update the JSON string below
json = "{}"
# create an instance of GetBudgetReply from a JSON string
get_budget_reply_instance = GetBudgetReply.from_json(json)
# print the JSON string representation of the object
print(GetBudgetReply.to_json())

# convert the object into a dict
get_budget_reply_dict = get_budget_reply_instance.to_dict()
# create an instance of GetBudgetReply from a dict
get_budget_reply_from_dict = GetBudgetReply.from_dict(get_budget_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


