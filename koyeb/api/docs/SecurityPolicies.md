# SecurityPolicies


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**basic_auths** | [**List[BasicAuthPolicy]**](BasicAuthPolicy.md) |  | [optional] 
**api_keys** | **List[str]** |  | [optional] 

## Example

```python
from koyeb.api.models.security_policies import SecurityPolicies

# TODO update the JSON string below
json = "{}"
# create an instance of SecurityPolicies from a JSON string
security_policies_instance = SecurityPolicies.from_json(json)
# print the JSON string representation of the object
print(SecurityPolicies.to_json())

# convert the object into a dict
security_policies_dict = security_policies_instance.to_dict()
# create an instance of SecurityPolicies from a dict
security_policies_from_dict = SecurityPolicies.from_dict(security_policies_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


