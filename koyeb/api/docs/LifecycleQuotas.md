# LifecycleQuotas


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delete_after_sleep_min** | **int** |  | [optional] 
**delete_after_sleep_max** | **int** |  | [optional] 
**delete_after_create_min** | **int** |  | [optional] 
**delete_after_create_max** | **int** |  | [optional] 

## Example

```python
from koyeb.api.models.lifecycle_quotas import LifecycleQuotas

# TODO update the JSON string below
json = "{}"
# create an instance of LifecycleQuotas from a JSON string
lifecycle_quotas_instance = LifecycleQuotas.from_json(json)
# print the JSON string representation of the object
print(LifecycleQuotas.to_json())

# convert the object into a dict
lifecycle_quotas_dict = lifecycle_quotas_instance.to_dict()
# create an instance of LifecycleQuotas from a dict
lifecycle_quotas_from_dict = LifecycleQuotas.from_dict(lifecycle_quotas_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


