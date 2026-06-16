# GetDeploymentScalingReplyItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**region** | **str** |  | [optional] 
**replica_index** | **int** |  | [optional] 
**instances** | [**List[Instance]**](Instance.md) | An array of &#x60;active&#x60; and &#x60;starting&#x60; instances.  Status of the active instance (and if none the most recent instance)  string status &#x3D; 4;  Status message of the active instance (and if none the most recent instance)  string message &#x3D; 5; | [optional] 

## Example

```python
from koyeb.api_async.models.get_deployment_scaling_reply_item import GetDeploymentScalingReplyItem

# TODO update the JSON string below
json = "{}"
# create an instance of GetDeploymentScalingReplyItem from a JSON string
get_deployment_scaling_reply_item_instance = GetDeploymentScalingReplyItem.from_json(json)
# print the JSON string representation of the object
print(GetDeploymentScalingReplyItem.to_json())

# convert the object into a dict
get_deployment_scaling_reply_item_dict = get_deployment_scaling_reply_item_instance.to_dict()
# create an instance of GetDeploymentScalingReplyItem from a dict
get_deployment_scaling_reply_item_from_dict = GetDeploymentScalingReplyItem.from_dict(get_deployment_scaling_reply_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


