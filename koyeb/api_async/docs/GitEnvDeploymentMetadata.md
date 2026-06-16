# GitEnvDeploymentMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sha** | **str** |  | [optional] 
**commit_author** | **str** |  | [optional] 
**commit_message** | **str** |  | [optional] 

## Example

```python
from koyeb.api_async.models.git_env_deployment_metadata import GitEnvDeploymentMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of GitEnvDeploymentMetadata from a JSON string
git_env_deployment_metadata_instance = GitEnvDeploymentMetadata.from_json(json)
# print the JSON string representation of the object
print(GitEnvDeploymentMetadata.to_json())

# convert the object into a dict
git_env_deployment_metadata_dict = git_env_deployment_metadata_instance.to_dict()
# create an instance of GitEnvDeploymentMetadata from a dict
git_env_deployment_metadata_from_dict = GitEnvDeploymentMetadata.from_dict(git_env_deployment_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


