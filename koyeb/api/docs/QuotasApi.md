# koyeb.api.QuotasApi

All URIs are relative to *https://app.koyeb.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_organization_quotas_usage**](QuotasApi.md#get_organization_quotas_usage) | **GET** /v1/quotas/organizations/{organization_id}/usage | Return the organization&#39;s current quota usage alongside the plan&#39;s limits. Response is cached in Redis for 60s. Accept text/plain (or ?format&#x3D;prometheus) to receive the response rendered as Prometheus text exposition format (\&quot;koyeb_quota_&lt;x&gt;\&quot; for usage, \&quot;koyeb_quota_&lt;x&gt;_limit\&quot; for the plan limit) suitable for scraping into an external Prometheus.
[**review_organization_capacity**](QuotasApi.md#review_organization_capacity) | **POST** /v1/quotas/capacity | DEPRECATED: Review Organization Capacity


# **get_organization_quotas_usage**
> GetOrganizationQuotasUsageReply get_organization_quotas_usage(organization_id)

Return the organization's current quota usage alongside the plan's limits. Response is cached in Redis for 60s. Accept text/plain (or ?format=prometheus) to receive the response rendered as Prometheus text exposition format (\"koyeb_quota_<x>\" for usage, \"koyeb_quota_<x>_limit\" for the plan limit) suitable for scraping into an external Prometheus.

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.get_organization_quotas_usage_reply import GetOrganizationQuotasUsageReply
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
    api_instance = koyeb.api.QuotasApi(api_client)
    organization_id = 'organization_id_example' # str | 

    try:
        # Return the organization's current quota usage alongside the plan's limits. Response is cached in Redis for 60s. Accept text/plain (or ?format=prometheus) to receive the response rendered as Prometheus text exposition format (\"koyeb_quota_<x>\" for usage, \"koyeb_quota_<x>_limit\" for the plan limit) suitable for scraping into an external Prometheus.
        api_response = api_instance.get_organization_quotas_usage(organization_id)
        print("The response of QuotasApi->get_organization_quotas_usage:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling QuotasApi->get_organization_quotas_usage: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_id** | **str**|  | 

### Return type

[**GetOrganizationQuotasUsageReply**](GetOrganizationQuotasUsageReply.md)

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

# **review_organization_capacity**
> ReviewOrganizationCapacityReply review_organization_capacity(body)

DEPRECATED: Review Organization Capacity

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.review_organization_capacity_reply import ReviewOrganizationCapacityReply
from koyeb.api.models.review_organization_capacity_request import ReviewOrganizationCapacityRequest
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
    api_instance = koyeb.api.QuotasApi(api_client)
    body = koyeb.api.ReviewOrganizationCapacityRequest() # ReviewOrganizationCapacityRequest | 

    try:
        # DEPRECATED: Review Organization Capacity
        api_response = api_instance.review_organization_capacity(body)
        print("The response of QuotasApi->review_organization_capacity:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling QuotasApi->review_organization_capacity: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ReviewOrganizationCapacityRequest**](ReviewOrganizationCapacityRequest.md)|  | 

### Return type

[**ReviewOrganizationCapacityReply**](ReviewOrganizationCapacityReply.md)

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

