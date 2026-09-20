# ListServicePoolsReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**service_pools** | [**List[ServicePool]**](ServicePool.md) |  | [optional] 
**limit** | **int** |  | [optional] 
**offset** | **int** |  | [optional] 
**count** | **int** |  | [optional] 
**has_next** | **bool** |  | [optional] 

## Example

```python
from koyeb.api.models.list_service_pools_reply import ListServicePoolsReply

# TODO update the JSON string below
json = "{}"
# create an instance of ListServicePoolsReply from a JSON string
list_service_pools_reply_instance = ListServicePoolsReply.from_json(json)
# print the JSON string representation of the object
print(ListServicePoolsReply.to_json())

# convert the object into a dict
list_service_pools_reply_dict = list_service_pools_reply_instance.to_dict()
# create an instance of ListServicePoolsReply from a dict
list_service_pools_reply_from_dict = ListServicePoolsReply.from_dict(list_service_pools_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


