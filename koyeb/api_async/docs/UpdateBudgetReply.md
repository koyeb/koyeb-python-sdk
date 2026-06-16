# UpdateBudgetReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**budget** | [**Budget**](Budget.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.update_budget_reply import UpdateBudgetReply

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateBudgetReply from a JSON string
update_budget_reply_instance = UpdateBudgetReply.from_json(json)
# print the JSON string representation of the object
print(UpdateBudgetReply.to_json())

# convert the object into a dict
update_budget_reply_dict = update_budget_reply_instance.to_dict()
# create an instance of UpdateBudgetReply from a dict
update_budget_reply_from_dict = UpdateBudgetReply.from_dict(update_budget_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


