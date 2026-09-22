# koyeb.api.ServicePoolsApi

All URIs are relative to *https://app.koyeb.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_service_pool**](ServicePoolsApi.md#create_service_pool) | **POST** /v1/service_pools | Create a ServicePool
[**delete_service_pool**](ServicePoolsApi.md#delete_service_pool) | **DELETE** /v1/service_pools/{id} | Delete a ServicePool
[**get_service_pool**](ServicePoolsApi.md#get_service_pool) | **GET** /v1/service_pools/{id} | Get a ServicePool
[**list_service_pools**](ServicePoolsApi.md#list_service_pools) | **GET** /v1/service_pools | List ServicePools
[**update_service_pool**](ServicePoolsApi.md#update_service_pool) | **PUT** /v1/service_pools/{id} | 


# **create_service_pool**
> CreateServicePoolReply create_service_pool(service_pool)

Create a ServicePool

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.create_service_pool import CreateServicePool
from koyeb.api.models.create_service_pool_reply import CreateServicePoolReply
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
    api_instance = koyeb.api.ServicePoolsApi(api_client)
    service_pool = koyeb.api.CreateServicePool() # CreateServicePool | 

    try:
        # Create a ServicePool
        api_response = api_instance.create_service_pool(service_pool)
        print("The response of ServicePoolsApi->create_service_pool:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServicePoolsApi->create_service_pool: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_pool** | [**CreateServicePool**](CreateServicePool.md)|  | 

### Return type

[**CreateServicePoolReply**](CreateServicePoolReply.md)

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

# **delete_service_pool**
> object delete_service_pool(id)

Delete a ServicePool

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
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
    api_instance = koyeb.api.ServicePoolsApi(api_client)
    id = 'id_example' # str | 

    try:
        # Delete a ServicePool
        api_response = api_instance.delete_service_pool(id)
        print("The response of ServicePoolsApi->delete_service_pool:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServicePoolsApi->delete_service_pool: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

**object**

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

# **get_service_pool**
> GetServicePoolReply get_service_pool(id)

Get a ServicePool

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.get_service_pool_reply import GetServicePoolReply
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
    api_instance = koyeb.api.ServicePoolsApi(api_client)
    id = 'id_example' # str | 

    try:
        # Get a ServicePool
        api_response = api_instance.get_service_pool(id)
        print("The response of ServicePoolsApi->get_service_pool:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServicePoolsApi->get_service_pool: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**GetServicePoolReply**](GetServicePoolReply.md)

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

# **list_service_pools**
> ListServicePoolsReply list_service_pools(name=name, limit=limit, offset=offset)

List ServicePools

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.list_service_pools_reply import ListServicePoolsReply
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
    api_instance = koyeb.api.ServicePoolsApi(api_client)
    name = 'name_example' # str |  (optional)
    limit = 'limit_example' # str |  (optional)
    offset = 'offset_example' # str |  (optional)

    try:
        # List ServicePools
        api_response = api_instance.list_service_pools(name=name, limit=limit, offset=offset)
        print("The response of ServicePoolsApi->list_service_pools:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServicePoolsApi->list_service_pools: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | [optional] 
 **limit** | **str**|  | [optional] 
 **offset** | **str**|  | [optional] 

### Return type

[**ListServicePoolsReply**](ListServicePoolsReply.md)

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

# **update_service_pool**
> UpdateServicePoolReply update_service_pool(id, service_pool, update_mask=update_mask)

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.update_service_pool import UpdateServicePool
from koyeb.api.models.update_service_pool_reply import UpdateServicePoolReply
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
    api_instance = koyeb.api.ServicePoolsApi(api_client)
    id = 'id_example' # str | 
    service_pool = koyeb.api.UpdateServicePool() # UpdateServicePool | 
    update_mask = 'update_mask_example' # str |  (optional)

    try:
        api_response = api_instance.update_service_pool(id, service_pool, update_mask=update_mask)
        print("The response of ServicePoolsApi->update_service_pool:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServicePoolsApi->update_service_pool: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **service_pool** | [**UpdateServicePool**](UpdateServicePool.md)|  | 
 **update_mask** | **str**|  | [optional] 

### Return type

[**UpdateServicePoolReply**](UpdateServicePoolReply.md)

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

