# Snapshot

The object that represents a snapshot. It can either be local, on a node, or remote, in a cold storage.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**size** | **int** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**deleted_at** | **datetime** |  | [optional] 
**organization_id** | **str** |  | [optional] 
**parent_volume_id** | **str** |  | [optional] 
**region** | **str** |  | [optional] 
**status** | [**SnapshotStatus**](SnapshotStatus.md) |  | [optional] [default to SnapshotStatus.SNAPSHOT_STATUS_INVALID]
**type** | [**SnapshotType**](SnapshotType.md) |  | [optional] [default to SnapshotType.SNAPSHOT_TYPE_INVALID]

## Example

```python
from koyeb.api_async.models.snapshot import Snapshot

# TODO update the JSON string below
json = "{}"
# create an instance of Snapshot from a JSON string
snapshot_instance = Snapshot.from_json(json)
# print the JSON string representation of the object
print(Snapshot.to_json())

# convert the object into a dict
snapshot_dict = snapshot_instance.to_dict()
# create an instance of Snapshot from a dict
snapshot_from_dict = Snapshot.from_dict(snapshot_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


