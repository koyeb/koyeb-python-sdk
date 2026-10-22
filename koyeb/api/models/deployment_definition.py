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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from koyeb.api.models.archive_source import ArchiveSource
from koyeb.api.models.config_file import ConfigFile
from koyeb.api.models.database_source import DatabaseSource
from koyeb.api.models.deployment_definition_type import DeploymentDefinitionType
from koyeb.api.models.deployment_env import DeploymentEnv
from koyeb.api.models.deployment_health_check import DeploymentHealthCheck
from koyeb.api.models.deployment_instance_type import DeploymentInstanceType
from koyeb.api.models.deployment_mesh import DeploymentMesh
from koyeb.api.models.deployment_port import DeploymentPort
from koyeb.api.models.deployment_proxy_port import DeploymentProxyPort
from koyeb.api.models.deployment_route import DeploymentRoute
from koyeb.api.models.deployment_scaling import DeploymentScaling
from koyeb.api.models.deployment_strategy import DeploymentStrategy
from koyeb.api.models.deployment_volume import DeploymentVolume
from koyeb.api.models.docker_source import DockerSource
from koyeb.api.models.git_source import GitSource
from koyeb.api.models.network_policy import NetworkPolicy
from typing import Optional, Set
from typing_extensions import Self
from pydantic_core import to_jsonable_python


