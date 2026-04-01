# koyeb.api.SecretsApi

All URIs are relative to *https://app.koyeb.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_secret**](SecretsApi.md#create_secret) | **POST** /v1/secrets | Create Secret
[**delete_secret**](SecretsApi.md#delete_secret) | **DELETE** /v1/secrets/{id} | Delete Secret
[**get_secret**](SecretsApi.md#get_secret) | **GET** /v1/secrets/{id} | Get Secret
[**list_secrets**](SecretsApi.md#list_secrets) | **GET** /v1/secrets | List Secrets
[**reveal_secret**](SecretsApi.md#reveal_secret) | **POST** /v1/secrets/{id}/reveal | Reveal Secret
[**update_secret**](SecretsApi.md#update_secret) | **PUT** /v1/secrets/{id} | Update Secret
[**update_secret2**](SecretsApi.md#update_secret2) | **PATCH** /v1/secrets/{id} | Update Secret


# **create_secret**
> CreateSecretReply create_secret(secret)

Create Secret

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.create_secret import CreateSecret
from koyeb.api.models.create_secret_reply import CreateSecretReply
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
    api_instance = koyeb.api.SecretsApi(api_client)
    secret = koyeb.api.CreateSecret() # CreateSecret | 

    try:
        # Create Secret
        api_response = api_instance.create_secret(secret)
        print("The response of SecretsApi->create_secret:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SecretsApi->create_secret: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **secret** | [**CreateSecret**](CreateSecret.md)|  | 

### Return type

[**CreateSecretReply**](CreateSecretReply.md)

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

# **delete_secret**
> object delete_secret(id)

Delete Secret

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
    api_instance = koyeb.api.SecretsApi(api_client)
    id = 'id_example' # str | 

    try:
        # Delete Secret
        api_response = api_instance.delete_secret(id)
        print("The response of SecretsApi->delete_secret:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SecretsApi->delete_secret: %s\n" % e)
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

# **get_secret**
> GetSecretReply get_secret(id)

Get Secret

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.get_secret_reply import GetSecretReply
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
    api_instance = koyeb.api.SecretsApi(api_client)
    id = 'id_example' # str | 

    try:
        # Get Secret
        api_response = api_instance.get_secret(id)
        print("The response of SecretsApi->get_secret:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SecretsApi->get_secret: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**GetSecretReply**](GetSecretReply.md)

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

# **list_secrets**
> ListSecretsReply list_secrets(name=name, limit=limit, offset=offset, types=types, project_id=project_id)

List Secrets

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.list_secrets_reply import ListSecretsReply
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
    api_instance = koyeb.api.SecretsApi(api_client)
    name = 'name_example' # str |  (optional)
    limit = 'limit_example' # str |  (optional)
    offset = 'offset_example' # str |  (optional)
    types = ['types_example'] # List[str] | Filter by secret types (optional)
    project_id = 'project_id_example' # str | (Optional) A filter for the project ID (optional)

    try:
        # List Secrets
        api_response = api_instance.list_secrets(name=name, limit=limit, offset=offset, types=types, project_id=project_id)
        print("The response of SecretsApi->list_secrets:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SecretsApi->list_secrets: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | [optional] 
 **limit** | **str**|  | [optional] 
 **offset** | **str**|  | [optional] 
 **types** | [**List[str]**](str.md)| Filter by secret types | [optional] 
 **project_id** | **str**| (Optional) A filter for the project ID | [optional] 

### Return type

[**ListSecretsReply**](ListSecretsReply.md)

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

# **reveal_secret**
> RevealSecretReply reveal_secret(id, body)

Reveal Secret

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.reveal_secret_reply import RevealSecretReply
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
    api_instance = koyeb.api.SecretsApi(api_client)
    id = 'id_example' # str | 
    body = None # object | 

    try:
        # Reveal Secret
        api_response = api_instance.reveal_secret(id, body)
        print("The response of SecretsApi->reveal_secret:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SecretsApi->reveal_secret: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **body** | **object**|  | 

### Return type

[**RevealSecretReply**](RevealSecretReply.md)

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

# **update_secret**
> UpdateSecretReply update_secret(id, secret, update_mask=update_mask)

Update Secret

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.secret import Secret
from koyeb.api.models.update_secret_reply import UpdateSecretReply
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
    api_instance = koyeb.api.SecretsApi(api_client)
    id = 'id_example' # str | 
    secret = koyeb.api.Secret() # Secret | 
    update_mask = 'update_mask_example' # str |  (optional)

    try:
        # Update Secret
        api_response = api_instance.update_secret(id, secret, update_mask=update_mask)
        print("The response of SecretsApi->update_secret:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SecretsApi->update_secret: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **secret** | [**Secret**](Secret.md)|  | 
 **update_mask** | **str**|  | [optional] 

### Return type

[**UpdateSecretReply**](UpdateSecretReply.md)

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

# **update_secret2**
> UpdateSecretReply update_secret2(id, secret, update_mask=update_mask)

Update Secret

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.secret import Secret
from koyeb.api.models.update_secret_reply import UpdateSecretReply
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
    api_instance = koyeb.api.SecretsApi(api_client)
    id = 'id_example' # str | 
    secret = koyeb.api.Secret() # Secret | 
    update_mask = 'update_mask_example' # str |  (optional)

    try:
        # Update Secret
        api_response = api_instance.update_secret2(id, secret, update_mask=update_mask)
        print("The response of SecretsApi->update_secret2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SecretsApi->update_secret2: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **secret** | [**Secret**](Secret.md)|  | 
 **update_mask** | **str**|  | [optional] 

### Return type

[**UpdateSecretReply**](UpdateSecretReply.md)

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

