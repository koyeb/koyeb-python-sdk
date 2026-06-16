# ListPersistentVolumeEventsReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**events** | [**List[PersistentVolumeEvent]**](PersistentVolumeEvent.md) |  | [optional] 
**limit** | **int** |  | [optional] 
**offset** | **int** |  | [optional] 
**order** | **str** |  | [optional] 
**has_next** | **bool** |  | [optional] 

## Example

```python
from koyeb.api_async.models.list_persistent_volume_events_reply import ListPersistentVolumeEventsReply

# TODO update the JSON string below
json = "{}"
# create an instance of ListPersistentVolumeEventsReply from a JSON string
list_persistent_volume_events_reply_instance = ListPersistentVolumeEventsReply.from_json(json)
# print the JSON string representation of the object
print(ListPersistentVolumeEventsReply.to_json())

# convert the object into a dict
list_persistent_volume_events_reply_dict = list_persistent_volume_events_reply_instance.to_dict()
# create an instance of ListPersistentVolumeEventsReply from a dict
list_persistent_volume_events_reply_from_dict = ListPersistentVolumeEventsReply.from_dict(list_persistent_volume_events_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


