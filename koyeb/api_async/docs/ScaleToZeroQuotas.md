# ScaleToZeroQuotas


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_deep_sleep_enabled** | **bool** |  | [optional] 
**deep_sleep_idle_delay_min** | **int** |  | [optional] 
**deep_sleep_idle_delay_max** | **int** |  | [optional] 
**is_light_sleep_enabled** | **bool** |  | [optional] 
**light_sleep_idle_delay_min** | **int** |  | [optional] 
**light_sleep_idle_delay_max** | **int** |  | [optional] 

## Example

```python
from koyeb.api_async.models.scale_to_zero_quotas import ScaleToZeroQuotas

# TODO update the JSON string below
json = "{}"
# create an instance of ScaleToZeroQuotas from a JSON string
scale_to_zero_quotas_instance = ScaleToZeroQuotas.from_json(json)
# print the JSON string representation of the object
print(ScaleToZeroQuotas.to_json())

# convert the object into a dict
scale_to_zero_quotas_dict = scale_to_zero_quotas_instance.to_dict()
# create an instance of ScaleToZeroQuotas from a dict
scale_to_zero_quotas_from_dict = ScaleToZeroQuotas.from_dict(scale_to_zero_quotas_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


