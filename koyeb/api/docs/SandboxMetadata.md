# SandboxMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**public_url** | **str** |  | [optional] 
**routing_key** | **str** |  | [optional] 

## Example

```python
from koyeb.api.models.sandbox_metadata import SandboxMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of SandboxMetadata from a JSON string
sandbox_metadata_instance = SandboxMetadata.from_json(json)
# print the JSON string representation of the object
print(SandboxMetadata.to_json())

# convert the object into a dict
sandbox_metadata_dict = sandbox_metadata_instance.to_dict()
# create an instance of SandboxMetadata from a dict
sandbox_metadata_from_dict = SandboxMetadata.from_dict(sandbox_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


