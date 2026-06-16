# DomainLoadBalancerKoyeb


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**request_timeout_seconds** | **int** |  | [optional] 

## Example

```python
from koyeb.api_async.models.domain_load_balancer_koyeb import DomainLoadBalancerKoyeb

# TODO update the JSON string below
json = "{}"
# create an instance of DomainLoadBalancerKoyeb from a JSON string
domain_load_balancer_koyeb_instance = DomainLoadBalancerKoyeb.from_json(json)
# print the JSON string representation of the object
print(DomainLoadBalancerKoyeb.to_json())

# convert the object into a dict
domain_load_balancer_koyeb_dict = domain_load_balancer_koyeb_instance.to_dict()
# create an instance of DomainLoadBalancerKoyeb from a dict
domain_load_balancer_koyeb_from_dict = DomainLoadBalancerKoyeb.from_dict(domain_load_balancer_koyeb_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


