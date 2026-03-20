# UpdateOrganizationDefaultProjectRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**default_project_id** | **str** |  | [optional] 

## Example

```python
from koyeb.api.models.update_organization_default_project_request import UpdateOrganizationDefaultProjectRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateOrganizationDefaultProjectRequest from a JSON string
update_organization_default_project_request_instance = UpdateOrganizationDefaultProjectRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateOrganizationDefaultProjectRequest.to_json())

# convert the object into a dict
update_organization_default_project_request_dict = update_organization_default_project_request_instance.to_dict()
# create an instance of UpdateOrganizationDefaultProjectRequest from a dict
update_organization_default_project_request_from_dict = UpdateOrganizationDefaultProjectRequest.from_dict(update_organization_default_project_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


