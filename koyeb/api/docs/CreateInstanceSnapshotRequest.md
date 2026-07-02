# CreateInstanceSnapshotRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**instance_id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**type** | [**InstanceSnapshotType**](InstanceSnapshotType.md) |  | [optional] [default to InstanceSnapshotType.INSTANCE_SNAPSHOT_TYPE_INVALID]

## Example

```python
from koyeb.api.models.create_instance_snapshot_request import CreateInstanceSnapshotRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateInstanceSnapshotRequest from a JSON string
create_instance_snapshot_request_instance = CreateInstanceSnapshotRequest.from_json(json)
# print the JSON string representation of the object
print(CreateInstanceSnapshotRequest.to_json())

# convert the object into a dict
create_instance_snapshot_request_dict = create_instance_snapshot_request_instance.to_dict()
# create an instance of CreateInstanceSnapshotRequest from a dict
create_instance_snapshot_request_from_dict = CreateInstanceSnapshotRequest.from_dict(create_instance_snapshot_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


