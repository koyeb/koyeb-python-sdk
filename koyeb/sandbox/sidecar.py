# coding: utf-8

"""
Sidecars: trusted helper services that run next to a sandbox.

A sidecar is a separate service, with its own image, env,
secrets and egress policy, that the sandbox reaches by name over a private
mesh (``http://<name>:<port>``). Secrets given to a sidecar never enter the
sandbox, so a sidecar can hold API keys, run a credential-injecting proxy,
or host a helper service the agent should use but not touch.

This module only describes sidecars and builds their service definitions.
The create, wait and delete flow lives with the sandbox.

Each sidecar runs as a web service with no public route, a TCP health check
on its first port, and the mesh enabled with app scope. Since the sandbox
owns its app, the app scope makes the mesh private to the sandbox and its
sidecars.

The ``Sidecar`` fields and the ``Sandbox`` sidecar API are stable. How
sidecars are hosted is not: today they are services in the sandbox's app,
which ``SidecarInfo.service_id`` and the ``KOYEB_SIDECARS`` env reflect and
which may change when the platform runs sidecars natively.
"""

from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

from koyeb.api.models.deployment_definition_type import DeploymentDefinitionType
from koyeb.api.models.deployment_health_check import DeploymentHealthCheck
from koyeb.api.models.deployment_port import DeploymentPort
from koyeb.api.models.mesh_scope import MeshScope
from koyeb.api.models.tcp_health_check import TCPHealthCheck

from .egress import build_egress_policy
from .errors import EgressPolicyError, SidecarError
from .spec import SandboxSpec

# A DNS label the API accepts as a service name: the sandbox reaches the
# sidecar at http://<name>:<port>. The API's slug rule allows no empty
# segment, so no "--" (and no "."; it would break the DNS name).
_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
_MIN_PORT, _MAX_PORT = 1, 64999  # the API reserves ports above 65000
_MAX_PORTS = 5
_MIN_GRACE, _MAX_GRACE = 5, 900  # API bounds for health check grace_period


@dataclass
class Sidecar:
    """A trusted helper service that runs next to a sandbox.

    Pass sidecars to ``Sandbox.create(sidecars=[...])``. The sandbox reaches
    each one at ``http://<name>:<port>`` over a private mesh.

    Args:
        name: DNS name the sandbox uses to reach the sidecar. Lowercase
            letters, digits and dashes, 2-63 characters.
        image: Docker image to run.
        ports: TCP ports the sidecar listens on (1-5). The first port is
            health-checked: the sandbox is created only once it accepts
            connections.
        instance_type: Instance type (default: nano).
        entrypoint: Override the image entrypoint.
        command: Override the image command.
        args: Arguments for the command.
        env: Environment variables. Use ``Secret(name=...)`` values so the
            platform injects secrets at deploy time; they never reach the
            sandbox.
        config_files: Files to mount, as ``{path: content}`` or
            ``{path: ConfigFile(...)}``.
        registry_secret: Secret holding registry credentials for a private
            image.
        privileged: Run the sidecar privileged (default: False), e.g. for a
            VPN client that needs /dev/net/tun. Honoured where a privileged
            sandbox is.
        startup_grace_period: Seconds the sidecar may take to start listening
            before failed health checks count (5-900, default: the platform's,
            5). The platform then allows about two more minutes. Raise it for
            images that install or configure things at boot.
        block_network: Block all outbound traffic from the sidecar.
        outbound_allowlist: IPs/CIDRs the sidecar may reach; everything else
            is blocked. Mutually exclusive with block_network. Entries must
            not overlap. With either option the sandbox can still reach the
            sidecar and get replies, but the sidecar can't open new
            connections to the sandbox.

    Example:
        >>> proxy = Sidecar(
        ...     name="proxy",
        ...     image="mitmproxy/mitmproxy:latest",
        ...     ports=[8080],
        ...     command="mitmdump",
        ...     args=["--listen-port", "8080"],
        ...     env={"API_KEY": Secret(name="my-api-key")},
        ... )
    """

    name: str
    image: str
    ports: List[int]
    instance_type: str = "nano"
    entrypoint: Optional[List[str]] = None
    command: Optional[str] = None
    args: Optional[List[str]] = None
    env: Optional[Dict[str, Any]] = None
    config_files: Optional[Dict[str, Any]] = None
    registry_secret: Optional[str] = None
    block_network: bool = False
    outbound_allowlist: Optional[List[str]] = None
    privileged: bool = False
    startup_grace_period: Optional[int] = None

    def __post_init__(self):
        _validate_name(self.name)
        if not isinstance(self.image, str) or not self.image:
            raise SidecarError(f"Sidecar '{self.name}': image is required")
        self.ports = _validate_ports(self.name, self.ports)
        grace = self.startup_grace_period
        if grace is not None and (
            isinstance(grace, bool)
            or not isinstance(grace, int)
            or not _MIN_GRACE <= grace <= _MAX_GRACE
        ):
            raise SidecarError(
                f"Sidecar '{self.name}': startup_grace_period must be an integer "
                f"between {_MIN_GRACE} and {_MAX_GRACE} seconds"
            )
        try:
            egress = build_egress_policy(self.block_network, self.outbound_allowlist)
        except EgressPolicyError as e:
            raise SidecarError(f"Sidecar '{self.name}': {e}") from e
        _check_disjoint(self.name, egress)

    def service_spec(
        self,
        region: Optional[str] = None,
        delete_after_delay: int = 0,
        delete_after_inactivity_delay: int = 0,
    ) -> SandboxSpec:
        """The service spec for this sidecar.

        A web service with no route (not public), a TCP health check on the
        first port, the mesh enabled with app scope, and no scale-to-zero:
        mesh traffic from the sandbox does not wake a sleeping service.
        ``region`` and the delete delays should match the sandbox's.
        """
        return SandboxSpec(
            name=self.name,
            image=self.image,
            instance_type=self.instance_type,
            definition_type=DeploymentDefinitionType.WEB,
            env=self.env,
            config_files=self.config_files,
            region=region,
            idle_timeout=0,
            registry_secret=self.registry_secret,
            privileged=self.privileged,
            delete_after_delay=delete_after_delay,
            delete_after_inactivity_delay=delete_after_inactivity_delay,
            enable_mesh=True,
            entrypoint=self.entrypoint,
            command=self.command,
            args=self.args,
            ports=[DeploymentPort(port=p, protocol="tcp") for p in self.ports],
            routes=[],
            block_network=self.block_network,
            outbound_allowlist=self.outbound_allowlist,
            mesh_scope=MeshScope.MESH_SCOPE_APP,
            health_checks=[
                DeploymentHealthCheck(
                    tcp=TCPHealthCheck(port=self.ports[0]),
                    grace_period=self.startup_grace_period,
                )
            ],
        )


