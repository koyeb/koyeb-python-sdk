# ClearIdenfyVerificationResultRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **str** |  | [optional] 
**organization_id** | **str** |  | [optional] 

## Example

```python
from koyeb.api_async.models.clear_idenfy_verification_result_request import ClearIdenfyVerificationResultRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ClearIdenfyVerificationResultRequest from a JSON string
clear_idenfy_verification_result_request_instance = ClearIdenfyVerificationResultRequest.from_json(json)
# print the JSON string representation of the object
print(ClearIdenfyVerificationResultRequest.to_json())

# convert the object into a dict
clear_idenfy_verification_result_request_dict = clear_idenfy_verification_result_request_instance.to_dict()
# create an instance of ClearIdenfyVerificationResultRequest from a dict
clear_idenfy_verification_result_request_from_dict = ClearIdenfyVerificationResultRequest.from_dict(clear_idenfy_verification_result_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


