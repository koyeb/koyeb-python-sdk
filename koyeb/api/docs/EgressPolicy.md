# EgressPolicy


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**mode** | [**EgressPolicyMode**](EgressPolicyMode.md) |  | [optional] [default to EgressPolicyMode.EGRESS_POLICY_MODE_DEFAULT]
**allow_list** | [**List[NetworkPolicyDestination]**](NetworkPolicyDestination.md) | Allowed destinations (deny-by-default semantics under DENY_ALL). Ignored when mode is DEFAULT. | [optional] 

## Example

```python
from koyeb.api.models.egress_policy import EgressPolicy

# TODO update the JSON string below
json = "{}"
# create an instance of EgressPolicy from a JSON string
egress_policy_instance = EgressPolicy.from_json(json)
# print the JSON string representation of the object
print(EgressPolicy.to_json())

# convert the object into a dict
egress_policy_dict = egress_policy_instance.to_dict()
# create an instance of EgressPolicy from a dict
egress_policy_from_dict = EgressPolicy.from_dict(egress_policy_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


