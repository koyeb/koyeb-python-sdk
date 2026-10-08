# DockerDeploymentMetadata

Image metadata resolved at provisioning time for docker-source deployments without an explicit command.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resolved_digest** | **str** | Digest of the resolved image manifest (\&quot;sha256:...\&quot;). | [optional] 
**resolved_entrypoint** | **List[str]** | ENTRYPOINT from the image config. | [optional] 
**resolved_cmd** | **List[str]** | CMD from the image config. | [optional] 

## Example

```python
from koyeb.api.models.docker_deployment_metadata import DockerDeploymentMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of DockerDeploymentMetadata from a JSON string
docker_deployment_metadata_instance = DockerDeploymentMetadata.from_json(json)
# print the JSON string representation of the object
print(DockerDeploymentMetadata.to_json())

# convert the object into a dict
docker_deployment_metadata_dict = docker_deployment_metadata_instance.to_dict()
# create an instance of DockerDeploymentMetadata from a dict
docker_deployment_metadata_from_dict = DockerDeploymentMetadata.from_dict(docker_deployment_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


