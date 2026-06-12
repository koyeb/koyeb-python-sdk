# koyeb.api_async.ProfileApi

All URIs are relative to *https://app.koyeb.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**accept_organization_invitation**](ProfileApi.md#accept_organization_invitation) | **POST** /v1/account/organization_invitations/{id}/accept | Accept Organization Invitation DEPRECATED: this has been replaced by WorkOS and will be dropped soon.
[**clear_idenfy_verification_result**](ProfileApi.md#clear_idenfy_verification_result) | **POST** /v1/account/idenfy | ClearIdenfyVerificationResult marks the current result for idenfy as superseded
[**decline_organization_invitation**](ProfileApi.md#decline_organization_invitation) | **POST** /v1/account/organization_invitations/{id}/decline | Decline Organization Invitation DEPRECATED: this has been replaced by WorkOS and will be dropped soon.
[**get_current_organization**](ProfileApi.md#get_current_organization) | **GET** /v1/account/organization | Get Current Organization
[**get_current_user**](ProfileApi.md#get_current_user) | **GET** /v1/account/profile | Get Current User
[**get_idenfy_token**](ProfileApi.md#get_idenfy_token) | **GET** /v1/account/idenfy | Begin a session with iDenfy, emit an authToken
[**get_o_auth_options**](ProfileApi.md#get_o_auth_options) | **GET** /v1/account/oauth | Get OAuth Providers
[**get_user_organization_invitation**](ProfileApi.md#get_user_organization_invitation) | **GET** /v1/account/organization_invitations/{id} | Get User Organization Invitation DEPRECATED: this has been replaced by WorkOS and will be dropped soon.
[**get_user_settings**](ProfileApi.md#get_user_settings) | **GET** /v1/account/settings | 
[**list_user_organization_invitations**](ProfileApi.md#list_user_organization_invitations) | **GET** /v1/account/organization_invitations | List User Organization Invitations DEPRECATED: this has been replaced by WorkOS and will be dropped soon.
[**list_user_organizations**](ProfileApi.md#list_user_organizations) | **GET** /v1/account/organizations | List User Organizations
[**login_method**](ProfileApi.md#login_method) | **GET** /v1/account/login_method | Get the login method for an email address DEPRECATED: this has been replaced by WorkOS and will be dropped soon.
[**o_auth_callback**](ProfileApi.md#o_auth_callback) | **POST** /v1/account/oauth | Authenticate using OAuth
[**resend_email_validation**](ProfileApi.md#resend_email_validation) | **POST** /v1/account/resend_validation | Resend Email Verification DEPRECATED: this has been replaced by WorkOS and will be dropped soon.
[**reset_password**](ProfileApi.md#reset_password) | **POST** /v1/account/reset_password | Reset Password DEPRECATED: this has been replaced by WorkOS and will be dropped soon.
[**signup**](ProfileApi.md#signup) | **POST** /v1/account/signup | Signup DEPRECATED: this has been replaced by WorkOS and will be dropped soon.
[**update_password**](ProfileApi.md#update_password) | **POST** /v1/account/update_password | Update Password DEPRECATED: this has been replaced by WorkOS and will be dropped soon.
[**update_user**](ProfileApi.md#update_user) | **PUT** /v1/account/profile | Update User
[**update_user2**](ProfileApi.md#update_user2) | **PATCH** /v1/account/profile | Update User
[**update_user_settings**](ProfileApi.md#update_user_settings) | **PATCH** /v1/account/settings | 
[**update_user_v2**](ProfileApi.md#update_user_v2) | **PUT** /v2/account/profile | Update User V2
[**update_user_v22**](ProfileApi.md#update_user_v22) | **PATCH** /v2/account/profile | Update User V2
[**validate**](ProfileApi.md#validate) | **POST** /v1/account/validate/{id} | Validate DEPRECATED: this has been replaced by WorkOS and will be dropped soon.


# **accept_organization_invitation**
> AcceptOrganizationInvitationReply accept_organization_invitation(id, body)

Accept Organization Invitation DEPRECATED: this has been replaced by WorkOS and will be dropped soon.

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.accept_organization_invitation_reply import AcceptOrganizationInvitationReply
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
    api_instance = koyeb.api_async.ProfileApi(api_client)
    id = 'id_example' # str | The id of the organization invitation to accept
    body = None # object | 

    try:
        # Accept Organization Invitation DEPRECATED: this has been replaced by WorkOS and will be dropped soon.
        api_response = await api_instance.accept_organization_invitation(id, body)
        print("The response of ProfileApi->accept_organization_invitation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->accept_organization_invitation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the organization invitation to accept | 
 **body** | **object**|  | 

### Return type

[**AcceptOrganizationInvitationReply**](AcceptOrganizationInvitationReply.md)

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

# **clear_idenfy_verification_result**
> object clear_idenfy_verification_result(body)

ClearIdenfyVerificationResult marks the current result for idenfy as superseded

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.clear_idenfy_verification_result_request import ClearIdenfyVerificationResultRequest
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
    api_instance = koyeb.api_async.ProfileApi(api_client)
    body = koyeb.api_async.ClearIdenfyVerificationResultRequest() # ClearIdenfyVerificationResultRequest | 

    try:
        # ClearIdenfyVerificationResult marks the current result for idenfy as superseded
        api_response = await api_instance.clear_idenfy_verification_result(body)
        print("The response of ProfileApi->clear_idenfy_verification_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->clear_idenfy_verification_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ClearIdenfyVerificationResultRequest**](ClearIdenfyVerificationResultRequest.md)|  | 

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

# **decline_organization_invitation**
> DeclineOrganizationInvitationReply decline_organization_invitation(id, body)

Decline Organization Invitation DEPRECATED: this has been replaced by WorkOS and will be dropped soon.

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.decline_organization_invitation_reply import DeclineOrganizationInvitationReply
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
    api_instance = koyeb.api_async.ProfileApi(api_client)
    id = 'id_example' # str | The id of the organization invitation to decline
    body = None # object | 

    try:
        # Decline Organization Invitation DEPRECATED: this has been replaced by WorkOS and will be dropped soon.
        api_response = await api_instance.decline_organization_invitation(id, body)
        print("The response of ProfileApi->decline_organization_invitation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->decline_organization_invitation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the organization invitation to decline | 
 **body** | **object**|  | 

### Return type

[**DeclineOrganizationInvitationReply**](DeclineOrganizationInvitationReply.md)

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

# **get_current_organization**
> GetOrganizationReply get_current_organization()

Get Current Organization

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.get_organization_reply import GetOrganizationReply
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
    api_instance = koyeb.api_async.ProfileApi(api_client)

    try:
        # Get Current Organization
        api_response = await api_instance.get_current_organization()
        print("The response of ProfileApi->get_current_organization:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->get_current_organization: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

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

# **get_current_user**
> UserReply get_current_user(seon_fp=seon_fp)

Get Current User

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.user_reply import UserReply
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
    api_instance = koyeb.api_async.ProfileApi(api_client)
    seon_fp = 'seon_fp_example' # str | Seon Fingerprint (optional)

    try:
        # Get Current User
        api_response = await api_instance.get_current_user(seon_fp=seon_fp)
        print("The response of ProfileApi->get_current_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->get_current_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **seon_fp** | **str**| Seon Fingerprint | [optional] 

### Return type

[**UserReply**](UserReply.md)

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

# **get_idenfy_token**
> GetIdenfyTokenReply get_idenfy_token()

Begin a session with iDenfy, emit an authToken

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.get_idenfy_token_reply import GetIdenfyTokenReply
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
    api_instance = koyeb.api_async.ProfileApi(api_client)

    try:
        # Begin a session with iDenfy, emit an authToken
        api_response = await api_instance.get_idenfy_token()
        print("The response of ProfileApi->get_idenfy_token:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->get_idenfy_token: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetIdenfyTokenReply**](GetIdenfyTokenReply.md)

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

# **get_o_auth_options**
> GetOAuthOptionsReply get_o_auth_options(action=action, metadata=metadata)

Get OAuth Providers

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.get_o_auth_options_reply import GetOAuthOptionsReply
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
    api_instance = koyeb.api_async.ProfileApi(api_client)
    action = signin # str | Which authentication flow is being initiated (optional) (default to signin)
    metadata = 'metadata_example' # str | A small (limited to 400 characters) string of arbitrary metadata which will be encoded in the state (optional)

    try:
        # Get OAuth Providers
        api_response = await api_instance.get_o_auth_options(action=action, metadata=metadata)
        print("The response of ProfileApi->get_o_auth_options:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->get_o_auth_options: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **action** | **str**| Which authentication flow is being initiated | [optional] [default to signin]
 **metadata** | **str**| A small (limited to 400 characters) string of arbitrary metadata which will be encoded in the state | [optional] 

### Return type

[**GetOAuthOptionsReply**](GetOAuthOptionsReply.md)

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

# **get_user_organization_invitation**
> GetUserOrganizationInvitationReply get_user_organization_invitation(id)

Get User Organization Invitation DEPRECATED: this has been replaced by WorkOS and will be dropped soon.

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.get_user_organization_invitation_reply import GetUserOrganizationInvitationReply
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
    api_instance = koyeb.api_async.ProfileApi(api_client)
    id = 'id_example' # str | The id of the organization invitation to get

    try:
        # Get User Organization Invitation DEPRECATED: this has been replaced by WorkOS and will be dropped soon.
        api_response = await api_instance.get_user_organization_invitation(id)
        print("The response of ProfileApi->get_user_organization_invitation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->get_user_organization_invitation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the organization invitation to get | 

### Return type

[**GetUserOrganizationInvitationReply**](GetUserOrganizationInvitationReply.md)

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

# **get_user_settings**
> GetUserSettingsReply get_user_settings()

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.get_user_settings_reply import GetUserSettingsReply
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
    api_instance = koyeb.api_async.ProfileApi(api_client)

    try:
        api_response = await api_instance.get_user_settings()
        print("The response of ProfileApi->get_user_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->get_user_settings: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetUserSettingsReply**](GetUserSettingsReply.md)

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

# **list_user_organization_invitations**
> ListUserOrganizationInvitationsReply list_user_organization_invitations(limit=limit, offset=offset, statuses=statuses)

List User Organization Invitations DEPRECATED: this has been replaced by WorkOS and will be dropped soon.

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.list_user_organization_invitations_reply import ListUserOrganizationInvitationsReply
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
    api_instance = koyeb.api_async.ProfileApi(api_client)
    limit = 'limit_example' # str | (Optional) The number of items to return (optional)
    offset = 'offset_example' # str | (Optional) The offset in the list of item to return (optional)
    statuses = ['statuses_example'] # List[str] | (Optional) Filter on organization invitation statuses (optional)

    try:
        # List User Organization Invitations DEPRECATED: this has been replaced by WorkOS and will be dropped soon.
        api_response = await api_instance.list_user_organization_invitations(limit=limit, offset=offset, statuses=statuses)
        print("The response of ProfileApi->list_user_organization_invitations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->list_user_organization_invitations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **str**| (Optional) The number of items to return | [optional] 
 **offset** | **str**| (Optional) The offset in the list of item to return | [optional] 
 **statuses** | [**List[str]**](str.md)| (Optional) Filter on organization invitation statuses | [optional] 

### Return type

[**ListUserOrganizationInvitationsReply**](ListUserOrganizationInvitationsReply.md)

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

# **list_user_organizations**
> ListUserOrganizationsReply list_user_organizations(limit=limit, offset=offset, order=order, search=search, statuses=statuses)

List User Organizations

List all organizations that the current user is a member of.

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.list_user_organizations_reply import ListUserOrganizationsReply
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
    api_instance = koyeb.api_async.ProfileApi(api_client)
    limit = 'limit_example' # str | (Optional) Define pagination limit (optional)
    offset = 'offset_example' # str | (Optional) Define pagination offset (optional)
    order = 'order_example' # str | (Optional) Sorts the list in the ascending or the descending order (optional)
    search = 'search_example' # str | (Optional) Fuzzy case-insensitive search based on organization name or organization id (optional)
    statuses = ['statuses_example'] # List[str] | (Optional) Only return organizations which status match one in the list (optional)

    try:
        # List User Organizations
        api_response = await api_instance.list_user_organizations(limit=limit, offset=offset, order=order, search=search, statuses=statuses)
        print("The response of ProfileApi->list_user_organizations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->list_user_organizations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **str**| (Optional) Define pagination limit | [optional] 
 **offset** | **str**| (Optional) Define pagination offset | [optional] 
 **order** | **str**| (Optional) Sorts the list in the ascending or the descending order | [optional] 
 **search** | **str**| (Optional) Fuzzy case-insensitive search based on organization name or organization id | [optional] 
 **statuses** | [**List[str]**](str.md)| (Optional) Only return organizations which status match one in the list | [optional] 

### Return type

[**ListUserOrganizationsReply**](ListUserOrganizationsReply.md)

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

# **login_method**
> LoginMethodReply login_method(email=email)

Get the login method for an email address DEPRECATED: this has been replaced by WorkOS and will be dropped soon.

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.login_method_reply import LoginMethodReply
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
    api_instance = koyeb.api_async.ProfileApi(api_client)
    email = 'email_example' # str |  (optional)

    try:
        # Get the login method for an email address DEPRECATED: this has been replaced by WorkOS and will be dropped soon.
        api_response = await api_instance.login_method(email=email)
        print("The response of ProfileApi->login_method:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->login_method: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **email** | **str**|  | [optional] 

### Return type

[**LoginMethodReply**](LoginMethodReply.md)

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

# **o_auth_callback**
> OAuthCallbackReply o_auth_callback(body, seon_fp=seon_fp)

Authenticate using OAuth

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.o_auth_callback_reply import OAuthCallbackReply
from koyeb.api_async.models.o_auth_callback_request import OAuthCallbackRequest
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
    api_instance = koyeb.api_async.ProfileApi(api_client)
    body = koyeb.api_async.OAuthCallbackRequest() # OAuthCallbackRequest | 
    seon_fp = 'seon_fp_example' # str | Seon Fingerprint (optional)

    try:
        # Authenticate using OAuth
        api_response = await api_instance.o_auth_callback(body, seon_fp=seon_fp)
        print("The response of ProfileApi->o_auth_callback:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->o_auth_callback: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**OAuthCallbackRequest**](OAuthCallbackRequest.md)|  | 
 **seon_fp** | **str**| Seon Fingerprint | [optional] 

### Return type

[**OAuthCallbackReply**](OAuthCallbackReply.md)

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

# **resend_email_validation**
> object resend_email_validation(body)

Resend Email Verification DEPRECATED: this has been replaced by WorkOS and will be dropped soon.

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
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
    api_instance = koyeb.api_async.ProfileApi(api_client)
    body = None # object | 

    try:
        # Resend Email Verification DEPRECATED: this has been replaced by WorkOS and will be dropped soon.
        api_response = await api_instance.resend_email_validation(body)
        print("The response of ProfileApi->resend_email_validation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->resend_email_validation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **object**|  | 

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

# **reset_password**
> object reset_password(body)

Reset Password DEPRECATED: this has been replaced by WorkOS and will be dropped soon.

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.reset_password_request import ResetPasswordRequest
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
    api_instance = koyeb.api_async.ProfileApi(api_client)
    body = koyeb.api_async.ResetPasswordRequest() # ResetPasswordRequest | 

    try:
        # Reset Password DEPRECATED: this has been replaced by WorkOS and will be dropped soon.
        api_response = await api_instance.reset_password(body)
        print("The response of ProfileApi->reset_password:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->reset_password: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ResetPasswordRequest**](ResetPasswordRequest.md)|  | 

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

# **signup**
> LoginReply signup(body, seon_fp=seon_fp)

Signup DEPRECATED: this has been replaced by WorkOS and will be dropped soon.

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.create_account_request import CreateAccountRequest
from koyeb.api_async.models.login_reply import LoginReply
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
    api_instance = koyeb.api_async.ProfileApi(api_client)
    body = koyeb.api_async.CreateAccountRequest() # CreateAccountRequest | Create new account
    seon_fp = 'seon_fp_example' # str | Seon Fingerprint (optional)

    try:
        # Signup DEPRECATED: this has been replaced by WorkOS and will be dropped soon.
        api_response = await api_instance.signup(body, seon_fp=seon_fp)
        print("The response of ProfileApi->signup:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->signup: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateAccountRequest**](CreateAccountRequest.md)| Create new account | 
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

# **update_password**
> LoginReply update_password(body, seon_fp=seon_fp)

Update Password DEPRECATED: this has been replaced by WorkOS and will be dropped soon.

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.login_reply import LoginReply
from koyeb.api_async.models.update_password_request import UpdatePasswordRequest
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
    api_instance = koyeb.api_async.ProfileApi(api_client)
    body = koyeb.api_async.UpdatePasswordRequest() # UpdatePasswordRequest | 
    seon_fp = 'seon_fp_example' # str | Seon Fingerprint (optional)

    try:
        # Update Password DEPRECATED: this has been replaced by WorkOS and will be dropped soon.
        api_response = await api_instance.update_password(body, seon_fp=seon_fp)
        print("The response of ProfileApi->update_password:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->update_password: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdatePasswordRequest**](UpdatePasswordRequest.md)|  | 
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

# **update_user**
> UserReply update_user(user, update_mask=update_mask)

Update User

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.update_user_request_user_update_body import UpdateUserRequestUserUpdateBody
from koyeb.api_async.models.user_reply import UserReply
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
    api_instance = koyeb.api_async.ProfileApi(api_client)
    user = koyeb.api_async.UpdateUserRequestUserUpdateBody() # UpdateUserRequestUserUpdateBody | 
    update_mask = 'update_mask_example' # str |  (optional)

    try:
        # Update User
        api_response = await api_instance.update_user(user, update_mask=update_mask)
        print("The response of ProfileApi->update_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->update_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | [**UpdateUserRequestUserUpdateBody**](UpdateUserRequestUserUpdateBody.md)|  | 
 **update_mask** | **str**|  | [optional] 

### Return type

[**UserReply**](UserReply.md)

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

# **update_user2**
> UserReply update_user2(user, update_mask=update_mask)

Update User

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.update_user_request_user_update_body import UpdateUserRequestUserUpdateBody
from koyeb.api_async.models.user_reply import UserReply
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
    api_instance = koyeb.api_async.ProfileApi(api_client)
    user = koyeb.api_async.UpdateUserRequestUserUpdateBody() # UpdateUserRequestUserUpdateBody | 
    update_mask = 'update_mask_example' # str |  (optional)

    try:
        # Update User
        api_response = await api_instance.update_user2(user, update_mask=update_mask)
        print("The response of ProfileApi->update_user2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->update_user2: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | [**UpdateUserRequestUserUpdateBody**](UpdateUserRequestUserUpdateBody.md)|  | 
 **update_mask** | **str**|  | [optional] 

### Return type

[**UserReply**](UserReply.md)

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

# **update_user_settings**
> UpdateUserSettingsReply update_user_settings(body)

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.update_user_settings_reply import UpdateUserSettingsReply
from koyeb.api_async.models.update_user_settings_request import UpdateUserSettingsRequest
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
    api_instance = koyeb.api_async.ProfileApi(api_client)
    body = koyeb.api_async.UpdateUserSettingsRequest() # UpdateUserSettingsRequest | 

    try:
        api_response = await api_instance.update_user_settings(body)
        print("The response of ProfileApi->update_user_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->update_user_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UpdateUserSettingsRequest**](UpdateUserSettingsRequest.md)|  | 

### Return type

[**UpdateUserSettingsReply**](UpdateUserSettingsReply.md)

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

# **update_user_v2**
> UserReply update_user_v2(user, update_mask=update_mask)

Update User V2

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.update_user_request_user_update_body import UpdateUserRequestUserUpdateBody
from koyeb.api_async.models.user_reply import UserReply
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
    api_instance = koyeb.api_async.ProfileApi(api_client)
    user = koyeb.api_async.UpdateUserRequestUserUpdateBody() # UpdateUserRequestUserUpdateBody | 
    update_mask = 'update_mask_example' # str |  (optional)

    try:
        # Update User V2
        api_response = await api_instance.update_user_v2(user, update_mask=update_mask)
        print("The response of ProfileApi->update_user_v2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->update_user_v2: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | [**UpdateUserRequestUserUpdateBody**](UpdateUserRequestUserUpdateBody.md)|  | 
 **update_mask** | **str**|  | [optional] 

### Return type

[**UserReply**](UserReply.md)

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

# **update_user_v22**
> UserReply update_user_v22(user, update_mask=update_mask)

Update User V2

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.update_user_request_user_update_body import UpdateUserRequestUserUpdateBody
from koyeb.api_async.models.user_reply import UserReply
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
    api_instance = koyeb.api_async.ProfileApi(api_client)
    user = koyeb.api_async.UpdateUserRequestUserUpdateBody() # UpdateUserRequestUserUpdateBody | 
    update_mask = 'update_mask_example' # str |  (optional)

    try:
        # Update User V2
        api_response = await api_instance.update_user_v22(user, update_mask=update_mask)
        print("The response of ProfileApi->update_user_v22:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->update_user_v22: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | [**UpdateUserRequestUserUpdateBody**](UpdateUserRequestUserUpdateBody.md)|  | 
 **update_mask** | **str**|  | [optional] 

### Return type

[**UserReply**](UserReply.md)

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

# **validate**
> LoginReply validate(id, seon_fp=seon_fp)

Validate DEPRECATED: this has been replaced by WorkOS and will be dropped soon.

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.login_reply import LoginReply
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
    api_instance = koyeb.api_async.ProfileApi(api_client)
    id = 'id_example' # str | 
    seon_fp = 'seon_fp_example' # str | Seon Fingerprint (optional)

    try:
        # Validate DEPRECATED: this has been replaced by WorkOS and will be dropped soon.
        api_response = await api_instance.validate(id, seon_fp=seon_fp)
        print("The response of ProfileApi->validate:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->validate: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
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

