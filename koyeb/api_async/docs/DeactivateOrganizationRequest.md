# DeactivateOrganizationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**skip_confirmation** | **bool** | if set to true, skip_confirmation will directly start the deactivation process, without sending a confirmation email beforehand. | [optional] 

## Example

```python
from koyeb.api_async.models.deactivate_organization_request import DeactivateOrganizationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DeactivateOrganizationRequest from a JSON string
deactivate_organization_request_instance = DeactivateOrganizationRequest.from_json(json)
# print the JSON string representation of the object
print(DeactivateOrganizationRequest.to_json())

# convert the object into a dict
deactivate_organization_request_dict = deactivate_organization_request_instance.to_dict()
# create an instance of DeactivateOrganizationRequest from a dict
deactivate_organization_request_from_dict = DeactivateOrganizationRequest.from_dict(deactivate_organization_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


