# GetDeploymentScalingReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**replicas** | [**List[GetDeploymentScalingReplyItem]**](GetDeploymentScalingReplyItem.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.get_deployment_scaling_reply import GetDeploymentScalingReply

# TODO update the JSON string below
json = "{}"
# create an instance of GetDeploymentScalingReply from a JSON string
get_deployment_scaling_reply_instance = GetDeploymentScalingReply.from_json(json)
# print the JSON string representation of the object
print(GetDeploymentScalingReply.to_json())

# convert the object into a dict
get_deployment_scaling_reply_dict = get_deployment_scaling_reply_instance.to_dict()
# create an instance of GetDeploymentScalingReply from a dict
get_deployment_scaling_reply_from_dict = GetDeploymentScalingReply.from_dict(get_deployment_scaling_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


