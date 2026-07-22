# InstanceSnapshotQuotas


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**filesystem** | **int** |  | [optional] 
**full** | **int** |  | [optional] 

## Example

```python
from koyeb.api.models.instance_snapshot_quotas import InstanceSnapshotQuotas

# TODO update the JSON string below
json = "{}"
# create an instance of InstanceSnapshotQuotas from a JSON string
instance_snapshot_quotas_instance = InstanceSnapshotQuotas.from_json(json)
# print the JSON string representation of the object
print(InstanceSnapshotQuotas.to_json())

# convert the object into a dict
instance_snapshot_quotas_dict = instance_snapshot_quotas_instance.to_dict()
# create an instance of InstanceSnapshotQuotas from a dict
instance_snapshot_quotas_from_dict = InstanceSnapshotQuotas.from_dict(instance_snapshot_quotas_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


