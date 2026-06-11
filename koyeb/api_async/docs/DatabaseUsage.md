# DatabaseUsage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**service_id** | **str** |  | [optional] 
**service_name** | **str** |  | [optional] 
**compute_time_seconds** | **int** |  | [optional] 
**data_storage_megabytes_hours** | **int** |  | [optional] 

## Example

```python
from koyeb.api_async.models.database_usage import DatabaseUsage

# TODO update the JSON string below
json = "{}"
# create an instance of DatabaseUsage from a JSON string
database_usage_instance = DatabaseUsage.from_json(json)
# print the JSON string representation of the object
print(DatabaseUsage.to_json())

# convert the object into a dict
database_usage_dict = database_usage_instance.to_dict()
# create an instance of DatabaseUsage from a dict
database_usage_from_dict = DatabaseUsage.from_dict(database_usage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


