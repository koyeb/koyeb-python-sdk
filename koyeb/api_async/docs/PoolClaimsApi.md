# koyeb.api_async.PoolClaimsApi

All URIs are relative to *https://app.koyeb.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**claim**](PoolClaimsApi.md#claim) | **POST** /v1/claim | Claim a sandbox from a service pool
[**get_claim**](PoolClaimsApi.md#get_claim) | **GET** /v1/claims/{claim_id} | Get a claim
[**list_claim**](PoolClaimsApi.md#list_claim) | **GET** /v1/service_pools/{pool_id}/claims | List claims of a service pool


# **claim**
> PoolClaimReply claim(body)

Claim a sandbox from a service pool

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.pool_claim_reply import PoolClaimReply
from koyeb.api_async.models.pool_claim_request import PoolClaimRequest
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
    api_instance = koyeb.api_async.PoolClaimsApi(api_client)
    body = koyeb.api_async.PoolClaimRequest() # PoolClaimRequest | 

    try:
        # Claim a sandbox from a service pool
        api_response = await api_instance.claim(body)
        print("The response of PoolClaimsApi->claim:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PoolClaimsApi->claim: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PoolClaimRequest**](PoolClaimRequest.md)|  | 

### Return type

[**PoolClaimReply**](PoolClaimReply.md)

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

# **get_claim**
> GetPoolClaimReply get_claim(claim_id, request_id=request_id)

Get a claim

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.get_pool_claim_reply import GetPoolClaimReply
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
    api_instance = koyeb.api_async.PoolClaimsApi(api_client)
    claim_id = 'claim_id_example' # str | 
    request_id = 'request_id_example' # str |  (optional)

    try:
        # Get a claim
        api_response = await api_instance.get_claim(claim_id, request_id=request_id)
        print("The response of PoolClaimsApi->get_claim:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PoolClaimsApi->get_claim: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **claim_id** | **str**|  | 
 **request_id** | **str**|  | [optional] 

### Return type

[**GetPoolClaimReply**](GetPoolClaimReply.md)

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

# **list_claim**
> ListPoolClaimReply list_claim(pool_id, status=status, limit=limit, offset=offset)

List claims of a service pool

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.list_pool_claim_reply import ListPoolClaimReply
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
    api_instance = koyeb.api_async.PoolClaimsApi(api_client)
    pool_id = 'pool_id_example' # str | 
    status = 'status_example' # str |  (optional)
    limit = 'limit_example' # str |  (optional)
    offset = 'offset_example' # str |  (optional)

    try:
        # List claims of a service pool
        api_response = await api_instance.list_claim(pool_id, status=status, limit=limit, offset=offset)
        print("The response of PoolClaimsApi->list_claim:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PoolClaimsApi->list_claim: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pool_id** | **str**|  | 
 **status** | **str**|  | [optional] 
 **limit** | **str**|  | [optional] 
 **offset** | **str**|  | [optional] 

### Return type

[**ListPoolClaimReply**](ListPoolClaimReply.md)

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

