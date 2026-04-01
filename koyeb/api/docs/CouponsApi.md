# koyeb.api.CouponsApi

All URIs are relative to *https://app.koyeb.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**check_coupon**](CouponsApi.md#check_coupon) | **GET** /v1/coupons/{code} | Check Coupon
[**redeem_coupon**](CouponsApi.md#redeem_coupon) | **POST** /v1/coupons | Redeem Coupon


# **check_coupon**
> CheckCouponReply check_coupon(code)

Check Coupon

This API allows to check if a given coupon is valid. It is heavily rate-limited.

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.check_coupon_reply import CheckCouponReply
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
    api_instance = koyeb.api.CouponsApi(api_client)
    code = 'code_example' # str | 

    try:
        # Check Coupon
        api_response = api_instance.check_coupon(code)
        print("The response of CouponsApi->check_coupon:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CouponsApi->check_coupon: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**|  | 

### Return type

[**CheckCouponReply**](CheckCouponReply.md)

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

# **redeem_coupon**
> object redeem_coupon(body)

Redeem Coupon

This API allows to redeem a coupon. Pass the code you received in the body.

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.redeem_coupon_request import RedeemCouponRequest
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
    api_instance = koyeb.api.CouponsApi(api_client)
    body = koyeb.api.RedeemCouponRequest() # RedeemCouponRequest | 

    try:
        # Redeem Coupon
        api_response = api_instance.redeem_coupon(body)
        print("The response of CouponsApi->redeem_coupon:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CouponsApi->redeem_coupon: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RedeemCouponRequest**](RedeemCouponRequest.md)|  | 

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

