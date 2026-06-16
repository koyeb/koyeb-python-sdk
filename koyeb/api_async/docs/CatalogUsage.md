# CatalogUsage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**instances** | [**Dict[str, InstanceAvailability]**](InstanceAvailability.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.catalog_usage import CatalogUsage

# TODO update the JSON string below
json = "{}"
# create an instance of CatalogUsage from a JSON string
catalog_usage_instance = CatalogUsage.from_json(json)
# print the JSON string representation of the object
print(CatalogUsage.to_json())

# convert the object into a dict
catalog_usage_dict = catalog_usage_instance.to_dict()
# create an instance of CatalogUsage from a dict
catalog_usage_from_dict = CatalogUsage.from_dict(catalog_usage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


