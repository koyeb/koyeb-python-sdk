# CreateSnapshotReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**snapshot** | [**Snapshot**](Snapshot.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.create_snapshot_reply import CreateSnapshotReply

# TODO update the JSON string below
json = "{}"
# create an instance of CreateSnapshotReply from a JSON string
create_snapshot_reply_instance = CreateSnapshotReply.from_json(json)
# print the JSON string representation of the object
print(CreateSnapshotReply.to_json())

# convert the object into a dict
create_snapshot_reply_dict = create_snapshot_reply_instance.to_dict()
# create an instance of CreateSnapshotReply from a dict
create_snapshot_reply_from_dict = CreateSnapshotReply.from_dict(create_snapshot_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


