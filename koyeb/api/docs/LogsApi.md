# koyeb.api.LogsApi

All URIs are relative to *https://app.koyeb.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**query_logs**](LogsApi.md#query_logs) | **GET** /v1/streams/logs/query | Query logs
[**tail_logs**](LogsApi.md#tail_logs) | **GET** /v1/streams/logs/tail | Tails logs


# **query_logs**
> QueryLogsReply query_logs(type=type, app_id=app_id, service_id=service_id, deployment_id=deployment_id, regional_deployment_id=regional_deployment_id, instance_id=instance_id, instance_ids=instance_ids, stream=stream, streams=streams, start=start, end=end, order=order, limit=limit, regex=regex, text=text, regions=regions)

Query logs

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.query_logs_reply import QueryLogsReply
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
    api_instance = koyeb.api.LogsApi(api_client)
    type = 'type_example' # str | Type of logs to retrieve, either \"build\" or \"runtime\". Defaults to \"runtime\". (optional)
    app_id = 'app_id_example' # str | (Optional) Filter on the provided app_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set. (optional)
    service_id = 'service_id_example' # str | (Optional) Filter on the provided service_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set. (optional)
    deployment_id = 'deployment_id_example' # str | (Optional) Filter on the provided deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set. (optional)
    regional_deployment_id = 'regional_deployment_id_example' # str | (Optional) Filter on the provided regional_deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set. (optional)
    instance_id = 'instance_id_example' # str | Deprecated, prefer using instance_ids instead. (optional)
    instance_ids = ['instance_ids_example'] # List[str] | (Optional) Filter on the provided instance_ids. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set. (optional)
    stream = 'stream_example' # str | Deprecated, prefer using streams instead. (optional)
    streams = ['streams_example'] # List[str] | (Optional) Filter on stream: either \"stdout\", \"stderr\" or \"koyeb\" (for system logs). (optional)
    start = '2013-10-20T19:20:30+01:00' # datetime | (Optional) Must always be before `end`. Defaults to 15 minutes ago. (optional)
    end = '2013-10-20T19:20:30+01:00' # datetime | (Optional) Must always be after `start`. Defaults to now. (optional)
    order = 'order_example' # str | (Optional) `asc` or `desc`. Defaults to `desc`. (optional)
    limit = 'limit_example' # str | (Optional) Defaults to 100. Maximum of 1000. (optional)
    regex = 'regex_example' # str | (Optional) Apply a regex to filter logs. Can't be used with `text`. (optional)
    text = 'text_example' # str | (Optional) Looks for this string in logs. Can't be used with `regex`. (optional)
    regions = ['regions_example'] # List[str] | (Optional) Filter on the provided regions (e.g. [\"fra\", \"was\"]). (optional)

    try:
        # Query logs
        api_response = api_instance.query_logs(type=type, app_id=app_id, service_id=service_id, deployment_id=deployment_id, regional_deployment_id=regional_deployment_id, instance_id=instance_id, instance_ids=instance_ids, stream=stream, streams=streams, start=start, end=end, order=order, limit=limit, regex=regex, text=text, regions=regions)
        print("The response of LogsApi->query_logs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LogsApi->query_logs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **type** | **str**| Type of logs to retrieve, either \&quot;build\&quot; or \&quot;runtime\&quot;. Defaults to \&quot;runtime\&quot;. | [optional] 
 **app_id** | **str**| (Optional) Filter on the provided app_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set. | [optional] 
 **service_id** | **str**| (Optional) Filter on the provided service_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set. | [optional] 
 **deployment_id** | **str**| (Optional) Filter on the provided deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set. | [optional] 
 **regional_deployment_id** | **str**| (Optional) Filter on the provided regional_deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set. | [optional] 
 **instance_id** | **str**| Deprecated, prefer using instance_ids instead. | [optional] 
 **instance_ids** | [**List[str]**](str.md)| (Optional) Filter on the provided instance_ids. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set. | [optional] 
 **stream** | **str**| Deprecated, prefer using streams instead. | [optional] 
 **streams** | [**List[str]**](str.md)| (Optional) Filter on stream: either \&quot;stdout\&quot;, \&quot;stderr\&quot; or \&quot;koyeb\&quot; (for system logs). | [optional] 
 **start** | **datetime**| (Optional) Must always be before &#x60;end&#x60;. Defaults to 15 minutes ago. | [optional] 
 **end** | **datetime**| (Optional) Must always be after &#x60;start&#x60;. Defaults to now. | [optional] 
 **order** | **str**| (Optional) &#x60;asc&#x60; or &#x60;desc&#x60;. Defaults to &#x60;desc&#x60;. | [optional] 
 **limit** | **str**| (Optional) Defaults to 100. Maximum of 1000. | [optional] 
 **regex** | **str**| (Optional) Apply a regex to filter logs. Can&#39;t be used with &#x60;text&#x60;. | [optional] 
 **text** | **str**| (Optional) Looks for this string in logs. Can&#39;t be used with &#x60;regex&#x60;. | [optional] 
 **regions** | [**List[str]**](str.md)| (Optional) Filter on the provided regions (e.g. [\&quot;fra\&quot;, \&quot;was\&quot;]). | [optional] 

### Return type

[**QueryLogsReply**](QueryLogsReply.md)

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

# **tail_logs**
> StreamResultOfLogEntry tail_logs(type=type, app_id=app_id, service_id=service_id, deployment_id=deployment_id, regional_deployment_id=regional_deployment_id, instance_id=instance_id, instance_ids=instance_ids, stream=stream, streams=streams, start=start, limit=limit, regex=regex, text=text, regions=regions)

Tails logs

### Example

* Api Key Authentication (Bearer):

```python
import koyeb.api
from koyeb.api.models.stream_result_of_log_entry import StreamResultOfLogEntry
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
    api_instance = koyeb.api.LogsApi(api_client)
    type = 'type_example' # str | Type of logs to retrieve, either \"build\" or \"runtime\". Defaults to \"runtime\". (optional)
    app_id = 'app_id_example' # str | (Optional) Filter on the provided app_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set. (optional)
    service_id = 'service_id_example' # str | (Optional) Filter on the provided service_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set. (optional)
    deployment_id = 'deployment_id_example' # str | (Optional) Filter on the provided deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set. (optional)
    regional_deployment_id = 'regional_deployment_id_example' # str | (Optional) Filter on the provided regional_deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set. (optional)
    instance_id = 'instance_id_example' # str | Deprecated, prefer using instance_ids instead. (optional)
    instance_ids = ['instance_ids_example'] # List[str] | (Optional) Filter on the provided instance_ids. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set. (optional)
    stream = 'stream_example' # str | Deprecated, prefer using streams instead. (optional)
    streams = ['streams_example'] # List[str] | (Optional) Filter on stream: either \"stdout\", \"stderr\" or \"koyeb\" (for system logs). (optional)
    start = '2013-10-20T19:20:30+01:00' # datetime | (Optional) Defaults to 24 hours ago. (optional)
    limit = 'limit_example' # str | (Optional) Defaults to 1000. Maximum of 1000. (optional)
    regex = 'regex_example' # str | (Optional) Apply a regex to filter logs. Can't be used with `text`. (optional)
    text = 'text_example' # str | (Optional) Looks for this string in logs. Can't be used with `regex`. (optional)
    regions = ['regions_example'] # List[str] | (Optional) Filter on the provided regions (e.g. [\"fra\", \"was\"]). (optional)

    try:
        # Tails logs
        api_response = api_instance.tail_logs(type=type, app_id=app_id, service_id=service_id, deployment_id=deployment_id, regional_deployment_id=regional_deployment_id, instance_id=instance_id, instance_ids=instance_ids, stream=stream, streams=streams, start=start, limit=limit, regex=regex, text=text, regions=regions)
        print("The response of LogsApi->tail_logs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LogsApi->tail_logs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **type** | **str**| Type of logs to retrieve, either \&quot;build\&quot; or \&quot;runtime\&quot;. Defaults to \&quot;runtime\&quot;. | [optional] 
 **app_id** | **str**| (Optional) Filter on the provided app_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set. | [optional] 
 **service_id** | **str**| (Optional) Filter on the provided service_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set. | [optional] 
 **deployment_id** | **str**| (Optional) Filter on the provided deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set. | [optional] 
 **regional_deployment_id** | **str**| (Optional) Filter on the provided regional_deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set. | [optional] 
 **instance_id** | **str**| Deprecated, prefer using instance_ids instead. | [optional] 
 **instance_ids** | [**List[str]**](str.md)| (Optional) Filter on the provided instance_ids. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set. | [optional] 
 **stream** | **str**| Deprecated, prefer using streams instead. | [optional] 
 **streams** | [**List[str]**](str.md)| (Optional) Filter on stream: either \&quot;stdout\&quot;, \&quot;stderr\&quot; or \&quot;koyeb\&quot; (for system logs). | [optional] 
 **start** | **datetime**| (Optional) Defaults to 24 hours ago. | [optional] 
 **limit** | **str**| (Optional) Defaults to 1000. Maximum of 1000. | [optional] 
 **regex** | **str**| (Optional) Apply a regex to filter logs. Can&#39;t be used with &#x60;text&#x60;. | [optional] 
 **text** | **str**| (Optional) Looks for this string in logs. Can&#39;t be used with &#x60;regex&#x60;. | [optional] 
 **regions** | [**List[str]**](str.md)| (Optional) Filter on the provided regions (e.g. [\&quot;fra\&quot;, \&quot;was\&quot;]). | [optional] 

### Return type

[**StreamResultOfLogEntry**](StreamResultOfLogEntry.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response.(streaming responses) |  -  |
**400** | Validation error |  -  |
**401** | Returned when the token is not valid. |  -  |
**403** | Returned when the user does not have permission to access the resource. |  -  |
**404** | Returned when the resource does not exist. |  -  |
**500** | Returned in case of server error. |  -  |
**503** | Service is unavailable. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

