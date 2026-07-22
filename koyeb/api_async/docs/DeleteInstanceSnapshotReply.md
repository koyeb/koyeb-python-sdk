# DeleteInstanceSnapshotReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**instance_snapshot** | [**InstanceSnapshot**](InstanceSnapshot.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.delete_instance_snapshot_reply import DeleteInstanceSnapshotReply

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteInstanceSnapshotReply from a JSON string
delete_instance_snapshot_reply_instance = DeleteInstanceSnapshotReply.from_json(json)
# print the JSON string representation of the object
print(DeleteInstanceSnapshotReply.to_json())

# convert the object into a dict
delete_instance_snapshot_reply_dict = delete_instance_snapshot_reply_instance.to_dict()
# create an instance of DeleteInstanceSnapshotReply from a dict
delete_instance_snapshot_reply_from_dict = DeleteInstanceSnapshotReply.from_dict(delete_instance_snapshot_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


