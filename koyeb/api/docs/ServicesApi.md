# koyeb.api.ServicesApi

All URIs are relative to *https://app.koyeb.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**autocomplete**](ServicesApi.md#autocomplete) | **POST** /v1/services-autocomplete | Autocomplete definition
[**create_service**](ServicesApi.md#create_service) | **POST** /v1/services | Create Service
[**delete_service**](ServicesApi.md#delete_service) | **DELETE** /v1/services/{id} | Delete Service
[**delete_service_scaling**](ServicesApi.md#delete_service_scaling) | **DELETE** /v1/services/{id}/scale | Delete Service Scaling
[**get_service**](ServicesApi.md#get_service) | **GET** /v1/services/{id} | Get Service
[**get_service_scaling**](ServicesApi.md#get_service_scaling) | **GET** /v1/services/{id}/scale | Get Service Scaling
[**list_service_events**](ServicesApi.md#list_service_events) | **GET** /v1/service_events | List Service events
[**list_services**](ServicesApi.md#list_services) | **GET** /v1/services | List Services
[**pause_service**](ServicesApi.md#pause_service) | **POST** /v1/services/{id}/pause | Pause Service
[**re_deploy**](ServicesApi.md#re_deploy) | **POST** /v1/services/{id}/redeploy | ReDeploy Service
[**resume_service**](ServicesApi.md#resume_service) | **POST** /v1/services/{id}/resume | Resume Service
[**update_service**](ServicesApi.md#update_service) | **PUT** /v1/services/{id} | Update Service
[**update_service2**](ServicesApi.md#update_service2) | **PATCH** /v1/services/{id} | Update Service
[**update_service_scaling**](ServicesApi.md#update_service_scaling) | **PUT** /v1/services/{id}/scale | Update Service Scaling


# **autocomplete**
> AutocompleteReply autocomplete(body)

Autocomplete definition

Generate autocomplete definition for a service

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.autocomplete_reply import AutocompleteReply
from koyeb.api.models.autocomplete_request import AutocompleteRequest
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
    api_instance = koyeb.api.ServicesApi(api_client)
    body = koyeb.api.AutocompleteRequest() # AutocompleteRequest | 

    try:
        # Autocomplete definition
        api_response = api_instance.autocomplete(body)
        print("The response of ServicesApi->autocomplete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServicesApi->autocomplete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AutocompleteRequest**](AutocompleteRequest.md)|  | 

### Return type

[**AutocompleteReply**](AutocompleteReply.md)

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

# **create_service**
> CreateServiceReply create_service(service, dry_run=dry_run)

Create Service

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.create_service import CreateService
from koyeb.api.models.create_service_reply import CreateServiceReply
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
    api_instance = koyeb.api.ServicesApi(api_client)
    service = koyeb.api.CreateService() # CreateService | 
    dry_run = True # bool | If set only run validation (optional)

    try:
        # Create Service
        api_response = api_instance.create_service(service, dry_run=dry_run)
        print("The response of ServicesApi->create_service:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServicesApi->create_service: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service** | [**CreateService**](CreateService.md)|  | 
 **dry_run** | **bool**| If set only run validation | [optional] 

### Return type

[**CreateServiceReply**](CreateServiceReply.md)

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

# **delete_service**
> object delete_service(id)

Delete Service

Service deletion is allowed for all status.

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
    api_instance = koyeb.api.ServicesApi(api_client)
    id = 'id_example' # str | The id of the entity to delete

    try:
        # Delete Service
        api_response = api_instance.delete_service(id)
        print("The response of ServicesApi->delete_service:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServicesApi->delete_service: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the entity to delete | 

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

# **delete_service_scaling**
> object delete_service_scaling(id)

Delete Service Scaling

Deletes the manual scaling configuration for a service, reverting to 
the scaling defined in the deployment definition.

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
    api_instance = koyeb.api.ServicesApi(api_client)
    id = 'id_example' # str | The id of the service

    try:
        # Delete Service Scaling
        api_response = api_instance.delete_service_scaling(id)
        print("The response of ServicesApi->delete_service_scaling:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServicesApi->delete_service_scaling: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the service | 

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

# **get_service**
> GetServiceReply get_service(id)

Get Service

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.get_service_reply import GetServiceReply
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
    api_instance = koyeb.api.ServicesApi(api_client)
    id = 'id_example' # str | The id of the Service

    try:
        # Get Service
        api_response = api_instance.get_service(id)
        print("The response of ServicesApi->get_service:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServicesApi->get_service: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the Service | 

### Return type

[**GetServiceReply**](GetServiceReply.md)

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

# **get_service_scaling**
> GetServiceScalingReply get_service_scaling(id)

Get Service Scaling

Returns the current scaling configuration for a service

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.get_service_scaling_reply import GetServiceScalingReply
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
    api_instance = koyeb.api.ServicesApi(api_client)
    id = 'id_example' # str | The id of the service

    try:
        # Get Service Scaling
        api_response = api_instance.get_service_scaling(id)
        print("The response of ServicesApi->get_service_scaling:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServicesApi->get_service_scaling: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the service | 

### Return type

[**GetServiceScalingReply**](GetServiceScalingReply.md)

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

# **list_service_events**
> ListServiceEventsReply list_service_events(service_id=service_id, types=types, limit=limit, offset=offset, order=order)

List Service events

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.list_service_events_reply import ListServiceEventsReply
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
    api_instance = koyeb.api.ServicesApi(api_client)
    service_id = 'service_id_example' # str | (Optional) Filter on service id (optional)
    types = ['types_example'] # List[str] | (Optional) Filter on service event types (optional)
    limit = 'limit_example' # str | (Optional) The number of items to return (optional)
    offset = 'offset_example' # str | (Optional) The offset in the list of item to return (optional)
    order = 'order_example' # str | (Optional) Sorts the list in the ascending or the descending order (optional)

    try:
        # List Service events
        api_response = api_instance.list_service_events(service_id=service_id, types=types, limit=limit, offset=offset, order=order)
        print("The response of ServicesApi->list_service_events:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServicesApi->list_service_events: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_id** | **str**| (Optional) Filter on service id | [optional] 
 **types** | [**List[str]**](str.md)| (Optional) Filter on service event types | [optional] 
 **limit** | **str**| (Optional) The number of items to return | [optional] 
 **offset** | **str**| (Optional) The offset in the list of item to return | [optional] 
 **order** | **str**| (Optional) Sorts the list in the ascending or the descending order | [optional] 

### Return type

[**ListServiceEventsReply**](ListServiceEventsReply.md)

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

# **list_services**
> ListServicesReply list_services(app_id=app_id, limit=limit, offset=offset, name=name, types=types, statuses=statuses, regions=regions, project_id=project_id)

List Services

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.list_services_reply import ListServicesReply
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
    api_instance = koyeb.api.ServicesApi(api_client)
    app_id = 'app_id_example' # str | (Optional) The id of the app (optional)
    limit = 'limit_example' # str | (Optional) The number of items to return (optional)
    offset = 'offset_example' # str | (Optional) The offset in the list of item to return (optional)
    name = 'name_example' # str | (Optional) A filter for name (optional)
    types = ['types_example'] # List[str] | (Optional) Filter on service types (optional)
    statuses = ['statuses_example'] # List[str] | (Optional) Filter on service statuses (optional)
    regions = ['regions_example'] # List[str] | (Optional) Filter on regions (optional)
    project_id = 'project_id_example' # str | (Optional) A filter for the project ID (optional)

    try:
        # List Services
        api_response = api_instance.list_services(app_id=app_id, limit=limit, offset=offset, name=name, types=types, statuses=statuses, regions=regions, project_id=project_id)
        print("The response of ServicesApi->list_services:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServicesApi->list_services: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| (Optional) The id of the app | [optional] 
 **limit** | **str**| (Optional) The number of items to return | [optional] 
 **offset** | **str**| (Optional) The offset in the list of item to return | [optional] 
 **name** | **str**| (Optional) A filter for name | [optional] 
 **types** | [**List[str]**](str.md)| (Optional) Filter on service types | [optional] 
 **statuses** | [**List[str]**](str.md)| (Optional) Filter on service statuses | [optional] 
 **regions** | [**List[str]**](str.md)| (Optional) Filter on regions | [optional] 
 **project_id** | **str**| (Optional) A filter for the project ID | [optional] 

### Return type

[**ListServicesReply**](ListServicesReply.md)

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

# **pause_service**
> object pause_service(id)

Pause Service

Service pause action is allowed for the following status:
 - starting
 - healthy
 - degraded
 - unhealthy
 - resuming

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
    api_instance = koyeb.api.ServicesApi(api_client)
    id = 'id_example' # str | The id of the service to pause.

    try:
        # Pause Service
        api_response = api_instance.pause_service(id)
        print("The response of ServicesApi->pause_service:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServicesApi->pause_service: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the service to pause. | 

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

# **re_deploy**
> RedeployReply re_deploy(id, info)

ReDeploy Service

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.redeploy_reply import RedeployReply
from koyeb.api.models.redeploy_request_info import RedeployRequestInfo
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
    api_instance = koyeb.api.ServicesApi(api_client)
    id = 'id_example' # str | 
    info = koyeb.api.RedeployRequestInfo() # RedeployRequestInfo | 

    try:
        # ReDeploy Service
        api_response = api_instance.re_deploy(id, info)
        print("The response of ServicesApi->re_deploy:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServicesApi->re_deploy: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **info** | [**RedeployRequestInfo**](RedeployRequestInfo.md)|  | 

### Return type

[**RedeployReply**](RedeployReply.md)

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

# **resume_service**
> object resume_service(id, skip_build=skip_build, use_cache=use_cache)

Resume Service

Service resume action is allowed for the following status:
 - paused

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
    api_instance = koyeb.api.ServicesApi(api_client)
    id = 'id_example' # str | The id of the service to pause.
    skip_build = True # bool | If set to true, the build stage will be skipped and the image coming from the last successful build step will be used instead. The call fails if no previous successful builds happened. (optional)
    use_cache = True # bool |  (optional)

    try:
        # Resume Service
        api_response = api_instance.resume_service(id, skip_build=skip_build, use_cache=use_cache)
        print("The response of ServicesApi->resume_service:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServicesApi->resume_service: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the service to pause. | 
 **skip_build** | **bool**| If set to true, the build stage will be skipped and the image coming from the last successful build step will be used instead. The call fails if no previous successful builds happened. | [optional] 
 **use_cache** | **bool**|  | [optional] 

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

# **update_service**
> UpdateServiceReply update_service(id, service, update_mask=update_mask, dry_run=dry_run)

Update Service

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.update_service import UpdateService
from koyeb.api.models.update_service_reply import UpdateServiceReply
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
    api_instance = koyeb.api.ServicesApi(api_client)
    id = 'id_example' # str | The id of the entity to update
    service = koyeb.api.UpdateService() # UpdateService | 
    update_mask = 'update_mask_example' # str |  (optional)
    dry_run = True # bool | If set, run validation and check that the service exists (optional)

    try:
        # Update Service
        api_response = api_instance.update_service(id, service, update_mask=update_mask, dry_run=dry_run)
        print("The response of ServicesApi->update_service:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServicesApi->update_service: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the entity to update | 
 **service** | [**UpdateService**](UpdateService.md)|  | 
 **update_mask** | **str**|  | [optional] 
 **dry_run** | **bool**| If set, run validation and check that the service exists | [optional] 

### Return type

[**UpdateServiceReply**](UpdateServiceReply.md)

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

# **update_service2**
> UpdateServiceReply update_service2(id, service, update_mask=update_mask, dry_run=dry_run)

Update Service

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.update_service import UpdateService
from koyeb.api.models.update_service_reply import UpdateServiceReply
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
    api_instance = koyeb.api.ServicesApi(api_client)
    id = 'id_example' # str | The id of the entity to update
    service = koyeb.api.UpdateService() # UpdateService | 
    update_mask = 'update_mask_example' # str |  (optional)
    dry_run = True # bool | If set, run validation and check that the service exists (optional)

    try:
        # Update Service
        api_response = api_instance.update_service2(id, service, update_mask=update_mask, dry_run=dry_run)
        print("The response of ServicesApi->update_service2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServicesApi->update_service2: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the entity to update | 
 **service** | [**UpdateService**](UpdateService.md)|  | 
 **update_mask** | **str**|  | [optional] 
 **dry_run** | **bool**| If set, run validation and check that the service exists | [optional] 

### Return type

[**UpdateServiceReply**](UpdateServiceReply.md)

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

# **update_service_scaling**
> object update_service_scaling(id, body)

Update Service Scaling

Stores or updates the scaling configuration for a service to use manual scaling

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.update_service_scaling_request import UpdateServiceScalingRequest
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
    api_instance = koyeb.api.ServicesApi(api_client)
    id = 'id_example' # str | The id of the service to scale
    body = koyeb.api.UpdateServiceScalingRequest() # UpdateServiceScalingRequest | 

    try:
        # Update Service Scaling
        api_response = api_instance.update_service_scaling(id, body)
        print("The response of ServicesApi->update_service_scaling:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServicesApi->update_service_scaling: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the service to scale | 
 **body** | [**UpdateServiceScalingRequest**](UpdateServiceScalingRequest.md)|  | 

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

