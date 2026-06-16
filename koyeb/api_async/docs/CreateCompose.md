# CreateCompose


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**app** | [**CreateApp**](CreateApp.md) |  | [optional] 
**services** | [**List[CreateService]**](CreateService.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.create_compose import CreateCompose

# TODO update the JSON string below
json = "{}"
# create an instance of CreateCompose from a JSON string
create_compose_instance = CreateCompose.from_json(json)
# print the JSON string representation of the object
print(CreateCompose.to_json())

# convert the object into a dict
create_compose_dict = create_compose_instance.to_dict()
# create an instance of CreateCompose from a dict
create_compose_from_dict = CreateCompose.from_dict(create_compose_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


