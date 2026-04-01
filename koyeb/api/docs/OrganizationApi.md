# koyeb.api.OrganizationApi

All URIs are relative to *https://app.koyeb.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_access_token**](OrganizationApi.md#create_access_token) | **POST** /v1/organizations/{id}/access_token | CreateAccessToken
[**create_budget**](OrganizationApi.md#create_budget) | **POST** /v1/organizations/{organization_id}/budget | Create Budget
[**create_organization**](OrganizationApi.md#create_organization) | **POST** /v1/organizations | Create Organization
[**deactivate_organization**](OrganizationApi.md#deactivate_organization) | **POST** /v1/organizations/{id}/deactivate | Deactivate an Organization
[**delete_budget**](OrganizationApi.md#delete_budget) | **DELETE** /v1/organizations/{organization_id}/budget | Delete Budget
[**delete_organization**](OrganizationApi.md#delete_organization) | **DELETE** /v1/organizations/{id} | Delete an Organization
[**get_budget**](OrganizationApi.md#get_budget) | **GET** /v1/organizations/{organization_id}/budget | Get Budget
[**get_github_installation**](OrganizationApi.md#get_github_installation) | **GET** /v1/github/installation | Fetch Github Installation configuration
[**get_organization**](OrganizationApi.md#get_organization) | **GET** /v1/organizations/{id} | Get Organization
[**github_installation**](OrganizationApi.md#github_installation) | **POST** /v1/github/installation | Start Github Installation
[**reactivate_organization**](OrganizationApi.md#reactivate_organization) | **POST** /v1/organizations/{id}/reactivate | Reactivate an Organization
[**switch_organization**](OrganizationApi.md#switch_organization) | **POST** /v1/organizations/{id}/switch | Switch Organization context
[**unscope_organization_token**](OrganizationApi.md#unscope_organization_token) | **POST** /v1/unscope_organization_token | Unscope Organization Token
[**update_budget**](OrganizationApi.md#update_budget) | **PUT** /v1/organizations/{organization_id}/budget | Update Budget
[**update_organization**](OrganizationApi.md#update_organization) | **PUT** /v1/organizations/{id} | Update Organization
[**update_organization2**](OrganizationApi.md#update_organization2) | **PATCH** /v1/organizations/{id} | Update Organization
[**update_organization_default_project**](OrganizationApi.md#update_organization_default_project) | **PUT** /v1/organizations/{id}/default_project | Update Organization&#39;s default project
[**update_organization_name**](OrganizationApi.md#update_organization_name) | **PUT** /v1/organizations/{id}/name | Update Organization Name
[**update_organization_plan**](OrganizationApi.md#update_organization_plan) | **POST** /v1/organizations/{id}/plan | Update Organization plan
[**upsert_signup_qualification**](OrganizationApi.md#upsert_signup_qualification) | **POST** /v1/organizations/{id}/signup_qualification | Upsert Organization&#39;s signup qualification


# **create_access_token**
> CreateAccessTokenReply create_access_token(id, body)

CreateAccessToken

CreateAccessToken creates a short-lived access token in the scope of the
specified organization, provided the user making the request is part of
said organization.

It's possible to specify a validity for the token, which defaults to 1h
and must be no more than 24h. The format is `<number>s`, where `<number>`
is a floating point in seconds (so `123.456789012s` means 123 seconds and
456789012 nanoseconds). See:
https://protobuf.dev/reference/php/api-docs/Google/Protobuf/Duration.html.

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.create_access_token_reply import CreateAccessTokenReply
from koyeb.api.models.create_access_token_request import CreateAccessTokenRequest
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
    api_instance = koyeb.api.OrganizationApi(api_client)
    id = 'id_example' # str | Organization id for ephemeral credential
    body = koyeb.api.CreateAccessTokenRequest() # CreateAccessTokenRequest | 

    try:
        # CreateAccessToken
        api_response = api_instance.create_access_token(id, body)
        print("The response of OrganizationApi->create_access_token:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->create_access_token: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Organization id for ephemeral credential | 
 **body** | [**CreateAccessTokenRequest**](CreateAccessTokenRequest.md)|  | 

### Return type

[**CreateAccessTokenReply**](CreateAccessTokenReply.md)

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

# **create_budget**
> CreateBudgetReply create_budget(organization_id, body)

Create Budget

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.create_budget_reply import CreateBudgetReply
from koyeb.api.models.update_budget_request import UpdateBudgetRequest
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
    api_instance = koyeb.api.OrganizationApi(api_client)
    organization_id = 'organization_id_example' # str | 
    body = koyeb.api.UpdateBudgetRequest() # UpdateBudgetRequest | 

    try:
        # Create Budget
        api_response = api_instance.create_budget(organization_id, body)
        print("The response of OrganizationApi->create_budget:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->create_budget: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_id** | **str**|  | 
 **body** | [**UpdateBudgetRequest**](UpdateBudgetRequest.md)|  | 

### Return type

[**CreateBudgetReply**](CreateBudgetReply.md)

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

# **create_organization**
> CreateOrganizationReply create_organization(body)

Create Organization

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.create_organization_reply import CreateOrganizationReply
from koyeb.api.models.create_organization_request import CreateOrganizationRequest
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
    api_instance = koyeb.api.OrganizationApi(api_client)
    body = koyeb.api.CreateOrganizationRequest() # CreateOrganizationRequest | 

    try:
        # Create Organization
        api_response = api_instance.create_organization(body)
        print("The response of OrganizationApi->create_organization:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->create_organization: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateOrganizationRequest**](CreateOrganizationRequest.md)|  | 

### Return type

[**CreateOrganizationReply**](CreateOrganizationReply.md)

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

# **deactivate_organization**
> DeactivateOrganizationReply deactivate_organization(id, body)

Deactivate an Organization

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.deactivate_organization_reply import DeactivateOrganizationReply
from koyeb.api.models.deactivate_organization_request import DeactivateOrganizationRequest
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
    api_instance = koyeb.api.OrganizationApi(api_client)
    id = 'id_example' # str | 
    body = koyeb.api.DeactivateOrganizationRequest() # DeactivateOrganizationRequest | 

    try:
        # Deactivate an Organization
        api_response = api_instance.deactivate_organization(id, body)
        print("The response of OrganizationApi->deactivate_organization:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->deactivate_organization: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **body** | [**DeactivateOrganizationRequest**](DeactivateOrganizationRequest.md)|  | 

### Return type

[**DeactivateOrganizationReply**](DeactivateOrganizationReply.md)

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

# **delete_budget**
> object delete_budget(organization_id)

Delete Budget

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
    api_instance = koyeb.api.OrganizationApi(api_client)
    organization_id = 'organization_id_example' # str | 

    try:
        # Delete Budget
        api_response = api_instance.delete_budget(organization_id)
        print("The response of OrganizationApi->delete_budget:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->delete_budget: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_id** | **str**|  | 

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

# **delete_organization**
> DeleteOrganizationReply delete_organization(id)

Delete an Organization

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.delete_organization_reply import DeleteOrganizationReply
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
    api_instance = koyeb.api.OrganizationApi(api_client)
    id = 'id_example' # str | 

    try:
        # Delete an Organization
        api_response = api_instance.delete_organization(id)
        print("The response of OrganizationApi->delete_organization:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->delete_organization: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**DeleteOrganizationReply**](DeleteOrganizationReply.md)

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

# **get_budget**
> GetBudgetReply get_budget(organization_id)

Get Budget

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.get_budget_reply import GetBudgetReply
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
    api_instance = koyeb.api.OrganizationApi(api_client)
    organization_id = 'organization_id_example' # str | 

    try:
        # Get Budget
        api_response = api_instance.get_budget(organization_id)
        print("The response of OrganizationApi->get_budget:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->get_budget: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_id** | **str**|  | 

### Return type

[**GetBudgetReply**](GetBudgetReply.md)

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

# **get_github_installation**
> GetGithubInstallationReply get_github_installation()

Fetch Github Installation configuration

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.get_github_installation_reply import GetGithubInstallationReply
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
    api_instance = koyeb.api.OrganizationApi(api_client)

    try:
        # Fetch Github Installation configuration
        api_response = api_instance.get_github_installation()
        print("The response of OrganizationApi->get_github_installation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->get_github_installation: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetGithubInstallationReply**](GetGithubInstallationReply.md)

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

# **get_organization**
> GetOrganizationReply get_organization(id)

Get Organization

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.get_organization_reply import GetOrganizationReply
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
    api_instance = koyeb.api.OrganizationApi(api_client)
    id = 'id_example' # str | 

    try:
        # Get Organization
        api_response = api_instance.get_organization(id)
        print("The response of OrganizationApi->get_organization:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->get_organization: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**GetOrganizationReply**](GetOrganizationReply.md)

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

# **github_installation**
> GithubInstallationReply github_installation(body)

Start Github Installation

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.github_installation_reply import GithubInstallationReply
from koyeb.api.models.github_installation_request import GithubInstallationRequest
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
    api_instance = koyeb.api.OrganizationApi(api_client)
    body = koyeb.api.GithubInstallationRequest() # GithubInstallationRequest | 

    try:
        # Start Github Installation
        api_response = api_instance.github_installation(body)
        print("The response of OrganizationApi->github_installation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->github_installation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**GithubInstallationRequest**](GithubInstallationRequest.md)|  | 

### Return type

[**GithubInstallationReply**](GithubInstallationReply.md)

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

# **reactivate_organization**
> ReactivateOrganizationReply reactivate_organization(id, body)

Reactivate an Organization

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.reactivate_organization_reply import ReactivateOrganizationReply
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
    api_instance = koyeb.api.OrganizationApi(api_client)
    id = 'id_example' # str | 
    body = None # object | 

    try:
        # Reactivate an Organization
        api_response = api_instance.reactivate_organization(id, body)
        print("The response of OrganizationApi->reactivate_organization:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->reactivate_organization: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **body** | **object**|  | 

### Return type

[**ReactivateOrganizationReply**](ReactivateOrganizationReply.md)

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

# **switch_organization**
> LoginReply switch_organization(id, body, seon_fp=seon_fp)

Switch Organization context

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.login_reply import LoginReply
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
    api_instance = koyeb.api.OrganizationApi(api_client)
    id = 'id_example' # str | 
    body = None # object | 
    seon_fp = 'seon_fp_example' # str | Seon Fingerprint (optional)

    try:
        # Switch Organization context
        api_response = api_instance.switch_organization(id, body, seon_fp=seon_fp)
        print("The response of OrganizationApi->switch_organization:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->switch_organization: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **body** | **object**|  | 
 **seon_fp** | **str**| Seon Fingerprint | [optional] 

### Return type

[**LoginReply**](LoginReply.md)

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

# **unscope_organization_token**
> LoginReply unscope_organization_token(body, seon_fp=seon_fp)

Unscope Organization Token

UnscopeOrganizationToken removes the organization scope from a token. This
endpoint is useful when a user wants to remove an organization: by
unscoping the token first, the user can then delete the organization
without invalidating his token.

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.login_reply import LoginReply
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
    api_instance = koyeb.api.OrganizationApi(api_client)
    body = None # object | 
    seon_fp = 'seon_fp_example' # str | Seon Fingerprint (optional)

    try:
        # Unscope Organization Token
        api_response = api_instance.unscope_organization_token(body, seon_fp=seon_fp)
        print("The response of OrganizationApi->unscope_organization_token:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->unscope_organization_token: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **object**|  | 
 **seon_fp** | **str**| Seon Fingerprint | [optional] 

### Return type

[**LoginReply**](LoginReply.md)

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

# **update_budget**
> UpdateBudgetReply update_budget(organization_id, body)

Update Budget

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.update_budget_reply import UpdateBudgetReply
from koyeb.api.models.update_budget_request import UpdateBudgetRequest
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
    api_instance = koyeb.api.OrganizationApi(api_client)
    organization_id = 'organization_id_example' # str | 
    body = koyeb.api.UpdateBudgetRequest() # UpdateBudgetRequest | 

    try:
        # Update Budget
        api_response = api_instance.update_budget(organization_id, body)
        print("The response of OrganizationApi->update_budget:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->update_budget: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_id** | **str**|  | 
 **body** | [**UpdateBudgetRequest**](UpdateBudgetRequest.md)|  | 

### Return type

[**UpdateBudgetReply**](UpdateBudgetReply.md)

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

# **update_organization**
> UpdateOrganizationReply update_organization(id, organization, update_mask=update_mask)

Update Organization

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.organization import Organization
from koyeb.api.models.update_organization_reply import UpdateOrganizationReply
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
    api_instance = koyeb.api.OrganizationApi(api_client)
    id = 'id_example' # str | 
    organization = koyeb.api.Organization() # Organization | 
    update_mask = 'update_mask_example' # str |  (optional)

    try:
        # Update Organization
        api_response = api_instance.update_organization(id, organization, update_mask=update_mask)
        print("The response of OrganizationApi->update_organization:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->update_organization: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **organization** | [**Organization**](Organization.md)|  | 
 **update_mask** | **str**|  | [optional] 

### Return type

[**UpdateOrganizationReply**](UpdateOrganizationReply.md)

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

# **update_organization2**
> UpdateOrganizationReply update_organization2(id, organization, update_mask=update_mask)

Update Organization

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.organization import Organization
from koyeb.api.models.update_organization_reply import UpdateOrganizationReply
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
    api_instance = koyeb.api.OrganizationApi(api_client)
    id = 'id_example' # str | 
    organization = koyeb.api.Organization() # Organization | 
    update_mask = 'update_mask_example' # str |  (optional)

    try:
        # Update Organization
        api_response = api_instance.update_organization2(id, organization, update_mask=update_mask)
        print("The response of OrganizationApi->update_organization2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->update_organization2: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **organization** | [**Organization**](Organization.md)|  | 
 **update_mask** | **str**|  | [optional] 

### Return type

[**UpdateOrganizationReply**](UpdateOrganizationReply.md)

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

# **update_organization_default_project**
> UpdateOrganizationDefaultProjectReply update_organization_default_project(id, body)

Update Organization's default project

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.update_organization_default_project_reply import UpdateOrganizationDefaultProjectReply
from koyeb.api.models.update_organization_default_project_request import UpdateOrganizationDefaultProjectRequest
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
    api_instance = koyeb.api.OrganizationApi(api_client)
    id = 'id_example' # str | 
    body = koyeb.api.UpdateOrganizationDefaultProjectRequest() # UpdateOrganizationDefaultProjectRequest | 

    try:
        # Update Organization's default project
        api_response = api_instance.update_organization_default_project(id, body)
        print("The response of OrganizationApi->update_organization_default_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->update_organization_default_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **body** | [**UpdateOrganizationDefaultProjectRequest**](UpdateOrganizationDefaultProjectRequest.md)|  | 

### Return type

[**UpdateOrganizationDefaultProjectReply**](UpdateOrganizationDefaultProjectReply.md)

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

# **update_organization_name**
> UpdateOrganizationNameReply update_organization_name(id, body)

Update Organization Name

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.update_organization_name_reply import UpdateOrganizationNameReply
from koyeb.api.models.update_organization_name_request import UpdateOrganizationNameRequest
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
    api_instance = koyeb.api.OrganizationApi(api_client)
    id = 'id_example' # str | 
    body = koyeb.api.UpdateOrganizationNameRequest() # UpdateOrganizationNameRequest | 

    try:
        # Update Organization Name
        api_response = api_instance.update_organization_name(id, body)
        print("The response of OrganizationApi->update_organization_name:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->update_organization_name: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **body** | [**UpdateOrganizationNameRequest**](UpdateOrganizationNameRequest.md)|  | 

### Return type

[**UpdateOrganizationNameReply**](UpdateOrganizationNameReply.md)

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

# **update_organization_plan**
> UpdateOrganizationPlanReply update_organization_plan(id, body)

Update Organization plan

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.update_organization_plan_reply import UpdateOrganizationPlanReply
from koyeb.api.models.update_organization_plan_request import UpdateOrganizationPlanRequest
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
    api_instance = koyeb.api.OrganizationApi(api_client)
    id = 'id_example' # str | 
    body = koyeb.api.UpdateOrganizationPlanRequest() # UpdateOrganizationPlanRequest | 

    try:
        # Update Organization plan
        api_response = api_instance.update_organization_plan(id, body)
        print("The response of OrganizationApi->update_organization_plan:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->update_organization_plan: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **body** | [**UpdateOrganizationPlanRequest**](UpdateOrganizationPlanRequest.md)|  | 

### Return type

[**UpdateOrganizationPlanReply**](UpdateOrganizationPlanReply.md)

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

# **upsert_signup_qualification**
> UpsertSignupQualificationReply upsert_signup_qualification(id, body)

Upsert Organization's signup qualification

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.upsert_signup_qualification_reply import UpsertSignupQualificationReply
from koyeb.api.models.upsert_signup_qualification_request import UpsertSignupQualificationRequest
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
    api_instance = koyeb.api.OrganizationApi(api_client)
    id = 'id_example' # str | 
    body = koyeb.api.UpsertSignupQualificationRequest() # UpsertSignupQualificationRequest | 

    try:
        # Upsert Organization's signup qualification
        api_response = api_instance.upsert_signup_qualification(id, body)
        print("The response of OrganizationApi->upsert_signup_qualification:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationApi->upsert_signup_qualification: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **body** | [**UpsertSignupQualificationRequest**](UpsertSignupQualificationRequest.md)|  | 

### Return type

[**UpsertSignupQualificationReply**](UpsertSignupQualificationReply.md)

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

