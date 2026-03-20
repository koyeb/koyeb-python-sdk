# UpdateServiceScalingRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scalings** | [**List[ManualServiceScaling]**](ManualServiceScaling.md) |  | [optional] 

## Example

```python
from koyeb.api.models.update_service_scaling_request import UpdateServiceScalingRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateServiceScalingRequest from a JSON string
update_service_scaling_request_instance = UpdateServiceScalingRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateServiceScalingRequest.to_json())

# convert the object into a dict
update_service_scaling_request_dict = update_service_scaling_request_instance.to_dict()
# create an instance of UpdateServiceScalingRequest from a dict
update_service_scaling_request_from_dict = UpdateServiceScalingRequest.from_dict(update_service_scaling_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


