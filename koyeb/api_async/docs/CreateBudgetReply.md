# CreateBudgetReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**budget** | [**Budget**](Budget.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.create_budget_reply import CreateBudgetReply

# TODO update the JSON string below
json = "{}"
# create an instance of CreateBudgetReply from a JSON string
create_budget_reply_instance = CreateBudgetReply.from_json(json)
# print the JSON string representation of the object
print(CreateBudgetReply.to_json())

# convert the object into a dict
create_budget_reply_dict = create_budget_reply_instance.to_dict()
# create an instance of CreateBudgetReply from a dict
create_budget_reply_from_dict = CreateBudgetReply.from_dict(create_budget_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


