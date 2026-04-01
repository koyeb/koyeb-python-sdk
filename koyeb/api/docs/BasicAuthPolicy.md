# BasicAuthPolicy


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**username** | **str** |  | [optional] 
**password** | **str** |  | [optional] 

## Example

```python
from koyeb.api.models.basic_auth_policy import BasicAuthPolicy

# TODO update the JSON string below
json = "{}"
# create an instance of BasicAuthPolicy from a JSON string
basic_auth_policy_instance = BasicAuthPolicy.from_json(json)
# print the JSON string representation of the object
print(BasicAuthPolicy.to_json())

# convert the object into a dict
basic_auth_policy_dict = basic_auth_policy_instance.to_dict()
# create an instance of BasicAuthPolicy from a dict
basic_auth_policy_from_dict = BasicAuthPolicy.from_dict(basic_auth_policy_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


