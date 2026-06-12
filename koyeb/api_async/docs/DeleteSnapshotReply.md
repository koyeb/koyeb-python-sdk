# DeleteSnapshotReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**snapshot** | [**Snapshot**](Snapshot.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.delete_snapshot_reply import DeleteSnapshotReply

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteSnapshotReply from a JSON string
delete_snapshot_reply_instance = DeleteSnapshotReply.from_json(json)
# print the JSON string representation of the object
print(DeleteSnapshotReply.to_json())

# convert the object into a dict
delete_snapshot_reply_dict = delete_snapshot_reply_instance.to_dict()
# create an instance of DeleteSnapshotReply from a dict
delete_snapshot_reply_from_dict = DeleteSnapshotReply.from_dict(delete_snapshot_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


