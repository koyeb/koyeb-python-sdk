# InstanceSnapshotTypeUsage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**used** | **int** |  | [optional] 
**limit** | **int** |  | [optional] 

## Example

```python
from koyeb.api_async.models.instance_snapshot_type_usage import InstanceSnapshotTypeUsage

# TODO update the JSON string below
json = "{}"
# create an instance of InstanceSnapshotTypeUsage from a JSON string
instance_snapshot_type_usage_instance = InstanceSnapshotTypeUsage.from_json(json)
# print the JSON string representation of the object
print(InstanceSnapshotTypeUsage.to_json())

# convert the object into a dict
instance_snapshot_type_usage_dict = instance_snapshot_type_usage_instance.to_dict()
# create an instance of InstanceSnapshotTypeUsage from a dict
instance_snapshot_type_usage_from_dict = InstanceSnapshotTypeUsage.from_dict(instance_snapshot_type_usage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


