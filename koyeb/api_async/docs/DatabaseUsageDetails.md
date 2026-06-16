# DatabaseUsageDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**organization_id** | **str** |  | [optional] 
**app_id** | **str** |  | [optional] 
**app_name** | **str** |  | [optional] 
**service_id** | **str** |  | [optional] 
**service_name** | **str** |  | [optional] 
**compute_time_seconds** | **int** |  | [optional] 
**data_storage_megabytes_hour** | **int** |  | [optional] 
**started_at** | **datetime** |  | [optional] 
**terminated_at** | **datetime** |  | [optional] 

## Example

```python
from koyeb.api_async.models.database_usage_details import DatabaseUsageDetails

# TODO update the JSON string below
json = "{}"
# create an instance of DatabaseUsageDetails from a JSON string
database_usage_details_instance = DatabaseUsageDetails.from_json(json)
# print the JSON string representation of the object
print(DatabaseUsageDetails.to_json())

# convert the object into a dict
database_usage_details_dict = database_usage_details_instance.to_dict()
# create an instance of DatabaseUsageDetails from a dict
database_usage_details_from_dict = DatabaseUsageDetails.from_dict(database_usage_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


