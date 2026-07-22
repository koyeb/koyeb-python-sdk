# koyeb.api_async.InstanceSnapshotsApi

All URIs are relative to *https://app.koyeb.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_instance_snapshot**](InstanceSnapshotsApi.md#create_instance_snapshot) | **POST** /v1/instance_snapshots | 
[**delete_instance_snapshot**](InstanceSnapshotsApi.md#delete_instance_snapshot) | **DELETE** /v1/instance_snapshots/{id} | 
[**get_instance_snapshot**](InstanceSnapshotsApi.md#get_instance_snapshot) | **GET** /v1/instance_snapshots/{id} | 
[**list_instance_snapshot_events**](InstanceSnapshotsApi.md#list_instance_snapshot_events) | **GET** /v1/instance_snapshot_events | 
[**list_instance_snapshots**](InstanceSnapshotsApi.md#list_instance_snapshots) | **GET** /v1/instance_snapshots | 


# **create_instance_snapshot**
> CreateInstanceSnapshotReply create_instance_snapshot(body)

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.create_instance_snapshot_reply import CreateInstanceSnapshotReply
from koyeb.api_async.models.create_instance_snapshot_request import CreateInstanceSnapshotRequest
from koyeb.api_async.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.koyeb.com
# See configuration.py for a list of all supported configuration parameters.
configuration = koyeb.api_async.Configuration(
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
async with koyeb.api_async.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = koyeb.api_async.InstanceSnapshotsApi(api_client)
    body = koyeb.api_async.CreateInstanceSnapshotRequest() # CreateInstanceSnapshotRequest | 

    try:
        api_response = await api_instance.create_instance_snapshot(body)
        print("The response of InstanceSnapshotsApi->create_instance_snapshot:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling InstanceSnapshotsApi->create_instance_snapshot: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateInstanceSnapshotRequest**](CreateInstanceSnapshotRequest.md)|  | 

### Return type

[**CreateInstanceSnapshotReply**](CreateInstanceSnapshotReply.md)

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

# **delete_instance_snapshot**
> DeleteInstanceSnapshotReply delete_instance_snapshot(id)

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.delete_instance_snapshot_reply import DeleteInstanceSnapshotReply
from koyeb.api_async.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.koyeb.com
# See configuration.py for a list of all supported configuration parameters.
configuration = koyeb.api_async.Configuration(
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
async with koyeb.api_async.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = koyeb.api_async.InstanceSnapshotsApi(api_client)
    id = 'id_example' # str | 

    try:
        api_response = await api_instance.delete_instance_snapshot(id)
        print("The response of InstanceSnapshotsApi->delete_instance_snapshot:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling InstanceSnapshotsApi->delete_instance_snapshot: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**DeleteInstanceSnapshotReply**](DeleteInstanceSnapshotReply.md)

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

# **get_instance_snapshot**
> GetInstanceSnapshotReply get_instance_snapshot(id)

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.get_instance_snapshot_reply import GetInstanceSnapshotReply
from koyeb.api_async.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.koyeb.com
# See configuration.py for a list of all supported configuration parameters.
configuration = koyeb.api_async.Configuration(
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
async with koyeb.api_async.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = koyeb.api_async.InstanceSnapshotsApi(api_client)
    id = 'id_example' # str | 

    try:
        api_response = await api_instance.get_instance_snapshot(id)
        print("The response of InstanceSnapshotsApi->get_instance_snapshot:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling InstanceSnapshotsApi->get_instance_snapshot: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**GetInstanceSnapshotReply**](GetInstanceSnapshotReply.md)

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

# **list_instance_snapshot_events**
> ListInstanceSnapshotEventsReply list_instance_snapshot_events(instance_snapshot_id=instance_snapshot_id, types=types, limit=limit, offset=offset, order=order)

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.list_instance_snapshot_events_reply import ListInstanceSnapshotEventsReply
from koyeb.api_async.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.koyeb.com
# See configuration.py for a list of all supported configuration parameters.
configuration = koyeb.api_async.Configuration(
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
async with koyeb.api_async.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = koyeb.api_async.InstanceSnapshotsApi(api_client)
    instance_snapshot_id = 'instance_snapshot_id_example' # str | (Optional) Filter on instance snapshot id (optional)
    types = ['types_example'] # List[str] | (Optional) Filter on instance snapshot event types (optional)
    limit = 'limit_example' # str | (Optional) The number of items to return (optional)
    offset = 'offset_example' # str | (Optional) The offset in the list of item to return (optional)
    order = 'order_example' # str | (Optional) Sorts the list in the ascending or the descending order (optional)

    try:
        api_response = await api_instance.list_instance_snapshot_events(instance_snapshot_id=instance_snapshot_id, types=types, limit=limit, offset=offset, order=order)
        print("The response of InstanceSnapshotsApi->list_instance_snapshot_events:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling InstanceSnapshotsApi->list_instance_snapshot_events: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instance_snapshot_id** | **str**| (Optional) Filter on instance snapshot id | [optional] 
 **types** | [**List[str]**](str.md)| (Optional) Filter on instance snapshot event types | [optional] 
 **limit** | **str**| (Optional) The number of items to return | [optional] 
 **offset** | **str**| (Optional) The offset in the list of item to return | [optional] 
 **order** | **str**| (Optional) Sorts the list in the ascending or the descending order | [optional] 

### Return type

[**ListInstanceSnapshotEventsReply**](ListInstanceSnapshotEventsReply.md)

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

# **list_instance_snapshots**
> ListInstanceSnapshotsReply list_instance_snapshots(limit=limit, offset=offset, name=name, statuses=statuses, type=type)

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.list_instance_snapshots_reply import ListInstanceSnapshotsReply
from koyeb.api_async.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.koyeb.com
# See configuration.py for a list of all supported configuration parameters.
configuration = koyeb.api_async.Configuration(
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
async with koyeb.api_async.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = koyeb.api_async.InstanceSnapshotsApi(api_client)
    limit = 'limit_example' # str |  (optional)
    offset = 'offset_example' # str |  (optional)
    name = 'name_example' # str |  (optional)
    statuses = ['statuses_example'] # List[str] |  (optional)
    type = INSTANCE_SNAPSHOT_TYPE_INVALID # str |  (optional) (default to INSTANCE_SNAPSHOT_TYPE_INVALID)

    try:
        api_response = await api_instance.list_instance_snapshots(limit=limit, offset=offset, name=name, statuses=statuses, type=type)
        print("The response of InstanceSnapshotsApi->list_instance_snapshots:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling InstanceSnapshotsApi->list_instance_snapshots: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **str**|  | [optional] 
 **offset** | **str**|  | [optional] 
 **name** | **str**|  | [optional] 
 **statuses** | [**List[str]**](str.md)|  | [optional] 
 **type** | **str**|  | [optional] [default to INSTANCE_SNAPSHOT_TYPE_INVALID]

### Return type

[**ListInstanceSnapshotsReply**](ListInstanceSnapshotsReply.md)

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

