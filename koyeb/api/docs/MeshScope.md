# MeshScope

MeshScope selects which set of services can communicate over the mesh. Only meaningful when the mesh is on (i.e. DeploymentMesh is ENABLED, or AUTO and the service is eligible). UNSPECIFIED defers to the organization-level default (workspace-scoped since KOYEB-6062, legacy organizations opted back to organization scope via use_organization_level_mesh).   - MESH_SCOPE_ORGANIZATION: Private communication between services in the same organization (mesh label k-<orgId>).  - MESH_SCOPE_WORKSPACE: Private communication between services in the same workspace/project (mesh label pr_<projectId>).  - MESH_SCOPE_APP: Private communication between services in the same app (mesh label app_<appId>).  - MESH_SCOPE_CUSTOM: Private communication between services in the same workspace that share the same NetworkPolicy.mesh.name. Server-computed label is scoped by workspace, so the same custom name in different workspaces never collides.

## Enum

* `MESH_SCOPE_UNSPECIFIED` (value: `'MESH_SCOPE_UNSPECIFIED'`)

* `MESH_SCOPE_ORGANIZATION` (value: `'MESH_SCOPE_ORGANIZATION'`)

* `MESH_SCOPE_WORKSPACE` (value: `'MESH_SCOPE_WORKSPACE'`)

* `MESH_SCOPE_APP` (value: `'MESH_SCOPE_APP'`)

* `MESH_SCOPE_CUSTOM` (value: `'MESH_SCOPE_CUSTOM'`)

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


