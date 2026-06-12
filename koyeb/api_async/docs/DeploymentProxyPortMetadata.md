# DeploymentProxyPortMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**host** | **str** |  | [optional] 
**public_port** | **int** |  | [optional] 
**port** | **int** |  | [optional] 
**protocol** | [**ProxyPortProtocol**](ProxyPortProtocol.md) |  | [optional] [default to ProxyPortProtocol.TCP]

## Example

```python
from koyeb.api_async.models.deployment_proxy_port_metadata import DeploymentProxyPortMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of DeploymentProxyPortMetadata from a JSON string
deployment_proxy_port_metadata_instance = DeploymentProxyPortMetadata.from_json(json)
# print the JSON string representation of the object
print(DeploymentProxyPortMetadata.to_json())

# convert the object into a dict
deployment_proxy_port_metadata_dict = deployment_proxy_port_metadata_instance.to_dict()
# create an instance of DeploymentProxyPortMetadata from a dict
deployment_proxy_port_metadata_from_dict = DeploymentProxyPortMetadata.from_dict(deployment_proxy_port_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


