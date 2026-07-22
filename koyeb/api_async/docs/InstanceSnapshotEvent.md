# InstanceSnapshotEvent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**when** | **datetime** |  | [optional] 
**organization_id** | **str** |  | [optional] 
**instance_snapshot_id** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**message** | **str** |  | [optional] 
**metadata** | **object** |  | [optional] 

## Example

```python
from koyeb.api_async.models.instance_snapshot_event import InstanceSnapshotEvent

# TODO update the JSON string below
json = "{}"
# create an instance of InstanceSnapshotEvent from a JSON string
instance_snapshot_event_instance = InstanceSnapshotEvent.from_json(json)
# print the JSON string representation of the object
print(InstanceSnapshotEvent.to_json())

# convert the object into a dict
instance_snapshot_event_dict = instance_snapshot_event_instance.to_dict()
# create an instance of InstanceSnapshotEvent from a dict
instance_snapshot_event_from_dict = InstanceSnapshotEvent.from_dict(instance_snapshot_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


