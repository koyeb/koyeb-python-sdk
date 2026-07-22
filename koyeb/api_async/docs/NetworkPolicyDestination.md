# NetworkPolicyDestination


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cidr** | **str** | IPv4 or IPv6 CIDR (e.g. \&quot;10.0.0.0/8\&quot;, \&quot;2001:db8::/32\&quot;). Bare IPs are accepted at the API boundary and normalized to /32 (IPv4) or /128 (IPv6) before storage. | [optional] 

## Example

```python
from koyeb.api_async.models.network_policy_destination import NetworkPolicyDestination

# TODO update the JSON string below
json = "{}"
# create an instance of NetworkPolicyDestination from a JSON string
network_policy_destination_instance = NetworkPolicyDestination.from_json(json)
# print the JSON string representation of the object
print(NetworkPolicyDestination.to_json())

# convert the object into a dict
network_policy_destination_dict = network_policy_destination_instance.to_dict()
# create an instance of NetworkPolicyDestination from a dict
network_policy_destination_from_dict = NetworkPolicyDestination.from_dict(network_policy_destination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


