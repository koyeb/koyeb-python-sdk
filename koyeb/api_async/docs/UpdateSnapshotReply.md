# UpdateSnapshotReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**snapshot** | [**Snapshot**](Snapshot.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.update_snapshot_reply import UpdateSnapshotReply

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateSnapshotReply from a JSON string
update_snapshot_reply_instance = UpdateSnapshotReply.from_json(json)
# print the JSON string representation of the object
print(UpdateSnapshotReply.to_json())

# convert the object into a dict
update_snapshot_reply_dict = update_snapshot_reply_instance.to_dict()
# create an instance of UpdateSnapshotReply from a dict
update_snapshot_reply_from_dict = UpdateSnapshotReply.from_dict(update_snapshot_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


