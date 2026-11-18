# Describe infrastructure with Terraform

Read infrastructure as code and interpret a Terraform plan. Learn which changes are easy to roll back and which require a migration.

**Supporting · 60 minutes** · **Prerequisites** [Map the application to Azure](../06-azure/architecture.md).

## The problem

A manually configured staging environment can drift from production. Terraform records infrastructure intent in configuration and compares it with the resources tracked in its state.

## Read a configuration excerpt

An Azure resource group provides a small example of a resource. This excerpt assumes the AzureRM provider is declared and authenticated, and the target subscription is selected.


```hcl
variable "location" {
  type = string
}

resource "azurerm_resource_group" "assistant" {
  name     = "rg-document-assistant-staging"
  location = var.location

  tags = {
    application = "document-assistant"
    environment = "staging"
  }
}
```


The provider translates resource and property definitions into Azure API calls. Terraform addresses this resource as `azurerm_resource_group.assistant`. Configuration is what you want. State maps Terraform addresses to real resources. A plan shows the candidate steps to reconcile them.

## Trace an environment change

Use `terraform fmt -check` to check formatting. In a configured workspace, `terraform init` prepares providers and the backend, and `terraform validate` checks configuration. `terraform plan` reads current infrastructure and proposes changes. A separate apply step changes resources. For an Azure lab, planning and applying need suitable subscription permissions and the resources created can incur charges.

Separate production and staging state and access. Remote state can be shared and locked. The AzureRM backend can store it in Azure Blob Storage. Limit who can read it because values marked sensitive can still appear there. Keep application settings in environment configuration and access secrets through a supported store such as Key Vault.

## Practice and debugging

A reviewer sees an update to tags and a replacement of the database. Identify which entry can affect customer data. For the replacement, inspect the changed property and provider explanation, then require a migration and recovery plan before applying. Determine whether an apparent creation instead comes from using the wrong state backend or environment.

## In production

Pin the provider version you validate and commit its lockfile. Review changes in the same environment and identity that will apply them. Assign one owner for each mutable property across Terraform and the release pipeline so the next apply does not undo a release.

## Recap and next step

You can explain what Terraform plans, where state lives, and why a replacement deserves a separate review. [Next: Test, promote and roll back releases](releases.md)

[Terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan), [AzureRM backend](https://developer.hashicorp.com/terraform/language/backend/azurerm)
