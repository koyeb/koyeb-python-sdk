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

from datetime import datetime
from pydantic import BaseModel, ConfigDict, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from koyeb.api_async.models.deployment_provisioning_info import (
    DeploymentProvisioningInfo,
)
from koyeb.api_async.models.regional_deployment_definition import (
    RegionalDeploymentDefinition,
)
from koyeb.api_async.models.regional_deployment_metadata import (
    RegionalDeploymentMetadata,
)
from koyeb.api_async.models.regional_deployment_role import RegionalDeploymentRole
from koyeb.api_async.models.regional_deployment_status import RegionalDeploymentStatus
from typing import Optional, Set
from typing_extensions import Self
from pydantic_core import to_jsonable_python


class RegionalDeployment(BaseModel):
    """
    RegionalDeployment
    """  # noqa: E501

    id: Optional[StrictStr] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    scheduled_at: Optional[datetime] = None
    allocated_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    succeeded_at: Optional[datetime] = None
    terminated_at: Optional[datetime] = None
    organization_id: Optional[StrictStr] = None
    app_id: Optional[StrictStr] = None
    service_id: Optional[StrictStr] = None
    region: Optional[StrictStr] = None
    parent_id: Optional[StrictStr] = None
    child_id: Optional[StrictStr] = None
    status: Optional[RegionalDeploymentStatus] = RegionalDeploymentStatus.PENDING
    messages: Optional[List[StrictStr]] = None
    definition: Optional[RegionalDeploymentDefinition] = None
    datacenters: Optional[List[StrictStr]] = None
    metadata: Optional[RegionalDeploymentMetadata] = None
    provisioning_info: Optional[DeploymentProvisioningInfo] = None
    role: Optional[RegionalDeploymentRole] = RegionalDeploymentRole.INVALID
    instance_snapshot_id: Optional[StrictStr] = None
    version: Optional[StrictStr] = None
    deployment_group: Optional[StrictStr] = None
    deployment_id: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = [
        "id",
        "created_at",
        "updated_at",
        "scheduled_at",
        "allocated_at",
        "started_at",
        "succeeded_at",
        "terminated_at",
        "organization_id",
        "app_id",
        "service_id",
        "region",
        "parent_id",
        "child_id",
        "status",
        "messages",
        "definition",
        "datacenters",
        "metadata",
        "provisioning_info",
        "role",
        "instance_snapshot_id",
        "version",
        "deployment_group",
        "deployment_id",
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
        """Create an instance of RegionalDeployment from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of definition
        if self.definition:
            _dict["definition"] = self.definition.to_dict()
        # override the default output from pydantic by calling `to_dict()` of metadata
        if self.metadata:
            _dict["metadata"] = self.metadata.to_dict()
        # override the default output from pydantic by calling `to_dict()` of provisioning_info
        if self.provisioning_info:
            _dict["provisioning_info"] = self.provisioning_info.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of RegionalDeployment from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "id": obj.get("id"),
                "created_at": obj.get("created_at"),
                "updated_at": obj.get("updated_at"),
                "scheduled_at": obj.get("scheduled_at"),
                "allocated_at": obj.get("allocated_at"),
                "started_at": obj.get("started_at"),
                "succeeded_at": obj.get("succeeded_at"),
                "terminated_at": obj.get("terminated_at"),
                "organization_id": obj.get("organization_id"),
                "app_id": obj.get("app_id"),
                "service_id": obj.get("service_id"),
                "region": obj.get("region"),
                "parent_id": obj.get("parent_id"),
                "child_id": obj.get("child_id"),
                "status": obj.get("status")
                if obj.get("status") is not None
                else RegionalDeploymentStatus.PENDING,
                "messages": obj.get("messages"),
                "definition": RegionalDeploymentDefinition.from_dict(obj["definition"])
                if obj.get("definition") is not None
                else None,
                "datacenters": obj.get("datacenters"),
                "metadata": RegionalDeploymentMetadata.from_dict(obj["metadata"])
                if obj.get("metadata") is not None
                else None,
                "provisioning_info": DeploymentProvisioningInfo.from_dict(
                    obj["provisioning_info"]
                )
                if obj.get("provisioning_info") is not None
                else None,
                "role": obj.get("role")
                if obj.get("role") is not None
                else RegionalDeploymentRole.INVALID,
                "instance_snapshot_id": obj.get("instance_snapshot_id"),
                "version": obj.get("version"),
                "deployment_group": obj.get("deployment_group"),
                "deployment_id": obj.get("deployment_id"),
            }
        )
        return _obj
