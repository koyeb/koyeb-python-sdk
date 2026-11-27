# QueryServicesViewReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**services** | [**List[ServiceViewRow]**](ServiceViewRow.md) |  | [optional] 
**groups** | [**List[ServiceViewGroup]**](ServiceViewGroup.md) |  | [optional] 
**facets** | [**List[ServiceViewFacet]**](ServiceViewFacet.md) |  | [optional] 
**limit** | **int** |  | [optional] 
**offset** | **int** |  | [optional] 
**count** | **int** |  | [optional] 
**has_next** | **bool** |  | [optional] 

## Example

```python
from koyeb.api_async.models.query_services_view_reply import QueryServicesViewReply

# TODO update the JSON string below
json = "{}"
# create an instance of QueryServicesViewReply from a JSON string
query_services_view_reply_instance = QueryServicesViewReply.from_json(json)
# print the JSON string representation of the object
print(QueryServicesViewReply.to_json())

# convert the object into a dict
query_services_view_reply_dict = query_services_view_reply_instance.to_dict()
# create an instance of QueryServicesViewReply from a dict
query_services_view_reply_from_dict = QueryServicesViewReply.from_dict(query_services_view_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


