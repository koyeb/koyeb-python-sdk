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

from pydantic import Field, StrictBool, StrictStr, field_validator
from typing import List, Optional
from typing_extensions import Annotated
from koyeb.api.models.query_services_view_reply import QueryServicesViewReply

from koyeb.api.api_client import ApiClient, RequestSerialized
from koyeb.api.api_response import ApiResponse
from koyeb.api.rest import RESTResponseType


class ServiceViewsApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_call
    def query_services_view(
        self,
        search: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Case-insensitive search on the Service name and the App name"
            ),
        ] = None,
        filters_types: Annotated[
            Optional[List[StrictStr]],
            Field(description="(Optional) Filter on Service types"),
        ] = None,
        filters_statuses: Annotated[
            Optional[List[StrictStr]],
            Field(description="(Optional) Filter on Service statuses"),
        ] = None,
        filters_regions: Annotated[
            Optional[List[StrictStr]],
            Field(description="(Optional) Filter on regions of the latest Deployment"),
        ] = None,
        filters_app_ids: Annotated[
            Optional[List[StrictStr]], Field(description="(Optional) Filter on App ids")
        ] = None,
        filters_active_deployment_states: Annotated[
            Optional[List[StrictStr]],
            Field(
                description="(Optional) Filter on active Deployment states   - SLEEPING: The active Deployment is scaled to zero and wakes up on traffic"
            ),
        ] = None,
        filters_latest_deployment_states: Annotated[
            Optional[List[StrictStr]],
            Field(description="(Optional) Filter on latest Deployment states"),
        ] = None,
        filters_needs_attention: Annotated[
            Optional[StrictBool],
            Field(description="(Optional) Filter on Services that need attention"),
        ] = None,
        sort_field: Optional[StrictStr] = None,
        sort_direction: Optional[StrictStr] = None,
        group_by: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Group rows by App. Groups are ordered by App name and keep a stable order across pages. Pagination always counts Services"
            ),
        ] = None,
        limit: Annotated[
            Optional[StrictStr],
            Field(description="(Optional) The number of items to return"),
        ] = None,
        offset: Annotated[
            Optional[StrictStr],
            Field(description="(Optional) The offset in the list of item to return"),
        ] = None,
        facets: Annotated[
            Optional[List[StrictStr]],
            Field(description="(Optional) Facets to compute on the full result"),
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
    ) -> QueryServicesViewReply:
        """Query the Services view

        Unstable: this endpoint may change without notice.  Returns Services with their App and Deployment state. Filters, search, sorting, grouping, counts and facets are all computed on the full authorized result before pagination.

        :param search: (Optional) Case-insensitive search on the Service name and the App name
        :type search: str
        :param filters_types: (Optional) Filter on Service types
        :type filters_types: List[str]
        :param filters_statuses: (Optional) Filter on Service statuses
        :type filters_statuses: List[str]
        :param filters_regions: (Optional) Filter on regions of the latest Deployment
        :type filters_regions: List[str]
        :param filters_app_ids: (Optional) Filter on App ids
        :type filters_app_ids: List[str]
        :param filters_active_deployment_states: (Optional) Filter on active Deployment states   - SLEEPING: The active Deployment is scaled to zero and wakes up on traffic
        :type filters_active_deployment_states: List[str]
        :param filters_latest_deployment_states: (Optional) Filter on latest Deployment states
        :type filters_latest_deployment_states: List[str]
        :param filters_needs_attention: (Optional) Filter on Services that need attention
        :type filters_needs_attention: bool
        :param sort_field:
        :type sort_field: str
        :param sort_direction:
        :type sort_direction: str
        :param group_by: (Optional) Group rows by App. Groups are ordered by App name and keep a stable order across pages. Pagination always counts Services
        :type group_by: str
        :param limit: (Optional) The number of items to return
        :type limit: str
        :param offset: (Optional) The offset in the list of item to return
        :type offset: str
        :param facets: (Optional) Facets to compute on the full result
        :type facets: List[str]
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

        _param = self._query_services_view_serialize(
            search=search,
            filters_types=filters_types,
            filters_statuses=filters_statuses,
            filters_regions=filters_regions,
            filters_app_ids=filters_app_ids,
            filters_active_deployment_states=filters_active_deployment_states,
            filters_latest_deployment_states=filters_latest_deployment_states,
            filters_needs_attention=filters_needs_attention,
            sort_field=sort_field,
            sort_direction=sort_direction,
            group_by=group_by,
            limit=limit,
            offset=offset,
            facets=facets,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "QueryServicesViewReply",
            "400": "ErrorWithFields",
            "401": "Error",
            "403": "Error",
            "404": "Error",
            "500": "Error",
            "503": "Error",
            "default": "GoogleRpcStatus",
        }
        response_data = self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data

    @validate_call
    def query_services_view_with_http_info(
        self,
        search: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Case-insensitive search on the Service name and the App name"
            ),
        ] = None,
        filters_types: Annotated[
            Optional[List[StrictStr]],
            Field(description="(Optional) Filter on Service types"),
        ] = None,
        filters_statuses: Annotated[
            Optional[List[StrictStr]],
            Field(description="(Optional) Filter on Service statuses"),
        ] = None,
        filters_regions: Annotated[
            Optional[List[StrictStr]],
            Field(description="(Optional) Filter on regions of the latest Deployment"),
        ] = None,
        filters_app_ids: Annotated[
            Optional[List[StrictStr]], Field(description="(Optional) Filter on App ids")
        ] = None,
        filters_active_deployment_states: Annotated[
            Optional[List[StrictStr]],
            Field(
                description="(Optional) Filter on active Deployment states   - SLEEPING: The active Deployment is scaled to zero and wakes up on traffic"
            ),
        ] = None,
        filters_latest_deployment_states: Annotated[
            Optional[List[StrictStr]],
            Field(description="(Optional) Filter on latest Deployment states"),
        ] = None,
        filters_needs_attention: Annotated[
            Optional[StrictBool],
            Field(description="(Optional) Filter on Services that need attention"),
        ] = None,
        sort_field: Optional[StrictStr] = None,
        sort_direction: Optional[StrictStr] = None,
        group_by: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Group rows by App. Groups are ordered by App name and keep a stable order across pages. Pagination always counts Services"
            ),
        ] = None,
        limit: Annotated[
            Optional[StrictStr],
            Field(description="(Optional) The number of items to return"),
        ] = None,
        offset: Annotated[
            Optional[StrictStr],
            Field(description="(Optional) The offset in the list of item to return"),
        ] = None,
        facets: Annotated[
            Optional[List[StrictStr]],
            Field(description="(Optional) Facets to compute on the full result"),
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
    ) -> ApiResponse[QueryServicesViewReply]:
        """Query the Services view

        Unstable: this endpoint may change without notice.  Returns Services with their App and Deployment state. Filters, search, sorting, grouping, counts and facets are all computed on the full authorized result before pagination.

        :param search: (Optional) Case-insensitive search on the Service name and the App name
        :type search: str
        :param filters_types: (Optional) Filter on Service types
        :type filters_types: List[str]
        :param filters_statuses: (Optional) Filter on Service statuses
        :type filters_statuses: List[str]
        :param filters_regions: (Optional) Filter on regions of the latest Deployment
        :type filters_regions: List[str]
        :param filters_app_ids: (Optional) Filter on App ids
        :type filters_app_ids: List[str]
        :param filters_active_deployment_states: (Optional) Filter on active Deployment states   - SLEEPING: The active Deployment is scaled to zero and wakes up on traffic
        :type filters_active_deployment_states: List[str]
        :param filters_latest_deployment_states: (Optional) Filter on latest Deployment states
        :type filters_latest_deployment_states: List[str]
        :param filters_needs_attention: (Optional) Filter on Services that need attention
        :type filters_needs_attention: bool
        :param sort_field:
        :type sort_field: str
        :param sort_direction:
        :type sort_direction: str
        :param group_by: (Optional) Group rows by App. Groups are ordered by App name and keep a stable order across pages. Pagination always counts Services
        :type group_by: str
        :param limit: (Optional) The number of items to return
        :type limit: str
        :param offset: (Optional) The offset in the list of item to return
        :type offset: str
        :param facets: (Optional) Facets to compute on the full result
        :type facets: List[str]
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

        _param = self._query_services_view_serialize(
            search=search,
            filters_types=filters_types,
            filters_statuses=filters_statuses,
            filters_regions=filters_regions,
            filters_app_ids=filters_app_ids,
            filters_active_deployment_states=filters_active_deployment_states,
            filters_latest_deployment_states=filters_latest_deployment_states,
            filters_needs_attention=filters_needs_attention,
            sort_field=sort_field,
            sort_direction=sort_direction,
            group_by=group_by,
            limit=limit,
            offset=offset,
            facets=facets,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "QueryServicesViewReply",
            "400": "ErrorWithFields",
            "401": "Error",
            "403": "Error",
            "404": "Error",
            "500": "Error",
            "503": "Error",
            "default": "GoogleRpcStatus",
        }
        response_data = self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )

    @validate_call
    def query_services_view_without_preload_content(
        self,
        search: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Case-insensitive search on the Service name and the App name"
            ),
        ] = None,
        filters_types: Annotated[
            Optional[List[StrictStr]],
            Field(description="(Optional) Filter on Service types"),
        ] = None,
        filters_statuses: Annotated[
            Optional[List[StrictStr]],
            Field(description="(Optional) Filter on Service statuses"),
        ] = None,
        filters_regions: Annotated[
            Optional[List[StrictStr]],
            Field(description="(Optional) Filter on regions of the latest Deployment"),
        ] = None,
        filters_app_ids: Annotated[
            Optional[List[StrictStr]], Field(description="(Optional) Filter on App ids")
        ] = None,
        filters_active_deployment_states: Annotated[
            Optional[List[StrictStr]],
            Field(
                description="(Optional) Filter on active Deployment states   - SLEEPING: The active Deployment is scaled to zero and wakes up on traffic"
            ),
        ] = None,
        filters_latest_deployment_states: Annotated[
            Optional[List[StrictStr]],
            Field(description="(Optional) Filter on latest Deployment states"),
        ] = None,
        filters_needs_attention: Annotated[
            Optional[StrictBool],
            Field(description="(Optional) Filter on Services that need attention"),
        ] = None,
        sort_field: Optional[StrictStr] = None,
        sort_direction: Optional[StrictStr] = None,
        group_by: Annotated[
            Optional[StrictStr],
            Field(
                description="(Optional) Group rows by App. Groups are ordered by App name and keep a stable order across pages. Pagination always counts Services"
            ),
        ] = None,
        limit: Annotated[
            Optional[StrictStr],
            Field(description="(Optional) The number of items to return"),
        ] = None,
        offset: Annotated[
            Optional[StrictStr],
            Field(description="(Optional) The offset in the list of item to return"),
        ] = None,
        facets: Annotated[
            Optional[List[StrictStr]],
            Field(description="(Optional) Facets to compute on the full result"),
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
        """Query the Services view

        Unstable: this endpoint may change without notice.  Returns Services with their App and Deployment state. Filters, search, sorting, grouping, counts and facets are all computed on the full authorized result before pagination.

        :param search: (Optional) Case-insensitive search on the Service name and the App name
        :type search: str
        :param filters_types: (Optional) Filter on Service types
        :type filters_types: List[str]
        :param filters_statuses: (Optional) Filter on Service statuses
        :type filters_statuses: List[str]
        :param filters_regions: (Optional) Filter on regions of the latest Deployment
        :type filters_regions: List[str]
        :param filters_app_ids: (Optional) Filter on App ids
        :type filters_app_ids: List[str]
        :param filters_active_deployment_states: (Optional) Filter on active Deployment states   - SLEEPING: The active Deployment is scaled to zero and wakes up on traffic
        :type filters_active_deployment_states: List[str]
        :param filters_latest_deployment_states: (Optional) Filter on latest Deployment states
        :type filters_latest_deployment_states: List[str]
        :param filters_needs_attention: (Optional) Filter on Services that need attention
        :type filters_needs_attention: bool
        :param sort_field:
        :type sort_field: str
        :param sort_direction:
        :type sort_direction: str
        :param group_by: (Optional) Group rows by App. Groups are ordered by App name and keep a stable order across pages. Pagination always counts Services
        :type group_by: str
        :param limit: (Optional) The number of items to return
        :type limit: str
        :param offset: (Optional) The offset in the list of item to return
        :type offset: str
        :param facets: (Optional) Facets to compute on the full result
        :type facets: List[str]
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

        _param = self._query_services_view_serialize(
            search=search,
            filters_types=filters_types,
            filters_statuses=filters_statuses,
            filters_regions=filters_regions,
            filters_app_ids=filters_app_ids,
            filters_active_deployment_states=filters_active_deployment_states,
            filters_latest_deployment_states=filters_latest_deployment_states,
            filters_needs_attention=filters_needs_attention,
            sort_field=sort_field,
            sort_direction=sort_direction,
            group_by=group_by,
            limit=limit,
            offset=offset,
            facets=facets,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "QueryServicesViewReply",
            "400": "ErrorWithFields",
            "401": "Error",
            "403": "Error",
            "404": "Error",
            "500": "Error",
            "503": "Error",
            "default": "GoogleRpcStatus",
        }
        response_data = self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        return response_data.response

    def _query_services_view_serialize(
        self,
        search,
        filters_types,
        filters_statuses,
        filters_regions,
        filters_app_ids,
        filters_active_deployment_states,
        filters_latest_deployment_states,
        filters_needs_attention,
        sort_field,
        sort_direction,
        group_by,
        limit,
        offset,
        facets,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:
        _host = None

        _collection_formats: Dict[str, str] = {
            "filters.types": "multi",
            "filters.statuses": "multi",
            "filters.regions": "multi",
            "filters.app_ids": "multi",
            "filters.active_deployment_states": "multi",
            "filters.latest_deployment_states": "multi",
            "facets": "multi",
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
        if search is not None:
            _query_params.append(("search", search))

        if filters_types is not None:
            _query_params.append(("filters.types", filters_types))

        if filters_statuses is not None:
            _query_params.append(("filters.statuses", filters_statuses))

        if filters_regions is not None:
            _query_params.append(("filters.regions", filters_regions))

        if filters_app_ids is not None:
            _query_params.append(("filters.app_ids", filters_app_ids))

        if filters_active_deployment_states is not None:
            _query_params.append(
                ("filters.active_deployment_states", filters_active_deployment_states)
            )

        if filters_latest_deployment_states is not None:
            _query_params.append(
                ("filters.latest_deployment_states", filters_latest_deployment_states)
            )

        if filters_needs_attention is not None:
            _query_params.append(("filters.needs_attention", filters_needs_attention))

        if sort_field is not None:
            _query_params.append(("sort.field", sort_field))

        if sort_direction is not None:
            _query_params.append(("sort.direction", sort_direction))

        if group_by is not None:
            _query_params.append(("group_by", group_by))

        if limit is not None:
            _query_params.append(("limit", limit))

        if offset is not None:
            _query_params.append(("offset", offset))

        if facets is not None:
            _query_params.append(("facets", facets))

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
            resource_path="/v1/views/services",
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
