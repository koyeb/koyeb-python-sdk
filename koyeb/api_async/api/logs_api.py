"""
    Koyeb Rest API

    Welcome to the Koyeb API documentation.  The Koyeb API allows you to interact with the Koyeb platform in a simple, programmatic way using conventional HTTP requests. The API has predictable resource-oriented URLs, allowing you to request, retrieve and execute actions on resources efficiently.  The API returns JSON-encoded responses and uses standard HTTP response codes, and verbs.  All of the functionality available in the Koyeb Control Panel is also available via the API, allowing you to automate repetitive and complex actions as required.  All production API requests are made to:  - https://app.koyeb.com/<version>  All data is sent and received as JSON.  ## Constructing Requests  Requests are made of three components:  - Base URL: `https://app.koyeb.com` - API Version: `v1` - Resource path: `apps`  To construct a proper request, you need to format the URL as follows:  `https://app.koyeb.com/{version}/{resource}`  Example: `https://app.koyeb.com/v1/apps`  The following code is an example request to retrieve the list of Apps.  ``` $ curl -H 'Authorization: Bearer 1111-1111-1111-1111-1111' https://app.koyeb.com/v1/apps {   \"apps\": [     {       \"id\": \"e267e09d-a2ef-4672-95c7-bf88d787a274\",       \"name\": \"demo\",       \"organization_id\": \"c402bcad-d06d-4fd6-8af2-08b790c0e249\",       \"updated_at\": \"2021-04-26T08:28:59.221274Z\",       \"created_at\": \"2021-04-26T08:28:59.221274Z\",       \"domains\": [         {           \"name\": \"demo-koyeb.koyeb.app\",           \"deployment_group\": \"prod\"         }       ]     },     {       \"id\": \"e38caea5-5acb-4fec-aa65-81749546b470\",       \"name\": \"www\",       \"organization_id\": \"c402bcad-d06d-4fd6-8af2-08b790c0e249\",       \"updated_at\": \"2021-05-04T08:56:40.557792Z\",       \"created_at\": \"2021-05-04T08:56:40.557792Z\",       \"domains\": [         {           \"name\": \"www-koyeb.koyeb.app\",           \"deployment_group\": \"prod\"         }       ]     }   ],   \"limit\": 20,   \"offset\": 0,   \"count\": 2 } ```  # Authentication  The Koyeb API uses API keys to authenticate requests. You can view and manage your API keys in the Koyeb Control Panel.  Your API keys carry many privileges. Take care to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, Slack, client-side code, and so forth.  To make an authenticated request, include a bearer-type Authorization header containing your API key, prefixed with `Bearer `:  ``` Authorization: Bearer <your-api-key> ```  All API requests must be made over HTTPS. Calls made over plain HTTP will fail. API requests without authentication will also fail.  # Errors  We use conventional HTTP response codes to indicate the success or failure of an API request.  In general, codes in the 2xx range indicate success, codes in the 4xx range indicate an error that resulted from the provided information (e.g., a required parameter is missing, resource not found), and codes in the 5xx range indicate an error with our servers.  ## HTTP Status Code Summary  - `200 OK` - Everything worked as expected. - `400 Bad Request` - Often missing a required parameter. - `401 Unauthorized` - No valid API key provided. - `402 Request Failed` - Parameters were valid, but the request failed. - `403 Forbidden` - Insufficient privileges to access the requested resource. - `404 Not Found` - The requested item doesn't exist. - `50x` Server errors - Something went wrong on the API domain's end.  Input and output data must be valid JSON with the appropriate Content-Type header set.  ## Attributes  - code:    - `invalid_argument`: Occur when your request has invalid parameters.   - `unknown_resource`: Occur when the resource doesn't exist.   - `authentication_error`: Arise when there is a problem with authentication.   - `rate_limit_error`: Too many requests hit the API too quickly.   - `authorization_required`: You don't have sufficient right to access the resource.   - `api_error`: API errors use in case of a problem with api domain's servers (extremely uncommon).  - message:    - A human-readable error giving more details about the error  - status:    - The HTTP code returned by the server.  - fields (Optional):    - An array of parameters with a human-readable message giving more details about the error.  ## Errors responses example  Response 400 (application/json)  ``` {   \"status\": 400,   \"code\": \"invalid_argument\",   \"message\": \"Invalid argument\",   \"fields\": [     {       \"field\": \"definition.docker.image\",       \"description\": \"cannot be blank\"     }   ] } ```  Response 401 (application/json)  ``` {   \"status\": 401,   \"code\": \"authentication_error\",   \"message\": \"Request unauthenticated with bearer\" } ```  Response 403 (application/json)  ``` {   \"status\": 403,   \"code\": \"authentication_required\",   \"message\": \"You don't have the requested permission to access to resource.\" } ```   Response 404 (application/json)  ``` {   \"status\": 404,   \"code\": \"unknown_resource\",   \"message\": \"App not found\" } ```  # Pagination  All top-level API resources receive a paginated response. For instance, list Apps, list Services, and others share a standard structure, taking two parameters: limit and offset.  **Paginated request**  Requests against paginated endpoints accept two query string arguments:  * *limit*, a positive integer lower or equal to 100 to select the number of items to display. * *offset*, an integer to indicate the position to start at.  Paginated endpoints usually also accept filters to search and sort results. These filters are documented along with each endpoint documentation. 

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import warnings
from pydantic import validate_call, Field, StrictFloat, StrictStr, StrictInt
from typing import Any, Dict, List, Optional, Tuple, Union
from typing_extensions import Annotated

from datetime import datetime
from pydantic import Field, StrictStr
from typing import List, Optional
from typing_extensions import Annotated
from koyeb.api_async.models.query_logs_reply import QueryLogsReply
from koyeb.api_async.models.stream_result_of_log_entry import StreamResultOfLogEntry

from koyeb.api_async.api_client import ApiClient, RequestSerialized
from koyeb.api_async.api_response import ApiResponse
from koyeb.api_async.rest import RESTResponseType


class LogsApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_call
    async def query_logs(
        self,
        type: Annotated[
            Optional[StrictStr],
            Field(
                description='Type of logs to retrieve, either "build" or "runtime". Defaults to "runtime".'
            ),
        ] = None,
        app_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided app_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        service_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided service_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        deployment_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        regional_deployment_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided regional_deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        instance_id: Annotated[
            Optional[StrictStr],
            Field(description="Deprecated, prefer using instance_ids instead."),
        ] = None,
        instance_ids: Annotated[
            Optional[List[StrictStr]],
            Field(
                description="(Optional) Filter on the provided instance_ids. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        stream: Annotated[
            Optional[StrictStr],
            Field(description="Deprecated, prefer using streams instead."),
        ] = None,
        streams: Annotated[
            Optional[List[StrictStr]],
            Field(
                description='(Optional) Filter on stream: either "stdout", "stderr" or "koyeb" (for system logs).'
            ),
        ] = None,
        start: Annotated[
            Optional[datetime],
            Field(
                description="(Optional) Must always be before `end`. Defaults to 15 minutes ago."
            ),
        ] = None,
        end: Annotated[
            Optional[datetime],
            Field(
                description="(Optional) Must always be after `start`. Defaults to now."
            ),
        ] = None,
        order: Annotated[
            Optional[StrictStr],
            Field(description="(Optional) `asc` or `desc`. Defaults to `desc`."),
        ] = None,
        limit: Annotated[
            Optional[StrictStr],
            Field(description="(Optional) Defaults to 100. Maximum of 1000."),
        ] = None,
        regex: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Apply a regex to filter logs. Can't be used with `text`."
            ),
        ] = None,
        text: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Looks for this string in logs. Can't be used with `regex`."
            ),
        ] = None,
        regions: Annotated[
            Optional[List[StrictStr]],
            Field(
                description='(Optional) Filter on the provided regions (e.g. ["fra", "was"]).'
            ),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> QueryLogsReply:
        """Query logs


        :param type: Type of logs to retrieve, either \"build\" or \"runtime\". Defaults to \"runtime\".
        :type type: str
        :param app_id: (Optional) Filter on the provided app_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type app_id: str
        :param service_id: (Optional) Filter on the provided service_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type service_id: str
        :param deployment_id: (Optional) Filter on the provided deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type deployment_id: str
        :param regional_deployment_id: (Optional) Filter on the provided regional_deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type regional_deployment_id: str
        :param instance_id: Deprecated, prefer using instance_ids instead.
        :type instance_id: str
        :param instance_ids: (Optional) Filter on the provided instance_ids. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type instance_ids: List[str]
        :param stream: Deprecated, prefer using streams instead.
        :type stream: str
        :param streams: (Optional) Filter on stream: either \"stdout\", \"stderr\" or \"koyeb\" (for system logs).
        :type streams: List[str]
        :param start: (Optional) Must always be before `end`. Defaults to 15 minutes ago.
        :type start: datetime
        :param end: (Optional) Must always be after `start`. Defaults to now.
        :type end: datetime
        :param order: (Optional) `asc` or `desc`. Defaults to `desc`.
        :type order: str
        :param limit: (Optional) Defaults to 100. Maximum of 1000.
        :type limit: str
        :param regex: (Optional) Apply a regex to filter logs. Can't be used with `text`.
        :type regex: str
        :param text: (Optional) Looks for this string in logs. Can't be used with `regex`.
        :type text: str
        :param regions: (Optional) Filter on the provided regions (e.g. [\"fra\", \"was\"]).
        :type regions: List[str]
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """  # noqa: E501

        _param = self._query_logs_serialize(
            type=type,
            app_id=app_id,
            service_id=service_id,
            deployment_id=deployment_id,
            regional_deployment_id=regional_deployment_id,
            instance_id=instance_id,
            instance_ids=instance_ids,
            stream=stream,
            streams=streams,
            start=start,
            end=end,
            order=order,
            limit=limit,
            regex=regex,
            text=text,
            regions=regions,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "QueryLogsReply",
            "400": "ErrorWithFields",
            "401": "Error",
            "403": "Error",
            "404": "Error",
            "500": "Error",
            "503": "Error",
            "default": "GoogleRpcStatus",
        }
        response_data = await self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        await response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data

    @validate_call
    async def query_logs_with_http_info(
        self,
        type: Annotated[
            Optional[StrictStr],
            Field(
                description='Type of logs to retrieve, either "build" or "runtime". Defaults to "runtime".'
            ),
        ] = None,
        app_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided app_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        service_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided service_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        deployment_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        regional_deployment_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided regional_deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        instance_id: Annotated[
            Optional[StrictStr],
            Field(description="Deprecated, prefer using instance_ids instead."),
        ] = None,
        instance_ids: Annotated[
            Optional[List[StrictStr]],
            Field(
                description="(Optional) Filter on the provided instance_ids. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        stream: Annotated[
            Optional[StrictStr],
            Field(description="Deprecated, prefer using streams instead."),
        ] = None,
        streams: Annotated[
            Optional[List[StrictStr]],
            Field(
                description='(Optional) Filter on stream: either "stdout", "stderr" or "koyeb" (for system logs).'
            ),
        ] = None,
        start: Annotated[
            Optional[datetime],
            Field(
                description="(Optional) Must always be before `end`. Defaults to 15 minutes ago."
            ),
        ] = None,
        end: Annotated[
            Optional[datetime],
            Field(
                description="(Optional) Must always be after `start`. Defaults to now."
            ),
        ] = None,
        order: Annotated[
            Optional[StrictStr],
            Field(description="(Optional) `asc` or `desc`. Defaults to `desc`."),
        ] = None,
        limit: Annotated[
            Optional[StrictStr],
            Field(description="(Optional) Defaults to 100. Maximum of 1000."),
        ] = None,
        regex: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Apply a regex to filter logs. Can't be used with `text`."
            ),
        ] = None,
        text: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Looks for this string in logs. Can't be used with `regex`."
            ),
        ] = None,
        regions: Annotated[
            Optional[List[StrictStr]],
            Field(
                description='(Optional) Filter on the provided regions (e.g. ["fra", "was"]).'
            ),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[QueryLogsReply]:
        """Query logs


        :param type: Type of logs to retrieve, either \"build\" or \"runtime\". Defaults to \"runtime\".
        :type type: str
        :param app_id: (Optional) Filter on the provided app_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type app_id: str
        :param service_id: (Optional) Filter on the provided service_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type service_id: str
        :param deployment_id: (Optional) Filter on the provided deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type deployment_id: str
        :param regional_deployment_id: (Optional) Filter on the provided regional_deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type regional_deployment_id: str
        :param instance_id: Deprecated, prefer using instance_ids instead.
        :type instance_id: str
        :param instance_ids: (Optional) Filter on the provided instance_ids. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type instance_ids: List[str]
        :param stream: Deprecated, prefer using streams instead.
        :type stream: str
        :param streams: (Optional) Filter on stream: either \"stdout\", \"stderr\" or \"koyeb\" (for system logs).
        :type streams: List[str]
        :param start: (Optional) Must always be before `end`. Defaults to 15 minutes ago.
        :type start: datetime
        :param end: (Optional) Must always be after `start`. Defaults to now.
        :type end: datetime
        :param order: (Optional) `asc` or `desc`. Defaults to `desc`.
        :type order: str
        :param limit: (Optional) Defaults to 100. Maximum of 1000.
        :type limit: str
        :param regex: (Optional) Apply a regex to filter logs. Can't be used with `text`.
        :type regex: str
        :param text: (Optional) Looks for this string in logs. Can't be used with `regex`.
        :type text: str
        :param regions: (Optional) Filter on the provided regions (e.g. [\"fra\", \"was\"]).
        :type regions: List[str]
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """  # noqa: E501

        _param = self._query_logs_serialize(
            type=type,
            app_id=app_id,
            service_id=service_id,
            deployment_id=deployment_id,
            regional_deployment_id=regional_deployment_id,
            instance_id=instance_id,
            instance_ids=instance_ids,
            stream=stream,
            streams=streams,
            start=start,
            end=end,
            order=order,
            limit=limit,
            regex=regex,
            text=text,
            regions=regions,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "QueryLogsReply",
            "400": "ErrorWithFields",
            "401": "Error",
            "403": "Error",
            "404": "Error",
            "500": "Error",
            "503": "Error",
            "default": "GoogleRpcStatus",
        }
        response_data = await self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        await response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )

    @validate_call
    async def query_logs_without_preload_content(
        self,
        type: Annotated[
            Optional[StrictStr],
            Field(
                description='Type of logs to retrieve, either "build" or "runtime". Defaults to "runtime".'
            ),
        ] = None,
        app_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided app_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        service_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided service_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        deployment_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        regional_deployment_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided regional_deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        instance_id: Annotated[
            Optional[StrictStr],
            Field(description="Deprecated, prefer using instance_ids instead."),
        ] = None,
        instance_ids: Annotated[
            Optional[List[StrictStr]],
            Field(
                description="(Optional) Filter on the provided instance_ids. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        stream: Annotated[
            Optional[StrictStr],
            Field(description="Deprecated, prefer using streams instead."),
        ] = None,
        streams: Annotated[
            Optional[List[StrictStr]],
            Field(
                description='(Optional) Filter on stream: either "stdout", "stderr" or "koyeb" (for system logs).'
            ),
        ] = None,
        start: Annotated[
            Optional[datetime],
            Field(
                description="(Optional) Must always be before `end`. Defaults to 15 minutes ago."
            ),
        ] = None,
        end: Annotated[
            Optional[datetime],
            Field(
                description="(Optional) Must always be after `start`. Defaults to now."
            ),
        ] = None,
        order: Annotated[
            Optional[StrictStr],
            Field(description="(Optional) `asc` or `desc`. Defaults to `desc`."),
        ] = None,
        limit: Annotated[
            Optional[StrictStr],
            Field(description="(Optional) Defaults to 100. Maximum of 1000."),
        ] = None,
        regex: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Apply a regex to filter logs. Can't be used with `text`."
            ),
        ] = None,
        text: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Looks for this string in logs. Can't be used with `regex`."
            ),
        ] = None,
        regions: Annotated[
            Optional[List[StrictStr]],
            Field(
                description='(Optional) Filter on the provided regions (e.g. ["fra", "was"]).'
            ),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """Query logs


        :param type: Type of logs to retrieve, either \"build\" or \"runtime\". Defaults to \"runtime\".
        :type type: str
        :param app_id: (Optional) Filter on the provided app_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type app_id: str
        :param service_id: (Optional) Filter on the provided service_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type service_id: str
        :param deployment_id: (Optional) Filter on the provided deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type deployment_id: str
        :param regional_deployment_id: (Optional) Filter on the provided regional_deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type regional_deployment_id: str
        :param instance_id: Deprecated, prefer using instance_ids instead.
        :type instance_id: str
        :param instance_ids: (Optional) Filter on the provided instance_ids. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type instance_ids: List[str]
        :param stream: Deprecated, prefer using streams instead.
        :type stream: str
        :param streams: (Optional) Filter on stream: either \"stdout\", \"stderr\" or \"koyeb\" (for system logs).
        :type streams: List[str]
        :param start: (Optional) Must always be before `end`. Defaults to 15 minutes ago.
        :type start: datetime
        :param end: (Optional) Must always be after `start`. Defaults to now.
        :type end: datetime
        :param order: (Optional) `asc` or `desc`. Defaults to `desc`.
        :type order: str
        :param limit: (Optional) Defaults to 100. Maximum of 1000.
        :type limit: str
        :param regex: (Optional) Apply a regex to filter logs. Can't be used with `text`.
        :type regex: str
        :param text: (Optional) Looks for this string in logs. Can't be used with `regex`.
        :type text: str
        :param regions: (Optional) Filter on the provided regions (e.g. [\"fra\", \"was\"]).
        :type regions: List[str]
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """  # noqa: E501

        _param = self._query_logs_serialize(
            type=type,
            app_id=app_id,
            service_id=service_id,
            deployment_id=deployment_id,
            regional_deployment_id=regional_deployment_id,
            instance_id=instance_id,
            instance_ids=instance_ids,
            stream=stream,
            streams=streams,
            start=start,
            end=end,
            order=order,
            limit=limit,
            regex=regex,
            text=text,
            regions=regions,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "QueryLogsReply",
            "400": "ErrorWithFields",
            "401": "Error",
            "403": "Error",
            "404": "Error",
            "500": "Error",
            "503": "Error",
            "default": "GoogleRpcStatus",
        }
        response_data = await self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        return response_data.response

    def _query_logs_serialize(
        self,
        type,
        app_id,
        service_id,
        deployment_id,
        regional_deployment_id,
        instance_id,
        instance_ids,
        stream,
        streams,
        start,
        end,
        order,
        limit,
        regex,
        text,
        regions,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:
        _host = None

        _collection_formats: Dict[str, str] = {
            "instance_ids": "multi",
            "streams": "multi",
            "regions": "multi",
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Any] = self.api_client._merge_headers(_headers)
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[
            str, Union[str, bytes, List[str], List[bytes], List[Tuple[str, bytes]]]
        ] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        # process the query parameters
        if type is not None:
            _query_params.append(("type", type))

        if app_id is not None:
            _query_params.append(("app_id", app_id))

        if service_id is not None:
            _query_params.append(("service_id", service_id))

        if deployment_id is not None:
            _query_params.append(("deployment_id", deployment_id))

        if regional_deployment_id is not None:
            _query_params.append(("regional_deployment_id", regional_deployment_id))

        if instance_id is not None:
            _query_params.append(("instance_id", instance_id))

        if instance_ids is not None:
            _query_params.append(("instance_ids", instance_ids))

        if stream is not None:
            _query_params.append(("stream", stream))

        if streams is not None:
            _query_params.append(("streams", streams))

        if start is not None:
            if isinstance(start, datetime):
                _query_params.append(
                    (
                        "start",
                        start.strftime(self.api_client.configuration.datetime_format),
                    )
                )
            else:
                _query_params.append(("start", start))

        if end is not None:
            if isinstance(end, datetime):
                _query_params.append(
                    ("end", end.strftime(self.api_client.configuration.datetime_format))
                )
            else:
                _query_params.append(("end", end))

        if order is not None:
            _query_params.append(("order", order))

        if limit is not None:
            _query_params.append(("limit", limit))

        if regex is not None:
            _query_params.append(("regex", regex))

        if text is not None:
            _query_params.append(("text", text))

        if regions is not None:
            _query_params.append(("regions", regions))

        # process the header parameters
        # process the form parameters
        # process the body parameter

        # set the HTTP header `Accept`
        if not any(key.lower() == "accept" for key in _header_params):
            _header_params["Accept"] = self.api_client.select_header_accept(["*/*"])

        # authentication setting
        _auth_settings: List[str] = ["Bearer"]

        return self.api_client.param_serialize(
            method="GET",
            resource_path="/v1/streams/logs/query",
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth,
        )

    @validate_call
    async def tail_logs(
        self,
        type: Annotated[
            Optional[StrictStr],
            Field(
                description='Type of logs to retrieve, either "build" or "runtime". Defaults to "runtime".'
            ),
        ] = None,
        app_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided app_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        service_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided service_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        deployment_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        regional_deployment_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided regional_deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        instance_id: Annotated[
            Optional[StrictStr],
            Field(description="Deprecated, prefer using instance_ids instead."),
        ] = None,
        instance_ids: Annotated[
            Optional[List[StrictStr]],
            Field(
                description="(Optional) Filter on the provided instance_ids. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        stream: Annotated[
            Optional[StrictStr],
            Field(description="Deprecated, prefer using streams instead."),
        ] = None,
        streams: Annotated[
            Optional[List[StrictStr]],
            Field(
                description='(Optional) Filter on stream: either "stdout", "stderr" or "koyeb" (for system logs).'
            ),
        ] = None,
        start: Annotated[
            Optional[datetime],
            Field(description="(Optional) Defaults to 24 hours ago."),
        ] = None,
        limit: Annotated[
            Optional[StrictStr],
            Field(description="(Optional) Defaults to 1000. Maximum of 1000."),
        ] = None,
        regex: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Apply a regex to filter logs. Can't be used with `text`."
            ),
        ] = None,
        text: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Looks for this string in logs. Can't be used with `regex`."
            ),
        ] = None,
        regions: Annotated[
            Optional[List[StrictStr]],
            Field(
                description='(Optional) Filter on the provided regions (e.g. ["fra", "was"]).'
            ),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> StreamResultOfLogEntry:
        """Tails logs


        :param type: Type of logs to retrieve, either \"build\" or \"runtime\". Defaults to \"runtime\".
        :type type: str
        :param app_id: (Optional) Filter on the provided app_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type app_id: str
        :param service_id: (Optional) Filter on the provided service_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type service_id: str
        :param deployment_id: (Optional) Filter on the provided deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type deployment_id: str
        :param regional_deployment_id: (Optional) Filter on the provided regional_deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type regional_deployment_id: str
        :param instance_id: Deprecated, prefer using instance_ids instead.
        :type instance_id: str
        :param instance_ids: (Optional) Filter on the provided instance_ids. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type instance_ids: List[str]
        :param stream: Deprecated, prefer using streams instead.
        :type stream: str
        :param streams: (Optional) Filter on stream: either \"stdout\", \"stderr\" or \"koyeb\" (for system logs).
        :type streams: List[str]
        :param start: (Optional) Defaults to 24 hours ago.
        :type start: datetime
        :param limit: (Optional) Defaults to 1000. Maximum of 1000.
        :type limit: str
        :param regex: (Optional) Apply a regex to filter logs. Can't be used with `text`.
        :type regex: str
        :param text: (Optional) Looks for this string in logs. Can't be used with `regex`.
        :type text: str
        :param regions: (Optional) Filter on the provided regions (e.g. [\"fra\", \"was\"]).
        :type regions: List[str]
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """  # noqa: E501

        _param = self._tail_logs_serialize(
            type=type,
            app_id=app_id,
            service_id=service_id,
            deployment_id=deployment_id,
            regional_deployment_id=regional_deployment_id,
            instance_id=instance_id,
            instance_ids=instance_ids,
            stream=stream,
            streams=streams,
            start=start,
            limit=limit,
            regex=regex,
            text=text,
            regions=regions,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "StreamResultOfLogEntry",
            "400": "ErrorWithFields",
            "401": "Error",
            "403": "Error",
            "404": "Error",
            "500": "Error",
            "503": "Error",
            "default": "GoogleRpcStatus",
        }
        response_data = await self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        await response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data

    @validate_call
    async def tail_logs_with_http_info(
        self,
        type: Annotated[
            Optional[StrictStr],
            Field(
                description='Type of logs to retrieve, either "build" or "runtime". Defaults to "runtime".'
            ),
        ] = None,
        app_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided app_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        service_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided service_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        deployment_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        regional_deployment_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided regional_deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        instance_id: Annotated[
            Optional[StrictStr],
            Field(description="Deprecated, prefer using instance_ids instead."),
        ] = None,
        instance_ids: Annotated[
            Optional[List[StrictStr]],
            Field(
                description="(Optional) Filter on the provided instance_ids. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        stream: Annotated[
            Optional[StrictStr],
            Field(description="Deprecated, prefer using streams instead."),
        ] = None,
        streams: Annotated[
            Optional[List[StrictStr]],
            Field(
                description='(Optional) Filter on stream: either "stdout", "stderr" or "koyeb" (for system logs).'
            ),
        ] = None,
        start: Annotated[
            Optional[datetime],
            Field(description="(Optional) Defaults to 24 hours ago."),
        ] = None,
        limit: Annotated[
            Optional[StrictStr],
            Field(description="(Optional) Defaults to 1000. Maximum of 1000."),
        ] = None,
        regex: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Apply a regex to filter logs. Can't be used with `text`."
            ),
        ] = None,
        text: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Looks for this string in logs. Can't be used with `regex`."
            ),
        ] = None,
        regions: Annotated[
            Optional[List[StrictStr]],
            Field(
                description='(Optional) Filter on the provided regions (e.g. ["fra", "was"]).'
            ),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[StreamResultOfLogEntry]:
        """Tails logs


        :param type: Type of logs to retrieve, either \"build\" or \"runtime\". Defaults to \"runtime\".
        :type type: str
        :param app_id: (Optional) Filter on the provided app_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type app_id: str
        :param service_id: (Optional) Filter on the provided service_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type service_id: str
        :param deployment_id: (Optional) Filter on the provided deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type deployment_id: str
        :param regional_deployment_id: (Optional) Filter on the provided regional_deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type regional_deployment_id: str
        :param instance_id: Deprecated, prefer using instance_ids instead.
        :type instance_id: str
        :param instance_ids: (Optional) Filter on the provided instance_ids. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type instance_ids: List[str]
        :param stream: Deprecated, prefer using streams instead.
        :type stream: str
        :param streams: (Optional) Filter on stream: either \"stdout\", \"stderr\" or \"koyeb\" (for system logs).
        :type streams: List[str]
        :param start: (Optional) Defaults to 24 hours ago.
        :type start: datetime
        :param limit: (Optional) Defaults to 1000. Maximum of 1000.
        :type limit: str
        :param regex: (Optional) Apply a regex to filter logs. Can't be used with `text`.
        :type regex: str
        :param text: (Optional) Looks for this string in logs. Can't be used with `regex`.
        :type text: str
        :param regions: (Optional) Filter on the provided regions (e.g. [\"fra\", \"was\"]).
        :type regions: List[str]
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """  # noqa: E501

        _param = self._tail_logs_serialize(
            type=type,
            app_id=app_id,
            service_id=service_id,
            deployment_id=deployment_id,
            regional_deployment_id=regional_deployment_id,
            instance_id=instance_id,
            instance_ids=instance_ids,
            stream=stream,
            streams=streams,
            start=start,
            limit=limit,
            regex=regex,
            text=text,
            regions=regions,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "StreamResultOfLogEntry",
            "400": "ErrorWithFields",
            "401": "Error",
            "403": "Error",
            "404": "Error",
            "500": "Error",
            "503": "Error",
            "default": "GoogleRpcStatus",
        }
        response_data = await self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        await response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )

    @validate_call
    async def tail_logs_without_preload_content(
        self,
        type: Annotated[
            Optional[StrictStr],
            Field(
                description='Type of logs to retrieve, either "build" or "runtime". Defaults to "runtime".'
            ),
        ] = None,
        app_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided app_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        service_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided service_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        deployment_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        regional_deployment_id: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Filter on the provided regional_deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        instance_id: Annotated[
            Optional[StrictStr],
            Field(description="Deprecated, prefer using instance_ids instead."),
        ] = None,
        instance_ids: Annotated[
            Optional[List[StrictStr]],
            Field(
                description="(Optional) Filter on the provided instance_ids. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set."
            ),
        ] = None,
        stream: Annotated[
            Optional[StrictStr],
            Field(description="Deprecated, prefer using streams instead."),
        ] = None,
        streams: Annotated[
            Optional[List[StrictStr]],
            Field(
                description='(Optional) Filter on stream: either "stdout", "stderr" or "koyeb" (for system logs).'
            ),
        ] = None,
        start: Annotated[
            Optional[datetime],
            Field(description="(Optional) Defaults to 24 hours ago."),
        ] = None,
        limit: Annotated[
            Optional[StrictStr],
            Field(description="(Optional) Defaults to 1000. Maximum of 1000."),
        ] = None,
        regex: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Apply a regex to filter logs. Can't be used with `text`."
            ),
        ] = None,
        text: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Looks for this string in logs. Can't be used with `regex`."
            ),
        ] = None,
        regions: Annotated[
            Optional[List[StrictStr]],
            Field(
                description='(Optional) Filter on the provided regions (e.g. ["fra", "was"]).'
            ),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """Tails logs


        :param type: Type of logs to retrieve, either \"build\" or \"runtime\". Defaults to \"runtime\".
        :type type: str
        :param app_id: (Optional) Filter on the provided app_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type app_id: str
        :param service_id: (Optional) Filter on the provided service_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type service_id: str
        :param deployment_id: (Optional) Filter on the provided deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type deployment_id: str
        :param regional_deployment_id: (Optional) Filter on the provided regional_deployment_id. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type regional_deployment_id: str
        :param instance_id: Deprecated, prefer using instance_ids instead.
        :type instance_id: str
        :param instance_ids: (Optional) Filter on the provided instance_ids. At least one of app_id, service_id, deployment_id, regional_deployment_id or instance_ids must be set.
        :type instance_ids: List[str]
        :param stream: Deprecated, prefer using streams instead.
        :type stream: str
        :param streams: (Optional) Filter on stream: either \"stdout\", \"stderr\" or \"koyeb\" (for system logs).
        :type streams: List[str]
        :param start: (Optional) Defaults to 24 hours ago.
        :type start: datetime
        :param limit: (Optional) Defaults to 1000. Maximum of 1000.
        :type limit: str
        :param regex: (Optional) Apply a regex to filter logs. Can't be used with `text`.
        :type regex: str
        :param text: (Optional) Looks for this string in logs. Can't be used with `regex`.
        :type text: str
        :param regions: (Optional) Filter on the provided regions (e.g. [\"fra\", \"was\"]).
        :type regions: List[str]
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """  # noqa: E501

        _param = self._tail_logs_serialize(
            type=type,
            app_id=app_id,
            service_id=service_id,
            deployment_id=deployment_id,
            regional_deployment_id=regional_deployment_id,
            instance_id=instance_id,
            instance_ids=instance_ids,
            stream=stream,
            streams=streams,
            start=start,
            limit=limit,
            regex=regex,
            text=text,
            regions=regions,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "StreamResultOfLogEntry",
            "400": "ErrorWithFields",
            "401": "Error",
            "403": "Error",
            "404": "Error",
            "500": "Error",
            "503": "Error",
            "default": "GoogleRpcStatus",
        }
        response_data = await self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        return response_data.response

    def _tail_logs_serialize(
        self,
        type,
        app_id,
        service_id,
        deployment_id,
        regional_deployment_id,
        instance_id,
        instance_ids,
        stream,
        streams,
        start,
        limit,
        regex,
        text,
        regions,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:
        _host = None

        _collection_formats: Dict[str, str] = {
            "instance_ids": "multi",
            "streams": "multi",
            "regions": "multi",
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Any] = self.api_client._merge_headers(_headers)
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[
            str, Union[str, bytes, List[str], List[bytes], List[Tuple[str, bytes]]]
        ] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        # process the query parameters
        if type is not None:
            _query_params.append(("type", type))

        if app_id is not None:
            _query_params.append(("app_id", app_id))

        if service_id is not None:
            _query_params.append(("service_id", service_id))

        if deployment_id is not None:
            _query_params.append(("deployment_id", deployment_id))

        if regional_deployment_id is not None:
            _query_params.append(("regional_deployment_id", regional_deployment_id))

        if instance_id is not None:
            _query_params.append(("instance_id", instance_id))

        if instance_ids is not None:
            _query_params.append(("instance_ids", instance_ids))

        if stream is not None:
            _query_params.append(("stream", stream))

        if streams is not None:
            _query_params.append(("streams", streams))

        if start is not None:
            if isinstance(start, datetime):
                _query_params.append(
                    (
                        "start",
                        start.strftime(self.api_client.configuration.datetime_format),
                    )
                )
            else:
                _query_params.append(("start", start))

        if limit is not None:
            _query_params.append(("limit", limit))

        if regex is not None:
            _query_params.append(("regex", regex))

        if text is not None:
            _query_params.append(("text", text))

        if regions is not None:
            _query_params.append(("regions", regions))

        # process the header parameters
        # process the form parameters
        # process the body parameter

        # set the HTTP header `Accept`
        if not any(key.lower() == "accept" for key in _header_params):
            _header_params["Accept"] = self.api_client.select_header_accept(["*/*"])

        # authentication setting
        _auth_settings: List[str] = ["Bearer"]

        return self.api_client.param_serialize(
            method="GET",
            resource_path="/v1/streams/logs/tail",
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth,
        )
