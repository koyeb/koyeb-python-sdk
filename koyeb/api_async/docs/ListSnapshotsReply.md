# ListSnapshotsReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**snapshots** | [**List[Snapshot]**](Snapshot.md) |  | [optional] 
**limit** | **int** |  | [optional] 
**offset** | **int** |  | [optional] 
**has_next** | **bool** |  | [optional] 

## Example

```python
from koyeb.api_async.models.list_snapshots_reply import ListSnapshotsReply

# TODO update the JSON string below
json = "{}"
# create an instance of ListSnapshotsReply from a JSON string
list_snapshots_reply_instance = ListSnapshotsReply.from_json(json)
# print the JSON string representation of the object
print(ListSnapshotsReply.to_json())

# convert the object into a dict
list_snapshots_reply_dict = list_snapshots_reply_instance.to_dict()
# create an instance of ListSnapshotsReply from a dict
list_snapshots_reply_from_dict = ListSnapshotsReply.from_dict(list_snapshots_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


