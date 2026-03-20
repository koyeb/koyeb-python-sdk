# koyeb.api.PersistentVolumesApi

All URIs are relative to *https://app.koyeb.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_persistent_volume**](PersistentVolumesApi.md#create_persistent_volume) | **POST** /v1/volumes | Create a PersistentVolume
[**delete_persistent_volume**](PersistentVolumesApi.md#delete_persistent_volume) | **DELETE** /v1/volumes/{id} | Delete a PersistentVolume
[**get_persistent_volume**](PersistentVolumesApi.md#get_persistent_volume) | **GET** /v1/volumes/{id} | Get a PersistentVolume
[**list_persistent_volume_events**](PersistentVolumesApi.md#list_persistent_volume_events) | **GET** /v1/volume_events | List Persistent Volume events
[**list_persistent_volumes**](PersistentVolumesApi.md#list_persistent_volumes) | **GET** /v1/volumes | List all PersistentVolumes
[**update_persistent_volume**](PersistentVolumesApi.md#update_persistent_volume) | **POST** /v1/volumes/{id} | Update a PersistentVolume


# **create_persistent_volume**
> CreatePersistentVolumeReply create_persistent_volume(body)

Create a PersistentVolume

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.create_persistent_volume_reply import CreatePersistentVolumeReply
from koyeb.api.models.create_persistent_volume_request import CreatePersistentVolumeRequest
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
    api_instance = koyeb.api.PersistentVolumesApi(api_client)
    body = koyeb.api.CreatePersistentVolumeRequest() # CreatePersistentVolumeRequest | 

    try:
        # Create a PersistentVolume
        api_response = api_instance.create_persistent_volume(body)
        print("The response of PersistentVolumesApi->create_persistent_volume:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PersistentVolumesApi->create_persistent_volume: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreatePersistentVolumeRequest**](CreatePersistentVolumeRequest.md)|  | 

### Return type

[**CreatePersistentVolumeReply**](CreatePersistentVolumeReply.md)

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

# **delete_persistent_volume**
> DeletePersistentVolumeReply delete_persistent_volume(id)

Delete a PersistentVolume

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.delete_persistent_volume_reply import DeletePersistentVolumeReply
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
    api_instance = koyeb.api.PersistentVolumesApi(api_client)
    id = 'id_example' # str | 

    try:
        # Delete a PersistentVolume
        api_response = api_instance.delete_persistent_volume(id)
        print("The response of PersistentVolumesApi->delete_persistent_volume:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PersistentVolumesApi->delete_persistent_volume: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**DeletePersistentVolumeReply**](DeletePersistentVolumeReply.md)

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

# **get_persistent_volume**
> GetPersistentVolumeReply get_persistent_volume(id)

Get a PersistentVolume

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.get_persistent_volume_reply import GetPersistentVolumeReply
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
    api_instance = koyeb.api.PersistentVolumesApi(api_client)
    id = 'id_example' # str | 

    try:
        # Get a PersistentVolume
        api_response = api_instance.get_persistent_volume(id)
        print("The response of PersistentVolumesApi->get_persistent_volume:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PersistentVolumesApi->get_persistent_volume: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**GetPersistentVolumeReply**](GetPersistentVolumeReply.md)

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

# **list_persistent_volume_events**
> ListPersistentVolumeEventsReply list_persistent_volume_events(persistent_volume_id=persistent_volume_id, types=types, limit=limit, offset=offset, order=order)

List Persistent Volume events

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.list_persistent_volume_events_reply import ListPersistentVolumeEventsReply
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
    api_instance = koyeb.api.PersistentVolumesApi(api_client)
    persistent_volume_id = 'persistent_volume_id_example' # str | (Optional) Filter on persistent volume id (optional)
    types = ['types_example'] # List[str] | (Optional) Filter on persistent volume event types (optional)
    limit = 'limit_example' # str | (Optional) The number of items to return (optional)
    offset = 'offset_example' # str | (Optional) The offset in the list of item to return (optional)
    order = 'order_example' # str | (Optional) Sorts the list in the ascending or the descending order (optional)

    try:
        # List Persistent Volume events
        api_response = api_instance.list_persistent_volume_events(persistent_volume_id=persistent_volume_id, types=types, limit=limit, offset=offset, order=order)
        print("The response of PersistentVolumesApi->list_persistent_volume_events:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PersistentVolumesApi->list_persistent_volume_events: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **persistent_volume_id** | **str**| (Optional) Filter on persistent volume id | [optional] 
 **types** | [**List[str]**](str.md)| (Optional) Filter on persistent volume event types | [optional] 
 **limit** | **str**| (Optional) The number of items to return | [optional] 
 **offset** | **str**| (Optional) The offset in the list of item to return | [optional] 
 **order** | **str**| (Optional) Sorts the list in the ascending or the descending order | [optional] 

### Return type

[**ListPersistentVolumeEventsReply**](ListPersistentVolumeEventsReply.md)

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

# **list_persistent_volumes**
> ListPersistentVolumesReply list_persistent_volumes(limit=limit, offset=offset, service_id=service_id, region=region, name=name, project_id=project_id)

List all PersistentVolumes

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.list_persistent_volumes_reply import ListPersistentVolumesReply
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
    api_instance = koyeb.api.PersistentVolumesApi(api_client)
    limit = 'limit_example' # str | (Optional) The number of items to return (optional)
    offset = 'offset_example' # str | (Optional) The offset in the list of item to return (optional)
    service_id = 'service_id_example' # str | (Optional) A filter for the service id (optional)
    region = 'region_example' # str | (Optional) A filter for the region (optional)
    name = 'name_example' # str | (Optional) A filter for the name (optional)
    project_id = 'project_id_example' # str | (Optional) A filter for the project ID (optional)

    try:
        # List all PersistentVolumes
        api_response = api_instance.list_persistent_volumes(limit=limit, offset=offset, service_id=service_id, region=region, name=name, project_id=project_id)
        print("The response of PersistentVolumesApi->list_persistent_volumes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PersistentVolumesApi->list_persistent_volumes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **str**| (Optional) The number of items to return | [optional] 
 **offset** | **str**| (Optional) The offset in the list of item to return | [optional] 
 **service_id** | **str**| (Optional) A filter for the service id | [optional] 
 **region** | **str**| (Optional) A filter for the region | [optional] 
 **name** | **str**| (Optional) A filter for the name | [optional] 
 **project_id** | **str**| (Optional) A filter for the project ID | [optional] 

### Return type

[**ListPersistentVolumesReply**](ListPersistentVolumesReply.md)

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

# **update_persistent_volume**
> UpdatePersistentVolumeReply update_persistent_volume(id, body)

Update a PersistentVolume

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.update_persistent_volume_reply import UpdatePersistentVolumeReply
from koyeb.api.models.update_persistent_volume_request import UpdatePersistentVolumeRequest
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
    api_instance = koyeb.api.PersistentVolumesApi(api_client)
    id = 'id_example' # str | 
    body = koyeb.api.UpdatePersistentVolumeRequest() # UpdatePersistentVolumeRequest | 

    try:
        # Update a PersistentVolume
        api_response = api_instance.update_persistent_volume(id, body)
        print("The response of PersistentVolumesApi->update_persistent_volume:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PersistentVolumesApi->update_persistent_volume: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **body** | [**UpdatePersistentVolumeRequest**](UpdatePersistentVolumeRequest.md)|  | 

### Return type

[**UpdatePersistentVolumeReply**](UpdatePersistentVolumeReply.md)

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