class DeploymentDefinition(BaseModel):
    """
    DeploymentDefinition
    """  # noqa: E501

    name: Optional[StrictStr] = Field(
        default=None,
        description="Service name. Deprecated, set it directly in the Service when creating it.",
    )
    type: Optional[DeploymentDefinitionType] = DeploymentDefinitionType.INVALID
    strategy: Optional[DeploymentStrategy] = None
    routes: Optional[List[DeploymentRoute]] = None
    ports: Optional[List[DeploymentPort]] = None
    proxy_ports: Optional[List[DeploymentProxyPort]] = None
    env: Optional[List[DeploymentEnv]] = None
    regions: Optional[List[StrictStr]] = None
    scalings: Optional[List[DeploymentScaling]] = None
    instance_types: Optional[List[DeploymentInstanceType]] = None
    health_checks: Optional[List[DeploymentHealthCheck]] = None
    volumes: Optional[List[DeploymentVolume]] = None
    config_files: Optional[List[ConfigFile]] = None
    skip_cache: Optional[StrictBool] = None
    mesh: Optional[DeploymentMesh] = DeploymentMesh.DEPLOYMENT_MESH_AUTO
    network_policy: Optional[NetworkPolicy] = None
    docker: Optional[DockerSource] = None
    git: Optional[GitSource] = None
    database: Optional[DatabaseSource] = None
    archive: Optional[ArchiveSource] = None
    __properties: ClassVar[List[str]] = [
        "name",
        "type",
        "strategy",
        "routes",
        "ports",
        "proxy_ports",
        "env",
        "regions",
        "scalings",
        "instance_types",
        "health_checks",
        "volumes",
        "config_files",
        "skip_cache",
        "mesh",
        "network_policy",
        "docker",
        "git",
        "database",
        "archive",
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
        """Create an instance of DeploymentDefinition from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of strategy
        if self.strategy:
            _dict["strategy"] = self.strategy.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in routes (list)
        _items = []
        if self.routes:
            for _item_routes in self.routes:
                _items.append(
                    _item_routes.to_dict() if _item_routes is not None else None
                )
            _dict["routes"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in ports (list)
        _items = []
        if self.ports:
            for _item_ports in self.ports:
                _items.append(
                    _item_ports.to_dict() if _item_ports is not None else None
                )
            _dict["ports"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in proxy_ports (list)
        _items = []
        if self.proxy_ports:
            for _item_proxy_ports in self.proxy_ports:
                _items.append(
                    _item_proxy_ports.to_dict()
                    if _item_proxy_ports is not None
                    else None
                )
            _dict["proxy_ports"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in env (list)
        _items = []
        if self.env:
            for _item_env in self.env:
                _items.append(_item_env.to_dict() if _item_env is not None else None)
            _dict["env"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in scalings (list)
        _items = []
        if self.scalings:
            for _item_scalings in self.scalings:
                _items.append(
                    _item_scalings.to_dict() if _item_scalings is not None else None
                )
            _dict["scalings"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in instance_types (list)
        _items = []
        if self.instance_types:
            for _item_instance_types in self.instance_types:
                _items.append(
                    _item_instance_types.to_dict()
                    if _item_instance_types is not None
                    else None
                )
            _dict["instance_types"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in health_checks (list)
        _items = []
        if self.health_checks:
            for _item_health_checks in self.health_checks:
                _items.append(
                    _item_health_checks.to_dict()
                    if _item_health_checks is not None
                    else None
                )
            _dict["health_checks"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in volumes (list)
        _items = []
        if self.volumes:
            for _item_volumes in self.volumes:
                _items.append(
                    _item_volumes.to_dict() if _item_volumes is not None else None
                )
            _dict["volumes"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in config_files (list)
        _items = []
        if self.config_files:
            for _item_config_files in self.config_files:
                _items.append(
                    _item_config_files.to_dict()
                    if _item_config_files is not None
                    else None
                )
            _dict["config_files"] = _items
        # override the default output from pydantic by calling `to_dict()` of network_policy
        if self.network_policy:
            _dict["network_policy"] = self.network_policy.to_dict()
        # override the default output from pydantic by calling `to_dict()` of docker
        if self.docker:
            _dict["docker"] = self.docker.to_dict()
        # override the default output from pydantic by calling `to_dict()` of git
        if self.git:
            _dict["git"] = self.git.to_dict()
        # override the default output from pydantic by calling `to_dict()` of database
        if self.database:
            _dict["database"] = self.database.to_dict()
        # override the default output from pydantic by calling `to_dict()` of archive
        if self.archive:
            _dict["archive"] = self.archive.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DeploymentDefinition from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "name": obj.get("name"),
                "type": obj.get("type")
                if obj.get("type") is not None
                else DeploymentDefinitionType.INVALID,
                "strategy": DeploymentStrategy.from_dict(obj["strategy"])
                if obj.get("strategy") is not None
                else None,
                "routes": [DeploymentRoute.from_dict(_item) for _item in obj["routes"]]
                if obj.get("routes") is not None
                else None,
                "ports": [DeploymentPort.from_dict(_item) for _item in obj["ports"]]
                if obj.get("ports") is not None
                else None,
                "proxy_ports": [
                    DeploymentProxyPort.from_dict(_item) for _item in obj["proxy_ports"]
                ]
                if obj.get("proxy_ports") is not None
                else None,
                "env": [DeploymentEnv.from_dict(_item) for _item in obj["env"]]
                if obj.get("env") is not None
                else None,
                "regions": obj.get("regions"),
                "scalings": [
                    DeploymentScaling.from_dict(_item) for _item in obj["scalings"]
                ]
                if obj.get("scalings") is not None
                else None,
                "instance_types": [
                    DeploymentInstanceType.from_dict(_item)
                    for _item in obj["instance_types"]
                ]
                if obj.get("instance_types") is not None
                else None,
                "health_checks": [
                    DeploymentHealthCheck.from_dict(_item)
                    for _item in obj["health_checks"]
                ]
                if obj.get("health_checks") is not None
                else None,
                "volumes": [
                    DeploymentVolume.from_dict(_item) for _item in obj["volumes"]
                ]
                if obj.get("volumes") is not None
                else None,
                "config_files": [
                    ConfigFile.from_dict(_item) for _item in obj["config_files"]
                ]
                if obj.get("config_files") is not None
                else None,
                "skip_cache": obj.get("skip_cache"),
                "mesh": obj.get("mesh")
                if obj.get("mesh") is not None
                else DeploymentMesh.DEPLOYMENT_MESH_AUTO,
                "network_policy": NetworkPolicy.from_dict(obj["network_policy"])
                if obj.get("network_policy") is not None
                else None,
                "docker": DockerSource.from_dict(obj["docker"])
                if obj.get("docker") is not None
                else None,
                "git": GitSource.from_dict(obj["git"])
                if obj.get("git") is not None
                else None,
                "database": DatabaseSource.from_dict(obj["database"])
                if obj.get("database") is not None
                else None,
                "archive": ArchiveSource.from_dict(obj["archive"])
                if obj.get("archive") is not None
                else None,
            }
        )
        return _obj
