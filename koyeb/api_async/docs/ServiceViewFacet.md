# ServiceViewFacet


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kind** | [**ServiceViewFacetKind**](ServiceViewFacetKind.md) |  | [optional] [default to ServiceViewFacetKind.TYPE]
**values** | [**List[ServiceViewFacetValue]**](ServiceViewFacetValue.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.service_view_facet import ServiceViewFacet

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceViewFacet from a JSON string
service_view_facet_instance = ServiceViewFacet.from_json(json)
# print the JSON string representation of the object
print(ServiceViewFacet.to_json())

# convert the object into a dict
service_view_facet_dict = service_view_facet_instance.to_dict()
# create an instance of ServiceViewFacet from a dict
service_view_facet_from_dict = ServiceViewFacet.from_dict(service_view_facet_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


