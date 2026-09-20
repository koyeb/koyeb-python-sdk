# PersistentVolumeRegionUsage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**region** | **str** |  | [optional] 
**total_size_gb_used** | **int** |  | [optional] 
**total_size_gb_limit** | **int** |  | [optional] 

## Example

```python
from koyeb.api.models.persistent_volume_region_usage import PersistentVolumeRegionUsage

# TODO update the JSON string below
json = "{}"
# create an instance of PersistentVolumeRegionUsage from a JSON string
persistent_volume_region_usage_instance = PersistentVolumeRegionUsage.from_json(json)
# print the JSON string representation of the object
print(PersistentVolumeRegionUsage.to_json())

# convert the object into a dict
persistent_volume_region_usage_dict = persistent_volume_region_usage_instance.to_dict()
# create an instance of PersistentVolumeRegionUsage from a dict
persistent_volume_region_usage_from_dict = PersistentVolumeRegionUsage.from_dict(persistent_volume_region_usage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


