# Region


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**coordinates** | **List[str]** |  | [optional] 
**status** | **str** |  | [optional] 
**instances** | **List[str]** |  | [optional] 
**datacenters** | **List[str]** |  | [optional] 
**volumes_enabled** | **bool** |  | [optional] 
**scope** | **str** | The scope of the region, continent, metropolitan area, etc. | [optional] 
**container_runtimes** | **List[str]** | The container runtimes available in this region, in catalog order (the first one is the region default). Only populated when the runtime-choice feature is enabled. | [optional] 

## Example

```python
from koyeb.api.models.region import Region

# TODO update the JSON string below
json = "{}"
# create an instance of Region from a JSON string
region_instance = Region.from_json(json)
# print the JSON string representation of the object
print(Region.to_json())

# convert the object into a dict
region_dict = region_instance.to_dict()
# create an instance of Region from a dict
region_from_dict = Region.from_dict(region_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


