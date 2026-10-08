# GRPCHealthCheck


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**port** | **int** |  | [optional] 
**service** | **str** |  | [optional] 

## Example

```python
from koyeb.api_async.models.grpc_health_check import GRPCHealthCheck

# TODO update the JSON string below
json = "{}"
# create an instance of GRPCHealthCheck from a JSON string
grpc_health_check_instance = GRPCHealthCheck.from_json(json)
# print the JSON string representation of the object
print(GRPCHealthCheck.to_json())

# convert the object into a dict
grpc_health_check_dict = grpc_health_check_instance.to_dict()
# create an instance of GRPCHealthCheck from a dict
grpc_health_check_from_dict = GRPCHealthCheck.from_dict(grpc_health_check_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


