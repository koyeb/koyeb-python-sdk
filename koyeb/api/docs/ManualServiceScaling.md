# ManualServiceScaling


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scopes** | **List[str]** |  | [optional] 
**instances** | **int** |  | [optional] 

## Example

```python
from koyeb.api.models.manual_service_scaling import ManualServiceScaling

# TODO update the JSON string below
json = "{}"
# create an instance of ManualServiceScaling from a JSON string
manual_service_scaling_instance = ManualServiceScaling.from_json(json)
# print the JSON string representation of the object
print(ManualServiceScaling.to_json())

# convert the object into a dict
manual_service_scaling_dict = manual_service_scaling_instance.to_dict()
# create an instance of ManualServiceScaling from a dict
manual_service_scaling_from_dict = ManualServiceScaling.from_dict(manual_service_scaling_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


