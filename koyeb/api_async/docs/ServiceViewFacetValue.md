# ServiceViewFacetValue


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **str** |  | [optional] 
**label** | **str** |  | [optional] 
**count** | **int** |  | [optional] 

## Example

```python
from koyeb.api_async.models.service_view_facet_value import ServiceViewFacetValue

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceViewFacetValue from a JSON string
service_view_facet_value_instance = ServiceViewFacetValue.from_json(json)
# print the JSON string representation of the object
print(ServiceViewFacetValue.to_json())

# convert the object into a dict
service_view_facet_value_dict = service_view_facet_value_instance.to_dict()
# create an instance of ServiceViewFacetValue from a dict
service_view_facet_value_from_dict = ServiceViewFacetValue.from_dict(service_view_facet_value_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


