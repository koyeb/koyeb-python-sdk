# PersistentVolumeEvent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**when** | **datetime** |  | [optional] 
**organization_id** | **str** |  | [optional] 
**persistent_volume_id** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**message** | **str** |  | [optional] 
**metadata** | **object** |  | [optional] 

## Example

```python
from koyeb.api_async.models.persistent_volume_event import PersistentVolumeEvent

# TODO update the JSON string below
json = "{}"
# create an instance of PersistentVolumeEvent from a JSON string
persistent_volume_event_instance = PersistentVolumeEvent.from_json(json)
# print the JSON string representation of the object
print(PersistentVolumeEvent.to_json())

# convert the object into a dict
persistent_volume_event_dict = persistent_volume_event_instance.to_dict()
# create an instance of PersistentVolumeEvent from a dict
persistent_volume_event_from_dict = PersistentVolumeEvent.from_dict(persistent_volume_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


