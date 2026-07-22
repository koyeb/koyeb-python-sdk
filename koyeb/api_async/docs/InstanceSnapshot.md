# InstanceSnapshot


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**available_at** | **datetime** |  | [optional] 
**deleted_at** | **datetime** |  | [optional] 
**organization_id** | **str** |  | [optional] 
**project_id** | **str** |  | [optional] 
**service_id** | **str** |  | [optional] 
**deployment_id** | **str** |  | [optional] 
**regional_deployment_id** | **str** |  | [optional] 
**instance_id** | **str** |  | [optional] 
**status** | [**InstanceSnapshotStatus**](InstanceSnapshotStatus.md) |  | [optional] [default to InstanceSnapshotStatus.INSTANCE_SNAPSHOT_STATUS_INVALID]
**type** | [**InstanceSnapshotType**](InstanceSnapshotType.md) |  | [optional] [default to InstanceSnapshotType.INSTANCE_SNAPSHOT_TYPE_INVALID]
**version** | **str** |  | [optional] 
**messages** | **List[str]** |  | [optional] 

## Example

```python
from koyeb.api_async.models.instance_snapshot import InstanceSnapshot

# TODO update the JSON string below
json = "{}"
# create an instance of InstanceSnapshot from a JSON string
instance_snapshot_instance = InstanceSnapshot.from_json(json)
# print the JSON string representation of the object
print(InstanceSnapshot.to_json())

# convert the object into a dict
instance_snapshot_dict = instance_snapshot_instance.to_dict()
# create an instance of InstanceSnapshot from a dict
instance_snapshot_from_dict = InstanceSnapshot.from_dict(instance_snapshot_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


