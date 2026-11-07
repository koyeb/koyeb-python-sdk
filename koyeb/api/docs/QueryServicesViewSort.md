# QueryServicesViewSort


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_field** | [**QueryServicesViewSortField**](QueryServicesViewSortField.md) |  | [optional] [default to QueryServicesViewSortField.CREATED_AT]
**direction** | [**QueryServicesViewSortDirection**](QueryServicesViewSortDirection.md) |  | [optional] [default to QueryServicesViewSortDirection.ASC]

## Example

```python
from koyeb.api.models.query_services_view_sort import QueryServicesViewSort

# TODO update the JSON string below
json = "{}"
# create an instance of QueryServicesViewSort from a JSON string
query_services_view_sort_instance = QueryServicesViewSort.from_json(json)
# print the JSON string representation of the object
print(QueryServicesViewSort.to_json())

# convert the object into a dict
query_services_view_sort_dict = query_services_view_sort_instance.to_dict()
# create an instance of QueryServicesViewSort from a dict
query_services_view_sort_from_dict = QueryServicesViewSort.from_dict(query_services_view_sort_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


