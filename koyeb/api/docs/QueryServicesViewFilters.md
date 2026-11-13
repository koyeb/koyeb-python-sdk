# QueryServicesViewFilters


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**types** | [**List[ServiceType]**](ServiceType.md) |  | [optional] 
**statuses** | [**List[ServiceStatus]**](ServiceStatus.md) |  | [optional] 
**regions** | **List[str]** |  | [optional] 
**app_ids** | **List[str]** |  | [optional] 
**active_deployment_states** | [**List[ServiceViewActiveDeploymentState]**](ServiceViewActiveDeploymentState.md) |  | [optional] 
**latest_deployment_states** | [**List[ServiceViewLatestDeploymentState]**](ServiceViewLatestDeploymentState.md) |  | [optional] 
**needs_attention** | **bool** |  | [optional] 

## Example

```python
from koyeb.api.models.query_services_view_filters import QueryServicesViewFilters

# TODO update the JSON string below
json = "{}"
# create an instance of QueryServicesViewFilters from a JSON string
query_services_view_filters_instance = QueryServicesViewFilters.from_json(json)
# print the JSON string representation of the object
print(QueryServicesViewFilters.to_json())

# convert the object into a dict
query_services_view_filters_dict = query_services_view_filters_instance.to_dict()
# create an instance of QueryServicesViewFilters from a dict
query_services_view_filters_from_dict = QueryServicesViewFilters.from_dict(query_services_view_filters_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


