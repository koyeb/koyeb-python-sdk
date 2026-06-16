# DomainLoadBalancerQuotas


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**max_koyeb** | **int** |  | [optional] 

## Example

```python
from koyeb.api_async.models.domain_load_balancer_quotas import DomainLoadBalancerQuotas

# TODO update the JSON string below
json = "{}"
# create an instance of DomainLoadBalancerQuotas from a JSON string
domain_load_balancer_quotas_instance = DomainLoadBalancerQuotas.from_json(json)
# print the JSON string representation of the object
print(DomainLoadBalancerQuotas.to_json())

# convert the object into a dict
domain_load_balancer_quotas_dict = domain_load_balancer_quotas_instance.to_dict()
# create an instance of DomainLoadBalancerQuotas from a dict
domain_load_balancer_quotas_from_dict = DomainLoadBalancerQuotas.from_dict(domain_load_balancer_quotas_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


