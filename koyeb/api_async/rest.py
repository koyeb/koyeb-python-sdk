# coding: utf-8

"""
    Koyeb Rest API

    Welcome to the Koyeb API documentation.  The Koyeb API allows you to interact with the Koyeb platform in a simple, programmatic way using conventional HTTP requests. The API has predictable resource-oriented URLs, allowing you to request, retrieve and execute actions on resources efficiently.  The API returns JSON-encoded responses and uses standard HTTP response codes, and verbs.  All of the functionality available in the Koyeb Control Panel is also available via the API, allowing you to automate repetitive and complex actions as required.  All production API requests are made to:  - https://app.koyeb.com/<version>  All data is sent and received as JSON.  ## Constructing Requests  Requests are made of three components:  - Base URL: `https://app.koyeb.com` - API Version: `v1` - Resource path: `apps`  To construct a proper request, you need to format the URL as follows:  `https://app.koyeb.com/{version}/{resource}`  Example: `https://app.koyeb.com/v1/apps`  The following code is an example request to retrieve the list of Apps.  ``` $ curl -H 'Authorization: Bearer 1111-1111-1111-1111-1111' https://app.koyeb.com/v1/apps {   \"apps\": [     {       \"id\": \"e267e09d-a2ef-4672-95c7-bf88d787a274\",       \"name\": \"demo\",       \"organization_id\": \"c402bcad-d06d-4fd6-8af2-08b790c0e249\",       \"updated_at\": \"2021-04-26T08:28:59.221274Z\",       \"created_at\": \"2021-04-26T08:28:59.221274Z\",       \"domains\": [         {           \"name\": \"demo-koyeb.koyeb.app\",           \"deployment_group\": \"prod\"         }       ]     },     {       \"id\": \"e38caea5-5acb-4fec-aa65-81749546b470\",       \"name\": \"www\",       \"organization_id\": \"c402bcad-d06d-4fd6-8af2-08b790c0e249\",       \"updated_at\": \"2021-05-04T08:56:40.557792Z\",       \"created_at\": \"2021-05-04T08:56:40.557792Z\",       \"domains\": [         {           \"name\": \"www-koyeb.koyeb.app\",           \"deployment_group\": \"prod\"         }       ]     }   ],   \"limit\": 20,   \"offset\": 0,   \"count\": 2 } ```  # Authentication  The Koyeb API uses API keys to authenticate requests. You can view and manage your API keys in the Koyeb Control Panel.  Your API keys carry many privileges. Take care to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, Slack, client-side code, and so forth.  To make an authenticated request, include a bearer-type Authorization header containing your API key, prefixed with `Bearer `:  ``` Authorization: Bearer <your-api-key> ```  All API requests must be made over HTTPS. Calls made over plain HTTP will fail. API requests without authentication will also fail.  # Errors  We use conventional HTTP response codes to indicate the success or failure of an API request.  In general, codes in the 2xx range indicate success, codes in the 4xx range indicate an error that resulted from the provided information (e.g., a required parameter is missing, resource not found), and codes in the 5xx range indicate an error with our servers.  ## HTTP Status Code Summary  - `200 OK` - Everything worked as expected. - `400 Bad Request` - Often missing a required parameter. - `401 Unauthorized` - No valid API key provided. - `402 Request Failed` - Parameters were valid, but the request failed. - `403 Forbidden` - Insufficient privileges to access the requested resource. - `404 Not Found` - The requested item doesn't exist. - `50x` Server errors - Something went wrong on the API domain's end.  Input and output data must be valid JSON with the appropriate Content-Type header set.  ## Attributes  - code:    - `invalid_argument`: Occur when your request has invalid parameters.   - `unknown_resource`: Occur when the resource doesn't exist.   - `authentication_error`: Arise when there is a problem with authentication.   - `rate_limit_error`: Too many requests hit the API too quickly.   - `authorization_required`: You don't have sufficient right to access the resource.   - `api_error`: API errors use in case of a problem with api domain's servers (extremely uncommon).  - message:    - A human-readable error giving more details about the error  - status:    - The HTTP code returned by the server.  - fields (Optional):    - An array of parameters with a human-readable message giving more details about the error.  ## Errors responses example  Response 400 (application/json)  ``` {   \"status\": 400,   \"code\": \"invalid_argument\",   \"message\": \"Invalid argument\",   \"fields\": [     {       \"field\": \"definition.docker.image\",       \"description\": \"cannot be blank\"     }   ] } ```  Response 401 (application/json)  ``` {   \"status\": 401,   \"code\": \"authentication_error\",   \"message\": \"Request unauthenticated with bearer\" } ```  Response 403 (application/json)  ``` {   \"status\": 403,   \"code\": \"authentication_required\",   \"message\": \"You don't have the requested permission to access to resource.\" } ```   Response 404 (application/json)  ``` {   \"status\": 404,   \"code\": \"unknown_resource\",   \"message\": \"App not found\" } ```  # Pagination  All top-level API resources receive a paginated response. For instance, list Apps, list Services, and others share a standard structure, taking two parameters: limit and offset.  **Paginated request**  Requests against paginated endpoints accept two query string arguments:  * *limit*, a positive integer lower or equal to 100 to select the number of items to display. * *offset*, an integer to indicate the position to start at.  Paginated endpoints usually also accept filters to search and sort results. These filters are documented along with each endpoint documentation. 

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import io
import json
import re
import ssl
from typing import Optional, Union

import httpx

from koyeb.api_async.exceptions import ApiException, ApiValueError

RESTResponseType = httpx.Response


class RESTResponse(io.IOBase):
    def __init__(self, resp) -> None:
        self.response = resp
        self.status = resp.status_code
        self.reason = resp.reason_phrase
        self.data = None

    async def read(self):
        if self.data is None:
            self.data = await self.response.aread()
        return self.data

    @property
    def headers(self):
        """Returns a CIMultiDictProxy of response headers."""
        return self.response.headers

    def getheaders(self):
        """Returns a CIMultiDictProxy of the response headers; use ``headers`` instead."""
        return self.response.headers

    def getheader(self, name, default=None):
        """Returns a given response header; use ``headers`` instead."""
        return self.response.headers.get(name, default)


class RESTClientObject:
    def __init__(self, configuration) -> None:
        # maxsize is number of requests to host that are allowed in parallel
        self.maxsize = configuration.connection_pool_maxsize

        self.ssl_context = ssl.create_default_context(
            cafile=configuration.ssl_ca_cert,
            cadata=configuration.ca_cert_data,
        )
        if configuration.cert_file:
            self.ssl_context.load_cert_chain(
                configuration.cert_file, keyfile=configuration.key_file
            )

        if not configuration.verify_ssl:
            self.ssl_context.check_hostname = False
            self.ssl_context.verify_mode = ssl.CERT_NONE

        self.proxy = configuration.proxy
        self.proxy_headers = configuration.proxy_headers

        self.pool_manager: Optional[httpx.AsyncClient] = None

    async def close(self):
        if self.pool_manager is not None:
            await self.pool_manager.aclose()

    async def request(
        self,
        method,
        url,
        headers=None,
        body=None,
        post_params=None,
        _request_timeout=None,
    ):
        """Execute request

        :param method: http request method
        :param url: http request url
        :param headers: http request headers
        :param body: request json body, for `application/json`
        :param post_params: request post parameters,
                            `application/x-www-form-urlencoded`
                            and `multipart/form-data`
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        """
        method = method.upper()
        assert method in ["GET", "HEAD", "DELETE", "POST", "PUT", "PATCH", "OPTIONS"]

        if post_params and body:
            raise ApiValueError(
                "body parameter cannot be used with post_params parameter."
            )

        post_params = post_params or {}
        headers = httpx.Headers(headers or {})
        timeout = _request_timeout or 5 * 60

        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"

        args = {"method": method, "url": url, "timeout": timeout, "headers": headers}

        # For `POST`, `PUT`, `PATCH`, `OPTIONS`, `DELETE`
        if method in ["POST", "PUT", "PATCH", "OPTIONS", "DELETE"]:
            if re.search("json", headers["Content-Type"], re.IGNORECASE):
                if body is not None:
                    args["json"] = body
                if body is None and post_params:
                    args["json"] = dict(post_params)
            elif (
                headers["Content-Type"] == "application/x-www-form-urlencoded"
            ):  # noqa: E501
                args["data"] = dict(post_params)
            elif headers["Content-Type"] == "multipart/form-data":
                # must del headers['Content-Type'], or the correct
                # Content-Type which generated by httpx
                del headers["Content-Type"]

                files = []
                data = {}
                for param in post_params:
                    k, v = param
                    if isinstance(v, tuple) and len(v) == 3:
                        files.append((k, v))
                    else:
                        # Ensures that dict objects are serialized
                        if isinstance(v, dict):
                            v = json.dumps(v)
                        elif isinstance(v, int):
                            v = str(v)
                        data[k] = v

                if files:
                    args["files"] = files
                if data:
                    args["data"] = data

            # Pass a `bytes` parameter directly in the body to support
            # other content types than Json when `body` argument is provided
            # in serialized form
            elif isinstance(body, str) or isinstance(body, bytes):
                args["data"] = body
            else:
                # Cannot generate the request from given parameters
                msg = """Cannot prepare a request message for provided
                         arguments. Please check that your arguments match
                         declared content type."""
                raise ApiException(status=0, reason=msg)

        if self.pool_manager is None:
            self.pool_manager = self._create_pool_manager()

        r = await self.pool_manager.request(**args)
        return RESTResponse(r)

    def _create_pool_manager(self) -> httpx.AsyncClient:
        limits = httpx.Limits(max_connections=self.maxsize)

        proxy = None
        if self.proxy:
            proxy = httpx.Proxy(url=self.proxy, headers=self.proxy_headers)

        return httpx.AsyncClient(
            limits=limits, proxy=proxy, verify=self.ssl_context, trust_env=True
        )
