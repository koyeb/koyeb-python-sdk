# DeploymentProxyPort


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**port** | **int** |  | [optional] 
**protocol** | [**ProxyPortProtocol**](ProxyPortProtocol.md) |  | [optional] [default to ProxyPortProtocol.TCP]

## Example

```python
from koyeb.api_async.models.deployment_proxy_port import DeploymentProxyPort

# TODO update the JSON string below
json = "{}"
# create an instance of DeploymentProxyPort from a JSON string
deployment_proxy_port_instance = DeploymentProxyPort.from_json(json)
# print the JSON string representation of the object
print(DeploymentProxyPort.to_json())

# convert the object into a dict
deployment_proxy_port_dict = deployment_proxy_port_instance.to_dict()
# create an instance of DeploymentProxyPort from a dict
deployment_proxy_port_from_dict = DeploymentProxyPort.from_dict(deployment_proxy_port_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