def validate_sidecars(sidecars: Iterable[Sidecar], sandbox_name: str) -> List[Sidecar]:
    """Check a sandbox's sidecars as a set, before any API call.

    Names must be unique and differ from the sandbox's name: they share one
    app, and the sandbox reaches each sidecar by its service name.
    """
    sidecars = list(sidecars)
    seen = set()
    for sidecar in sidecars:
        if not isinstance(sidecar, Sidecar):
            raise SidecarError(f"Expected a Sidecar, got {type(sidecar).__name__}")
        if sidecar.name == sandbox_name:
            raise SidecarError(
                f"Sidecar name '{sidecar.name}' is the sandbox's name; pick another"
            )
        if sidecar.name in seen:
            raise SidecarError(f"Duplicate sidecar name '{sidecar.name}'")
        seen.add(sidecar.name)
    return sidecars


def _validate_name(name: Any) -> None:
    if (
        not isinstance(name, str)
        or not 2 <= len(name) <= 63
        or not _NAME_RE.fullmatch(name)
    ):
        raise SidecarError(
            f"Invalid sidecar name {name!r}: use 2-63 lowercase letters, digits "
            "and single dashes, starting and ending with a letter or digit"
        )


def _validate_ports(name: str, ports: Any) -> List[int]:
    if isinstance(ports, (str, bytes)) or not isinstance(ports, Iterable):
        raise SidecarError(f"Sidecar '{name}': ports must be a list of integers")
    ports = list(ports)
    if not 1 <= len(ports) <= _MAX_PORTS:
        raise SidecarError(
            f"Sidecar '{name}': declare between 1 and {_MAX_PORTS} ports"
        )
    for port in ports:
        if (
            isinstance(port, bool)
            or not isinstance(port, int)
            or not _MIN_PORT <= port <= _MAX_PORT
        ):
            raise SidecarError(
                f"Sidecar '{name}': port {port!r} must be an integer between "
                f"{_MIN_PORT} and {_MAX_PORT}"
            )
    if len(set(ports)) != len(ports):
        raise SidecarError(f"Sidecar '{name}': duplicate port")
    return ports


def _check_disjoint(name: str, egress: Any) -> None:
    """The API rejects overlapping allowlist entries; fail before creating
    anything."""
    nets = [
        ipaddress.ip_network(d.cidr)
        for d in (getattr(egress, "allow_list", None) or [])
    ]
    for i, a in enumerate(nets):
        for b in nets[i + 1 :]:
            if a.version == b.version and a.overlaps(b):
                raise SidecarError(
                    f"Sidecar '{name}': outbound_allowlist entries must not "
                    f"overlap ({a} and {b})"
                )
