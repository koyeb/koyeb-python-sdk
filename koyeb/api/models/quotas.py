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

from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from koyeb.api.models.domain_load_balancer_quotas import DomainLoadBalancerQuotas
from koyeb.api.models.instance_snapshot_quotas import InstanceSnapshotQuotas
from koyeb.api.models.lifecycle_quotas import LifecycleQuotas
from koyeb.api.models.persistent_volume_quotas import PersistentVolumeQuotas
from koyeb.api.models.scale_to_zero_quotas import ScaleToZeroQuotas
from typing import Optional, Set
from typing_extensions import Self
from pydantic_core import to_jsonable_python


class Quotas(BaseModel):
    """
    Quotas
    """  # noqa: E501

    apps: Optional[StrictStr] = None
    services: Optional[StrictStr] = None
    domains: Optional[StrictStr] = None
    service_provisioning_concurrency: Optional[StrictStr] = None
    memory_mb: Optional[StrictStr] = None
    instance_types: Optional[List[StrictStr]] = None
    regions: Optional[List[StrictStr]] = None
    max_organization_members: Optional[StrictStr] = None
    max_instances_by_type: Optional[Dict[str, StrictStr]] = None
    persistent_volumes_by_region: Optional[Dict[str, PersistentVolumeQuotas]] = None
    custom_domains: Optional[StrictStr] = None
    domains_load_balancer: Optional[DomainLoadBalancerQuotas] = None
    metrics_retention: Optional[StrictInt] = None
    logs_retention: Optional[StrictInt] = None
    access_reserved_subdomains: Optional[List[StrictStr]] = None
    proxy_ports: Optional[StrictInt] = None
    scale_to_zero: Optional[ScaleToZeroQuotas] = None
    archives: Optional[StrictStr] = None
    archive_max_size_mb: Optional[StrictStr] = None
    lifecycle: Optional[LifecycleQuotas] = None
    max_projects: Optional[StrictStr] = None
    instance_snapshots: Optional[InstanceSnapshotQuotas] = None
    __properties: ClassVar[List[str]] = [
        "apps",
        "services",
        "domains",
        "service_provisioning_concurrency",
        "memory_mb",
        "instance_types",
        "regions",
        "max_organization_members",
        "max_instances_by_type",
        "persistent_volumes_by_region",
        "custom_domains",
        "domains_load_balancer",
        "metrics_retention",
        "logs_retention",
        "access_reserved_subdomains",
        "proxy_ports",
        "scale_to_zero",
        "archives",
        "archive_max_size_mb",
        "lifecycle",
        "max_projects",
        "instance_snapshots",
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
        """Create an instance of Quotas from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each value in persistent_volumes_by_region (dict)
        _field_dict = {}
        if self.persistent_volumes_by_region:
            for _key_persistent_volumes_by_region in self.persistent_volumes_by_region:
                _field_dict[_key_persistent_volumes_by_region] = (
                    self.persistent_volumes_by_region[
                        _key_persistent_volumes_by_region
                    ].to_dict()
                    if self.persistent_volumes_by_region[
                        _key_persistent_volumes_by_region
                    ]
                    is not None
                    else None
                )
            _dict["persistent_volumes_by_region"] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of domains_load_balancer
        if self.domains_load_balancer:
            _dict["domains_load_balancer"] = self.domains_load_balancer.to_dict()
        # override the default output from pydantic by calling `to_dict()` of scale_to_zero
        if self.scale_to_zero:
            _dict["scale_to_zero"] = self.scale_to_zero.to_dict()
        # override the default output from pydantic by calling `to_dict()` of lifecycle
        if self.lifecycle:
            _dict["lifecycle"] = self.lifecycle.to_dict()
        # override the default output from pydantic by calling `to_dict()` of instance_snapshots
        if self.instance_snapshots:
            _dict["instance_snapshots"] = self.instance_snapshots.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Quotas from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "apps": obj.get("apps"),
                "services": obj.get("services"),
                "domains": obj.get("domains"),
                "service_provisioning_concurrency": obj.get(
                    "service_provisioning_concurrency"
                ),
                "memory_mb": obj.get("memory_mb"),
                "instance_types": obj.get("instance_types"),
                "regions": obj.get("regions"),
                "max_organization_members": obj.get("max_organization_members"),
                "max_instances_by_type": obj.get("max_instances_by_type"),
                "persistent_volumes_by_region": dict(
                    (_k, PersistentVolumeQuotas.from_dict(_v))
                    for _k, _v in obj["persistent_volumes_by_region"].items()
                )
                if obj.get("persistent_volumes_by_region") is not None
                else None,
                "custom_domains": obj.get("custom_domains"),
                "domains_load_balancer": DomainLoadBalancerQuotas.from_dict(
                    obj["domains_load_balancer"]
                )
                if obj.get("domains_load_balancer") is not None
                else None,
                "metrics_retention": obj.get("metrics_retention"),
                "logs_retention": obj.get("logs_retention"),
                "access_reserved_subdomains": obj.get("access_reserved_subdomains"),
                "proxy_ports": obj.get("proxy_ports"),
                "scale_to_zero": ScaleToZeroQuotas.from_dict(obj["scale_to_zero"])
                if obj.get("scale_to_zero") is not None
                else None,
                "archives": obj.get("archives"),
                "archive_max_size_mb": obj.get("archive_max_size_mb"),
                "lifecycle": LifecycleQuotas.from_dict(obj["lifecycle"])
                if obj.get("lifecycle") is not None
                else None,
                "max_projects": obj.get("max_projects"),
                "instance_snapshots": InstanceSnapshotQuotas.from_dict(
                    obj["instance_snapshots"]
                )
                if obj.get("instance_snapshots") is not None
                else None,
            }
        )
        return _obj
