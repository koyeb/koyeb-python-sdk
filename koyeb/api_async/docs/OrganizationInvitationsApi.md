# koyeb.api_async.OrganizationInvitationsApi

All URIs are relative to *https://app.koyeb.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_organization_invitation**](OrganizationInvitationsApi.md#create_organization_invitation) | **POST** /v1/organization_invitations | Create Organization Invitation
[**delete_organization_invitation**](OrganizationInvitationsApi.md#delete_organization_invitation) | **DELETE** /v1/organization_invitations/{id} | Delete Organization Invitation
[**get_organization_invitation**](OrganizationInvitationsApi.md#get_organization_invitation) | **GET** /v1/organization_invitations/{id} | Get Organization Invitation
[**list_organization_invitations**](OrganizationInvitationsApi.md#list_organization_invitations) | **GET** /v1/organization_invitations | List Organization Invitations
[**resend_organization_invitation**](OrganizationInvitationsApi.md#resend_organization_invitation) | **POST** /v1/organization_invitations/{id}/resend | Resend Organization Invitation


# **create_organization_invitation**
> CreateOrganizationInvitationReply create_organization_invitation(body)

Create Organization Invitation

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.create_organization_invitation_reply import CreateOrganizationInvitationReply
from koyeb.api_async.models.create_organization_invitation_request import CreateOrganizationInvitationRequest
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
    api_instance = koyeb.api_async.OrganizationInvitationsApi(api_client)
    body = koyeb.api_async.CreateOrganizationInvitationRequest() # CreateOrganizationInvitationRequest | 

    try:
        # Create Organization Invitation
        api_response = await api_instance.create_organization_invitation(body)
        print("The response of OrganizationInvitationsApi->create_organization_invitation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationInvitationsApi->create_organization_invitation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateOrganizationInvitationRequest**](CreateOrganizationInvitationRequest.md)|  | 

### Return type

[**CreateOrganizationInvitationReply**](CreateOrganizationInvitationReply.md)

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

# **delete_organization_invitation**
> object delete_organization_invitation(id)

Delete Organization Invitation

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
    api_instance = koyeb.api_async.OrganizationInvitationsApi(api_client)
    id = 'id_example' # str | The id of the organization invitation to delete

    try:
        # Delete Organization Invitation
        api_response = await api_instance.delete_organization_invitation(id)
        print("The response of OrganizationInvitationsApi->delete_organization_invitation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationInvitationsApi->delete_organization_invitation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the organization invitation to delete | 

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

# **get_organization_invitation**
> GetOrganizationInvitationReply get_organization_invitation(id)

Get Organization Invitation

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.get_organization_invitation_reply import GetOrganizationInvitationReply
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
    api_instance = koyeb.api_async.OrganizationInvitationsApi(api_client)
    id = 'id_example' # str | The id of the invitation to get

    try:
        # Get Organization Invitation
        api_response = await api_instance.get_organization_invitation(id)
        print("The response of OrganizationInvitationsApi->get_organization_invitation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationInvitationsApi->get_organization_invitation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the invitation to get | 

### Return type

[**GetOrganizationInvitationReply**](GetOrganizationInvitationReply.md)

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

# **list_organization_invitations**
> ListOrganizationInvitationsReply list_organization_invitations(limit=limit, offset=offset, statuses=statuses, user_id=user_id)

List Organization Invitations

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.list_organization_invitations_reply import ListOrganizationInvitationsReply
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
    api_instance = koyeb.api_async.OrganizationInvitationsApi(api_client)
    limit = 'limit_example' # str | (Optional) The number of items to return (optional)
    offset = 'offset_example' # str | (Optional) The offset in the list of item to return (optional)
    statuses = ['statuses_example'] # List[str] | (Optional) Filter on organization invitation statuses (optional)
    user_id = 'user_id_example' # str | (Optional) Filter on invitee ID. Will match both invitations sent to that user_id and invitations sent to the email of that user_id. The only valid value is the requester's user_id (optional)

    try:
        # List Organization Invitations
        api_response = await api_instance.list_organization_invitations(limit=limit, offset=offset, statuses=statuses, user_id=user_id)
        print("The response of OrganizationInvitationsApi->list_organization_invitations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationInvitationsApi->list_organization_invitations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **str**| (Optional) The number of items to return | [optional] 
 **offset** | **str**| (Optional) The offset in the list of item to return | [optional] 
 **statuses** | [**List[str]**](str.md)| (Optional) Filter on organization invitation statuses | [optional] 
 **user_id** | **str**| (Optional) Filter on invitee ID. Will match both invitations sent to that user_id and invitations sent to the email of that user_id. The only valid value is the requester&#39;s user_id | [optional] 

### Return type

[**ListOrganizationInvitationsReply**](ListOrganizationInvitationsReply.md)

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

# **resend_organization_invitation**
> ResendOrganizationInvitationReply resend_organization_invitation(id, body)

Resend Organization Invitation

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api_async
from koyeb.api_async.models.resend_organization_invitation_reply import ResendOrganizationInvitationReply
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
    api_instance = koyeb.api_async.OrganizationInvitationsApi(api_client)
    id = 'id_example' # str | The id of the organization invitation to resend
    body = None # object | 

    try:
        # Resend Organization Invitation
        api_response = await api_instance.resend_organization_invitation(id, body)
        print("The response of OrganizationInvitationsApi->resend_organization_invitation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationInvitationsApi->resend_organization_invitation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the organization invitation to resend | 
 **body** | **object**|  | 

### Return type

[**ResendOrganizationInvitationReply**](ResendOrganizationInvitationReply.md)

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

