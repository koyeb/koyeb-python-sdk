# GetSnapshotReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**snapshot** | [**Snapshot**](Snapshot.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.get_snapshot_reply import GetSnapshotReply

# TODO update the JSON string below
json = "{}"
# create an instance of GetSnapshotReply from a JSON string
get_snapshot_reply_instance = GetSnapshotReply.from_json(json)
# print the JSON string representation of the object
print(GetSnapshotReply.to_json())

# convert the object into a dict
get_snapshot_reply_dict = get_snapshot_reply_instance.to_dict()
# create an instance of GetSnapshotReply from a dict
get_snapshot_reply_from_dict = GetSnapshotReply.from_dict(get_snapshot_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


