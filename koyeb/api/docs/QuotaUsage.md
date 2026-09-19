# QuotaUsage

QuotaUsage carries an organization's current resource consumption alongside the corresponding plan limits (from the caller's InternalToken.Quotas). Paused services are included in services_used but excluded from memory / instances_by_type / proxy_ports totals, matching enforcement semantics.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**apps_used** | **int** |  | [optional] 
**apps_limit** | **int** |  | [optional] 
**services_used** | **int** |  | [optional] 
**services_limit** | **int** |  | [optional] 
**memory_mb_used** | **int** |  | [optional] 
**memory_mb_limit** | **int** |  | [optional] 
**custom_domains_used** | **int** |  | [optional] 
**custom_domains_limit** | **int** |  | [optional] 
**koyeb_lb_domains_used** | **int** |  | [optional] 
**koyeb_lb_domains_limit** | **int** |  | [optional] 
**proxy_ports_used** | **int** |  | [optional] 
**proxy_ports_limit** | **int** |  | [optional] 
**instances_by_type** | [**List[InstanceTypeUsage]**](InstanceTypeUsage.md) |  | [optional] 
**persistent_volumes_by_region** | [**List[PersistentVolumeRegionUsage]**](PersistentVolumeRegionUsage.md) |  | [optional] 
**instance_snapshots_by_type** | [**List[InstanceSnapshotTypeUsage]**](InstanceSnapshotTypeUsage.md) |  | [optional] 

## Example

```python
from koyeb.api.models.quota_usage import QuotaUsage

# TODO update the JSON string below
json = "{}"
# create an instance of QuotaUsage from a JSON string
quota_usage_instance = QuotaUsage.from_json(json)
# print the JSON string representation of the object
print(QuotaUsage.to_json())

# convert the object into a dict
quota_usage_dict = quota_usage_instance.to_dict()
# create an instance of QuotaUsage from a dict
quota_usage_from_dict = QuotaUsage.from_dict(quota_usage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


