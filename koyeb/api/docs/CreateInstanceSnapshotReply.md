# CreateInstanceSnapshotReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**instance_snapshot** | [**InstanceSnapshot**](InstanceSnapshot.md) |  | [optional] 

## Example

```python
from koyeb.api.models.create_instance_snapshot_reply import CreateInstanceSnapshotReply

# TODO update the JSON string below
json = "{}"
# create an instance of CreateInstanceSnapshotReply from a JSON string
create_instance_snapshot_reply_instance = CreateInstanceSnapshotReply.from_json(json)
# print the JSON string representation of the object
print(CreateInstanceSnapshotReply.to_json())

# convert the object into a dict
create_instance_snapshot_reply_dict = create_instance_snapshot_reply_instance.to_dict()
# create an instance of CreateInstanceSnapshotReply from a dict
create_instance_snapshot_reply_from_dict = CreateInstanceSnapshotReply.from_dict(create_instance_snapshot_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


