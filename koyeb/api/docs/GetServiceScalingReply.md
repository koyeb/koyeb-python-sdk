# GetServiceScalingReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scalings** | [**List[ManualServiceScaling]**](ManualServiceScaling.md) |  | [optional] 

## Example

```python
from koyeb.api.models.get_service_scaling_reply import GetServiceScalingReply

# TODO update the JSON string below
json = "{}"
# create an instance of GetServiceScalingReply from a JSON string
get_service_scaling_reply_instance = GetServiceScalingReply.from_json(json)
# print the JSON string representation of the object
print(GetServiceScalingReply.to_json())

# convert the object into a dict
get_service_scaling_reply_dict = get_service_scaling_reply_instance.to_dict()
# create an instance of GetServiceScalingReply from a dict
get_service_scaling_reply_from_dict = GetServiceScalingReply.from_dict(get_service_scaling_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


