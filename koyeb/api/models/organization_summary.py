# coding: utf-8

"""
    Koyeb Rest API

    Welcome to the Koyeb API documentation.  The Koyeb API allows you to interact with the Koyeb platform in a simple, programmatic way using conventional HTTP requests. The API has predictable resource-oriented URLs, allowing you to request, retrieve and execute actions on resources efficiently.  The API returns JSON-encoded responses and uses standard HTTP response codes, and verbs.  All of the functionality available in the Koyeb Control Panel is also available via the API, allowing you to automate repetitive and complex actions as required.  All production API requests are made to:  - https://app.koyeb.com/<version>  All data is sent and received as JSON.  ## Constructing Requests  Requests are made of three components:  - Base URL: `https://app.koyeb.com` - API Version: `v1` - Resource path: `apps`  To construct a proper request, you need to format the URL as follows:  `https://app.koyeb.com/{version}/{resource}`  Example: `https://app.koyeb.com/v1/apps`  The following code is an example request to retrieve the list of Apps.  ``` $ curl -H 'Authorization: Bearer 1111-1111-1111-1111-1111' https://app.koyeb.com/v1/apps {   \"apps\": [     {       \"id\": \"e267e09d-a2ef-4672-95c7-bf88d787a274\",       \"name\": \"demo\",       \"organization_id\": \"c402bcad-d06d-4fd6-8af2-08b790c0e249\",       \"updated_at\": \"2021-04-26T08:28:59.221274Z\",       \"created_at\": \"2021-04-26T08:28:59.221274Z\",       \"domains\": [         {           \"name\": \"demo-koyeb.koyeb.app\",           \"deployment_group\": \"prod\"         }       ]     },     {       \"id\": \"e38caea5-5acb-4fec-aa65-81749546b470\",       \"name\": \"www\",       \"organization_id\": \"c402bcad-d06d-4fd6-8af2-08b790c0e249\",       \"updated_at\": \"2021-05-04T08:56:40.557792Z\",       \"created_at\": \"2021-05-04T08:56:40.557792Z\",       \"domains\": [         {           \"name\": \"www-koyeb.koyeb.app\",           \"deployment_group\": \"prod\"         }       ]     }   ],   \"limit\": 20,   \"offset\": 0,   \"count\": 2 } ```  # Authentication  The Koyeb API uses API keys to authenticate requests. You can view and manage your API keys in the Koyeb Control Panel.  Your API keys carry many privileges. Take care to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, Slack, client-side code, and so forth.  To make an authenticated request, include a bearer-type Authorization header containing your API key, prefixed with `Bearer `:  ``` Authorization: Bearer <your-api-key> ```  All API requests must be made over HTTPS. Calls made over plain HTTP will fail. API requests without authentication will also fail.  # Errors  We use conventional HTTP response codes to indicate the success or failure of an API request.  In general, codes in the 2xx range indicate success, codes in the 4xx range indicate an error that resulted from the provided information (e.g., a required parameter is missing, resource not found), and codes in the 5xx range indicate an error with our servers.  ## HTTP Status Code Summary  - `200 OK` - Everything worked as expected. - `400 Bad Request` - Often missing a required parameter. - `401 Unauthorized` - No valid API key provided. - `402 Request Failed` - Parameters were valid, but the request failed. - `403 Forbidden` - Insufficient privileges to access the requested resource. - `404 Not Found` - The requested item doesn't exist. - `50x` Server errors - Something went wrong on the API domain's end.  Input and output data must be valid JSON with the appropriate Content-Type header set.  ## Attributes  - code:    - `invalid_argument`: Occur when your request has invalid parameters.   - `unknown_resource`: Occur when the resource doesn't exist.   - `authentication_error`: Arise when there is a problem with authentication.   - `rate_limit_error`: Too many requests hit the API too quickly.   - `authorization_required`: You don't have sufficient right to access the resource.   - `api_error`: API errors use in case of a problem with api domain's servers (extremely uncommon).  - message:    - A human-readable error giving more details about the error  - status:    - The HTTP code returned by the server.  - fields (Optional):    - An array of parameters with a human-readable message giving more details about the error.  ## Errors responses example  Response 400 (application/json)  ``` {   \"status\": 400,   \"code\": \"invalid_argument\",   \"message\": \"Invalid argument\",   \"fields\": [     {       \"field\": \"definition.docker.image\",       \"description\": \"cannot be blank\"     }   ] } ```  Response 401 (application/json)  ``` {   \"status\": 401,   \"code\": \"authentication_error\",   \"message\": \"Request unauthenticated with bearer\" } ```  Response 403 (application/json)  ``` {   \"status\": 403,   \"code\": \"authentication_required\",   \"message\": \"You don't have the requested permission to access to resource.\" } ```   Response 404 (application/json)  ``` {   \"status\": 404,   \"code\": \"unknown_resource\",   \"message\": \"App not found\" } ```  # Pagination  All top-level API resources receive a paginated response. For instance, list Apps, list Services, and others share a standard structure, taking two parameters: limit and offset.  **Paginated request**  Requests against paginated endpoints accept two query string arguments:  * *limit*, a positive integer lower or equal to 100 to select the number of items to display. * *offset*, an integer to indicate the position to start at.  Paginated endpoints usually also accept filters to search and sort results. These filters are documented along with each endpoint documentation. 

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from koyeb.api.models.apps_summary import AppsSummary
from koyeb.api.models.domains_summary import DomainsSummary
from koyeb.api.models.instances_summary import InstancesSummary
from koyeb.api.models.members_summary import MembersSummary
from koyeb.api.models.neon_postgres_summary import NeonPostgresSummary
from koyeb.api.models.secrets_summary import SecretsSummary
from koyeb.api.models.service_summary import ServiceSummary
from typing import Optional, Set
from typing_extensions import Self
from pydantic_core import to_jsonable_python


class OrganizationSummary(BaseModel):
    """
    OrganizationSummary
    """  # noqa: E501

    organization_id: Optional[StrictStr] = None
    instances: Optional[InstancesSummary] = None
    apps: Optional[AppsSummary] = None
    services: Optional[Dict[str, ServiceSummary]] = None
    domains: Optional[DomainsSummary] = None
    secrets: Optional[SecretsSummary] = None
    neon_postgres: Optional[NeonPostgresSummary] = None
    members: Optional[MembersSummary] = None
    __properties: ClassVar[List[str]] = [
        "organization_id",
        "instances",
        "apps",
        "services",
        "domains",
        "secrets",
        "neon_postgres",
        "members",
    ]

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(to_jsonable_python(self.to_dict()))

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of OrganizationSummary from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of instances
        if self.instances:
            _dict["instances"] = self.instances.to_dict()
        # override the default output from pydantic by calling `to_dict()` of apps
        if self.apps:
            _dict["apps"] = self.apps.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each value in services (dict)
        _field_dict = {}
        if self.services:
            for _key_services in self.services:
                _field_dict[_key_services] = (
                    self.services[_key_services].to_dict()
                    if self.services[_key_services] is not None
                    else None
                )
            _dict["services"] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of domains
        if self.domains:
            _dict["domains"] = self.domains.to_dict()
        # override the default output from pydantic by calling `to_dict()` of secrets
        if self.secrets:
            _dict["secrets"] = self.secrets.to_dict()
        # override the default output from pydantic by calling `to_dict()` of neon_postgres
        if self.neon_postgres:
            _dict["neon_postgres"] = self.neon_postgres.to_dict()
        # override the default output from pydantic by calling `to_dict()` of members
        if self.members:
            _dict["members"] = self.members.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of OrganizationSummary from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "organization_id": obj.get("organization_id"),
                "instances": InstancesSummary.from_dict(obj["instances"])
                if obj.get("instances") is not None
                else None,
                "apps": AppsSummary.from_dict(obj["apps"])
                if obj.get("apps") is not None
                else None,
                "services": dict(
                    (_k, ServiceSummary.from_dict(_v))
                    for _k, _v in obj["services"].items()
                )
                if obj.get("services") is not None
                else None,
                "domains": DomainsSummary.from_dict(obj["domains"])
                if obj.get("domains") is not None
                else None,
                "secrets": SecretsSummary.from_dict(obj["secrets"])
                if obj.get("secrets") is not None
                else None,
                "neon_postgres": NeonPostgresSummary.from_dict(obj["neon_postgres"])
                if obj.get("neon_postgres") is not None
                else None,
                "members": MembersSummary.from_dict(obj["members"])
                if obj.get("members") is not None
                else None,
            }
        )
        return _obj
