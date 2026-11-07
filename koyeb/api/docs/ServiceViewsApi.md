# koyeb.api.ServiceViewsApi

All URIs are relative to *https://app.koyeb.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**query_services_view**](ServiceViewsApi.md#query_services_view) | **GET** /v1/views/services | Query the Services view


# **query_services_view**
> QueryServicesViewReply query_services_view(search=search, filters_types=filters_types, filters_statuses=filters_statuses, filters_regions=filters_regions, filters_app_ids=filters_app_ids, filters_active_deployment_states=filters_active_deployment_states, filters_latest_deployment_states=filters_latest_deployment_states, filters_needs_attention=filters_needs_attention, sort_field=sort_field, sort_direction=sort_direction, group_by=group_by, limit=limit, offset=offset, facets=facets)

Query the Services view

Unstable: this endpoint may change without notice.

Returns Services with their App and Deployment state. Filters, search,
sorting, grouping, counts and facets are all computed on the full
authorized result before pagination.

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.query_services_view_reply import QueryServicesViewReply
from koyeb.api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.koyeb.com
# See configuration.py for a list of all supported configuration parameters.
configuration = koyeb.api.Configuration(
    host = "https://app.koyeb.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: Bearer
configuration.api_key['Bearer'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Bearer'] = 'Bearer'

# Enter a context with an instance of the API client
with koyeb.api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = koyeb.api.ServiceViewsApi(api_client)
    search = 'search_example' # str | (Optional) Case-insensitive search on the Service name and the App name (optional)
    filters_types = ['filters_types_example'] # List[str] | (Optional) Filter on Service types (optional)
    filters_statuses = ['filters_statuses_example'] # List[str] | (Optional) Filter on Service statuses (optional)
    filters_regions = ['filters_regions_example'] # List[str] | (Optional) Filter on regions of the latest Deployment (optional)
    filters_app_ids = ['filters_app_ids_example'] # List[str] | (Optional) Filter on App ids (optional)
    filters_active_deployment_states = ['filters_active_deployment_states_example'] # List[str] | (Optional) Filter on active Deployment states   - SLEEPING: The active Deployment is scaled to zero and wakes up on traffic (optional)
    filters_latest_deployment_states = ['filters_latest_deployment_states_example'] # List[str] | (Optional) Filter on latest Deployment states (optional)
    filters_needs_attention = True # bool | (Optional) Filter on Services that need attention (optional)
    sort_field = 'CREATED_AT' # str |  (optional) (default to 'CREATED_AT')
    sort_direction = 'ASC' # str |  (optional) (default to 'ASC')
    group_by = 'NO_GROUP' # str | (Optional) Group rows by App. Groups are ordered by App name and keep a stable order across pages. Pagination always counts Services (optional) (default to 'NO_GROUP')
    limit = 'limit_example' # str | (Optional) The number of items to return (optional)
    offset = 'offset_example' # str | (Optional) The offset in the list of item to return (optional)
    facets = ['facets_example'] # List[str] | (Optional) Facets to compute on the full result (optional)

    try:
        # Query the Services view
        api_response = api_instance.query_services_view(search=search, filters_types=filters_types, filters_statuses=filters_statuses, filters_regions=filters_regions, filters_app_ids=filters_app_ids, filters_active_deployment_states=filters_active_deployment_states, filters_latest_deployment_states=filters_latest_deployment_states, filters_needs_attention=filters_needs_attention, sort_field=sort_field, sort_direction=sort_direction, group_by=group_by, limit=limit, offset=offset, facets=facets)
        print("The response of ServiceViewsApi->query_services_view:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceViewsApi->query_services_view: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **search** | **str**| (Optional) Case-insensitive search on the Service name and the App name | [optional] 
 **filters_types** | [**List[str]**](str.md)| (Optional) Filter on Service types | [optional] 
 **filters_statuses** | [**List[str]**](str.md)| (Optional) Filter on Service statuses | [optional] 
 **filters_regions** | [**List[str]**](str.md)| (Optional) Filter on regions of the latest Deployment | [optional] 
 **filters_app_ids** | [**List[str]**](str.md)| (Optional) Filter on App ids | [optional] 
 **filters_active_deployment_states** | [**List[str]**](str.md)| (Optional) Filter on active Deployment states   - SLEEPING: The active Deployment is scaled to zero and wakes up on traffic | [optional] 
 **filters_latest_deployment_states** | [**List[str]**](str.md)| (Optional) Filter on latest Deployment states | [optional] 
 **filters_needs_attention** | **bool**| (Optional) Filter on Services that need attention | [optional] 
 **sort_field** | **str**|  | [optional] [default to &#39;CREATED_AT&#39;]
 **sort_direction** | **str**|  | [optional] [default to &#39;ASC&#39;]
 **group_by** | **str**| (Optional) Group rows by App. Groups are ordered by App name and keep a stable order across pages. Pagination always counts Services | [optional] [default to &#39;NO_GROUP&#39;]
 **limit** | **str**| (Optional) The number of items to return | [optional] 
 **offset** | **str**| (Optional) The offset in the list of item to return | [optional] 
 **facets** | [**List[str]**](str.md)| (Optional) Facets to compute on the full result | [optional] 

### Return type

[**QueryServicesViewReply**](QueryServicesViewReply.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**400** | Validation error |  -  |
**401** | Returned when the token is not valid. |  -  |
**403** | Returned when the user does not have permission to access the resource. |  -  |
**404** | Returned when the resource does not exist. |  -  |
**500** | Returned in case of server error. |  -  |
**503** | Service is unavailable. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

