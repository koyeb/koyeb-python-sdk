# GetInstanceSnapshotReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**instance_snapshot** | [**InstanceSnapshot**](InstanceSnapshot.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.get_instance_snapshot_reply import GetInstanceSnapshotReply

# TODO update the JSON string below
json = "{}"
# create an instance of GetInstanceSnapshotReply from a JSON string
get_instance_snapshot_reply_instance = GetInstanceSnapshotReply.from_json(json)
# print the JSON string representation of the object
print(GetInstanceSnapshotReply.to_json())

# convert the object into a dict
get_instance_snapshot_reply_dict = get_instance_snapshot_reply_instance.to_dict()
# create an instance of GetInstanceSnapshotReply from a dict
get_instance_snapshot_reply_from_dict = GetInstanceSnapshotReply.from_dict(get_instance_snapshot_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


