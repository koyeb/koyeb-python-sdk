# Mesh

Mesh groups the mesh scope selector and the (optional) custom mesh name. Kept inside NetworkPolicy so scope/name and other network-policy dimensions (egress, future inbound) live together.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scope** | [**MeshScope**](MeshScope.md) |  | [optional] [default to MeshScope.MESH_SCOPE_UNSPECIFIED]
**name** | **str** | Custom mesh name — required when scope is MESH_SCOPE_CUSTOM, ignored otherwise. Combined with the workspace ID server-side to ensure the same custom name in different workspaces never collides. | [optional] 

## Example

```python
from koyeb.api_async.models.mesh import Mesh

# TODO update the JSON string below
json = "{}"
# create an instance of Mesh from a JSON string
mesh_instance = Mesh.from_json(json)
# print the JSON string representation of the object
print(Mesh.to_json())

# convert the object into a dict
mesh_dict = mesh_instance.to_dict()
# create an instance of Mesh from a dict
mesh_from_dict = Mesh.from_dict(mesh_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


