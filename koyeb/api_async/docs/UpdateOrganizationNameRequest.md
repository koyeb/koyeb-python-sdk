# UpdateOrganizationNameRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 

## Example

```python
from koyeb.api_async.models.update_organization_name_request import UpdateOrganizationNameRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateOrganizationNameRequest from a JSON string
update_organization_name_request_instance = UpdateOrganizationNameRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateOrganizationNameRequest.to_json())

# convert the object into a dict
update_organization_name_request_dict = update_organization_name_request_instance.to_dict()
# create an instance of UpdateOrganizationNameRequest from a dict
update_organization_name_request_from_dict = UpdateOrganizationNameRequest.from_dict(update_organization_name_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


