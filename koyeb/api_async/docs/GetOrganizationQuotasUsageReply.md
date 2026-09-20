# GetOrganizationQuotasUsageReply


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**usage** | [**QuotaUsage**](QuotaUsage.md) |  | [optional] 

## Example

```python
from koyeb.api_async.models.get_organization_quotas_usage_reply import GetOrganizationQuotasUsageReply

# TODO update the JSON string below
json = "{}"
# create an instance of GetOrganizationQuotasUsageReply from a JSON string
get_organization_quotas_usage_reply_instance = GetOrganizationQuotasUsageReply.from_json(json)
# print the JSON string representation of the object
print(GetOrganizationQuotasUsageReply.to_json())

# convert the object into a dict
get_organization_quotas_usage_reply_dict = get_organization_quotas_usage_reply_instance.to_dict()
# create an instance of GetOrganizationQuotasUsageReply from a dict
get_organization_quotas_usage_reply_from_dict = GetOrganizationQuotasUsageReply.from_dict(get_organization_quotas_usage_reply_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


