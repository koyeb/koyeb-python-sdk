# ListInstanceSnapshotEventsReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**events** | [**List[InstanceSnapshotEvent]**](InstanceSnapshotEvent.md) |  | [optional] 
**limit** | **int** |  | [optional] 
**offset** | **int** |  | [optional] 
**order** | **str** |  | [optional] 
**has_next** | **bool** |  | [optional] 

## Example

```python
from koyeb.api.models.list_instance_snapshot_events_reply import ListInstanceSnapshotEventsReply

# TODO update the JSON string below
json = "{}"
# create an instance of ListInstanceSnapshotEventsReply from a JSON string
list_instance_snapshot_events_reply_instance = ListInstanceSnapshotEventsReply.from_json(json)
# print the JSON string representation of the object
print(ListInstanceSnapshotEventsReply.to_json())

# convert the object into a dict
list_instance_snapshot_events_reply_dict = list_instance_snapshot_events_reply_instance.to_dict()
# create an instance of ListInstanceSnapshotEventsReply from a dict
list_instance_snapshot_events_reply_from_dict = ListInstanceSnapshotEventsReply.from_dict(list_instance_snapshot_events_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


