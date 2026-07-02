# ListInstanceSnapshotsReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**instance_snapshots** | [**List[InstanceSnapshot]**](InstanceSnapshot.md) |  | [optional] 
**limit** | **int** |  | [optional] 
**offset** | **int** |  | [optional] 
**count** | **int** |  | [optional] 
**has_next** | **bool** |  | [optional] 

## Example

```python
from koyeb.api_async.models.list_instance_snapshots_reply import ListInstanceSnapshotsReply

# TODO update the JSON string below
json = "{}"
# create an instance of ListInstanceSnapshotsReply from a JSON string
list_instance_snapshots_reply_instance = ListInstanceSnapshotsReply.from_json(json)
# print the JSON string representation of the object
print(ListInstanceSnapshotsReply.to_json())

# convert the object into a dict
list_instance_snapshots_reply_dict = list_instance_snapshots_reply_instance.to_dict()
# create an instance of ListInstanceSnapshotsReply from a dict
list_instance_snapshots_reply_from_dict = ListInstanceSnapshotsReply.from_dict(list_instance_snapshots_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


