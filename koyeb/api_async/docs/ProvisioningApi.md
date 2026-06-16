# koyeb.api_async.ProvisioningApi

All URIs are relative to *https://app.koyeb.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_stage_attempt**](ProvisioningApi.md#create_stage_attempt) | **POST** /v1/provisioning/{deployment_id}/status/{stage}/{attempt} | Create an attempt for a stage
[**declare_stage_progress**](ProvisioningApi.md#declare_stage_progress) | **PATCH** /v1/provisioning/{deployment_id}/status/{stage}/{attempt} | Declare stage progress
[**declare_step_progress**](ProvisioningApi.md#declare_step_progress) | **PATCH** /v1/provisioning/{deployment_id}/status/{stage}/{attempt}/{step} | Declare step progress


# **create_stage_attempt**
> object create_stage_attempt(deployment_id, stage, attempt, body)

Create an attempt for a stage

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.create_stage_attempt_request import CreateStageAttemptRequest
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
    api_instance = koyeb.api_async.ProvisioningApi(api_client)
    deployment_id = 'deployment_id_example' # str | 
    stage = 'stage_example' # str | 
    attempt = 'attempt_example' # str | 
    body = koyeb.api_async.CreateStageAttemptRequest() # CreateStageAttemptRequest | 

    try:
        # Create an attempt for a stage
        api_response = await api_instance.create_stage_attempt(deployment_id, stage, attempt, body)
        print("The response of ProvisioningApi->create_stage_attempt:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProvisioningApi->create_stage_attempt: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **deployment_id** | **str**|  | 
 **stage** | **str**|  | 
 **attempt** | **str**|  | 
 **body** | [**CreateStageAttemptRequest**](CreateStageAttemptRequest.md)|  | 

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

# **declare_stage_progress**
> object declare_stage_progress(deployment_id, stage, attempt, body)

Declare stage progress

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.declare_stage_progress_request import DeclareStageProgressRequest
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
    api_instance = koyeb.api_async.ProvisioningApi(api_client)
    deployment_id = 'deployment_id_example' # str | 
    stage = 'stage_example' # str | 
    attempt = 'attempt_example' # str | 
    body = koyeb.api_async.DeclareStageProgressRequest() # DeclareStageProgressRequest | 

    try:
        # Declare stage progress
        api_response = await api_instance.declare_stage_progress(deployment_id, stage, attempt, body)
        print("The response of ProvisioningApi->declare_stage_progress:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProvisioningApi->declare_stage_progress: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **deployment_id** | **str**|  | 
 **stage** | **str**|  | 
 **attempt** | **str**|  | 
 **body** | [**DeclareStageProgressRequest**](DeclareStageProgressRequest.md)|  | 

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

# **declare_step_progress**
> object declare_step_progress(deployment_id, stage, attempt, step, body)

Declare step progress

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.declare_step_progress_request import DeclareStepProgressRequest
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
    api_instance = koyeb.api_async.ProvisioningApi(api_client)
    deployment_id = 'deployment_id_example' # str | 
    stage = 'stage_example' # str | 
    attempt = 'attempt_example' # str | 
    step = 'step_example' # str | 
    body = koyeb.api_async.DeclareStepProgressRequest() # DeclareStepProgressRequest | 

    try:
        # Declare step progress
        api_response = await api_instance.declare_step_progress(deployment_id, stage, attempt, step, body)
        print("The response of ProvisioningApi->declare_step_progress:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProvisioningApi->declare_step_progress: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **deployment_id** | **str**|  | 
 **stage** | **str**|  | 
 **attempt** | **str**|  | 
 **step** | **str**|  | 
 **body** | [**DeclareStepProgressRequest**](DeclareStepProgressRequest.md)|  | 

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

