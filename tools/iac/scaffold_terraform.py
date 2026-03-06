"""
Tool: Terraform Module Scaffolder
Purpose: Generate Terraform or Bicep module directory structures with boilerplate files

Creates properly structured IaC module directories following best practices:
pinned providers, typed variables, documented outputs, README per module.

Usage:
    python tools/iac/scaffold_terraform.py --modules networking,compute,database --provider aws --output ./infrastructure
    python tools/iac/scaffold_terraform.py --modules networking,compute --provider azure --output ./infrastructure
    python tools/iac/scaffold_terraform.py --modules networking --provider aws --output ./infrastructure --environments dev,staging,prod

Dependencies:
    - json (stdlib)
    - argparse (stdlib)

Output:
    Directory structure with Terraform/Bicep scaffold files
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path


AWS_PROVIDER_BLOCK = '''terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
'''

AZURE_PROVIDER_BLOCK = '''terraform {
  required_version = ">= 1.5.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}
'''

MODULE_TEMPLATES = {
    "networking": {
        "aws": {
            "main.tf": '''# Networking Module - AWS
# Creates VPC, subnets, route tables, internet gateway, NAT gateway

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(var.tags, {
    Name = "${{var.project_name}}-vpc"
  })
}

# TODO: Add subnets, route tables, NAT gateway, internet gateway
# This is a scaffold - implement per architecture specification
''',
            "variables.tf": '''variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

variable "tags" {
  description = "Common tags applied to all resources"
  type        = map(string)
  default     = {}
}
''',
            "outputs.tf": '''output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}
''',
        },
        "azure": {
            "main.tf": '''# Networking Module - Azure
# Creates Virtual Network, subnets, NSGs

resource "azurerm_virtual_network" "main" {
  name                = "${{var.project_name}}-vnet"
  resource_group_name = var.resource_group_name
  location            = var.location
  address_space       = [var.vnet_cidr]

  tags = var.tags
}

# TODO: Add subnets, NSGs, route tables
# This is a scaffold - implement per architecture specification
''',
            "variables.tf": '''variable "vnet_cidr" {
  description = "Address space for the Virtual Network"
  type        = string
  default     = "10.0.0.0/16"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

variable "tags" {
  description = "Common tags applied to all resources"
  type        = map(string)
  default     = {}
}
''',
            "outputs.tf": '''output "vnet_id" {
  description = "ID of the Virtual Network"
  value       = azurerm_virtual_network.main.id
}

output "vnet_name" {
  description = "Name of the Virtual Network"
  value       = azurerm_virtual_network.main.name
}
''',
        },
    },
}

# Generic scaffold for modules not in the template library
GENERIC_MAIN = '''# {module_name} Module - {provider}
# TODO: Implement resources per architecture specification
# This is a scaffold - add resources, data sources, and locals as needed
'''

GENERIC_VARIABLES = '''variable "project_name" {{
  description = "Project name for resource naming"
  type        = string
}}

variable "environment" {{
  description = "Environment name (dev, staging, prod)"
  type        = string
}}

variable "tags" {{
  description = "Common tags applied to all resources"
  type        = map(string)
  default     = {{}}
}}
'''

GENERIC_OUTPUTS = '''# Outputs
# TODO: Add outputs for resource IDs, ARNs, endpoints that downstream modules need
'''


def scaffold_module(module_name: str, provider: str, base_path: Path) -> dict:
    """Create a single Terraform module directory with scaffold files."""
    module_path = base_path / "modules" / module_name
    module_path.mkdir(parents=True, exist_ok=True)

    files_created = []
    provider_block = AWS_PROVIDER_BLOCK if provider == "aws" else AZURE_PROVIDER_BLOCK

    # Check for specific template
    template = MODULE_TEMPLATES.get(module_name, {}).get(provider)

    if template:
        for filename, content in template.items():
            filepath = module_path / filename
            filepath.write_text(content, encoding="utf-8")
            files_created.append(str(filepath))
    else:
        # Generic scaffold
        (module_path / "main.tf").write_text(
            GENERIC_MAIN.format(module_name=module_name.title(), provider=provider.upper()),
            encoding="utf-8"
        )
        (module_path / "variables.tf").write_text(
            GENERIC_VARIABLES.format(), encoding="utf-8"
        )
        (module_path / "outputs.tf").write_text(GENERIC_OUTPUTS, encoding="utf-8")
        files_created.extend([
            str(module_path / "main.tf"),
            str(module_path / "variables.tf"),
            str(module_path / "outputs.tf"),
        ])

    # Always add versions.tf and README
    (module_path / "versions.tf").write_text(provider_block, encoding="utf-8")
    files_created.append(str(module_path / "versions.tf"))

    readme_content = f"""# {module_name.title()} Module

## Purpose

{module_name.title()} infrastructure resources for {provider.upper()}.

## Usage

```hcl
module "{module_name}" {{
  source = "../modules/{module_name}"

  project_name = var.project_name
  environment  = var.environment
  tags         = var.tags
}}
```

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|----------|
| `project_name` | Project name for resource naming | string | yes |
| `environment` | Environment name | string | yes |
| `tags` | Common tags | map(string) | no |

## Outputs

| Name | Description |
|------|-------------|
| (see outputs.tf) | |

---

*Generated: {datetime.now().strftime('%Y-%m-%d')}*
"""
    (module_path / "README.md").write_text(readme_content, encoding="utf-8")
    files_created.append(str(module_path / "README.md"))

    return {"module": module_name, "path": str(module_path), "files": files_created}


def scaffold_environment(env_name: str, modules: list, provider: str, base_path: Path) -> dict:
    """Create an environment directory with root module configuration."""
    env_path = base_path / "environments" / env_name
    env_path.mkdir(parents=True, exist_ok=True)

    files_created = []

    # main.tf - root module calling child modules
    main_lines = [f"# {env_name.title()} Environment", ""]
    for mod in modules:
        main_lines.append(f'module "{mod}" {{')
        main_lines.append(f'  source = "../../modules/{mod}"')
        main_lines.append("")
        main_lines.append(f"  project_name = var.project_name")
        main_lines.append(f"  environment  = var.environment")
        main_lines.append(f"  tags         = var.tags")
        main_lines.append("}")
        main_lines.append("")

    (env_path / "main.tf").write_text("\n".join(main_lines), encoding="utf-8")
    files_created.append(str(env_path / "main.tf"))

    # terraform.tfvars
    tfvars = f'''project_name = "my-project"
environment  = "{env_name}"

tags = {{
  Environment = "{env_name}"
  ManagedBy   = "terraform"
  Project     = "my-project"
}}
'''
    (env_path / "terraform.tfvars").write_text(tfvars, encoding="utf-8")
    files_created.append(str(env_path / "terraform.tfvars"))

    # backend.tf
    if provider == "aws":
        backend = f'''terraform {{
  backend "s3" {{
    bucket         = "my-project-terraform-state"
    key            = "{env_name}/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "my-project-terraform-locks"
    encrypt        = true
  }}
}}
'''
    else:
        backend = f'''terraform {{
  backend "azurerm" {{
    resource_group_name  = "my-project-tfstate-rg"
    storage_account_name = "myprojecttfstate"
    container_name       = "tfstate"
    key                  = "{env_name}.terraform.tfstate"
  }}
}}
'''
    (env_path / "backend.tf").write_text(backend, encoding="utf-8")
    files_created.append(str(env_path / "backend.tf"))

    # variables.tf for root
    root_vars = '''variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "tags" {
  description = "Common tags"
  type        = map(string)
  default     = {}
}
'''
    (env_path / "variables.tf").write_text(root_vars, encoding="utf-8")
    files_created.append(str(env_path / "variables.tf"))

    return {"environment": env_name, "path": str(env_path), "files": files_created}


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold Terraform module directory structures with boilerplate files"
    )
    parser.add_argument(
        "--modules", "-m", required=True,
        help="Comma-separated list of module names (e.g., networking,compute,database)"
    )
    parser.add_argument(
        "--provider", "-p",
        choices=["aws", "azure"],
        default="aws",
        help="Cloud provider (default: aws)"
    )
    parser.add_argument(
        "--output", "-o", required=True,
        help="Base output directory for the infrastructure scaffold"
    )
    parser.add_argument(
        "--environments", "-e",
        default="",
        help="Comma-separated environment names (e.g., dev,staging,prod). If empty, no environment dirs created."
    )

    args = parser.parse_args()

    modules = [m.strip() for m in args.modules.split(",") if m.strip()]
    environments = [e.strip() for e in args.environments.split(",") if e.strip()] if args.environments else []
    base_path = Path(args.output)

    results = {"modules": [], "environments": [], "files_created": 0}

    # Scaffold modules
    for mod in modules:
        result = scaffold_module(mod, args.provider, base_path)
        results["modules"].append(result)
        results["files_created"] += len(result["files"])

    # Scaffold environments
    for env in environments:
        result = scaffold_environment(env, modules, args.provider, base_path)
        results["environments"].append(result)
        results["files_created"] += len(result["files"])

    # Root README
    readme = f"""# Infrastructure - {args.provider.upper()}

## Modules

{chr(10).join(f"- `modules/{m}/` - {m.title()} resources" for m in modules)}

## Environments

{chr(10).join(f"- `environments/{e}/`" for e in environments) if environments else "- (none scaffolded)"}

## Usage

```bash
cd environments/dev
terraform init
terraform plan
terraform apply
```

---

*Generated: {datetime.now().strftime('%Y-%m-%d')}*
"""
    (base_path / "README.md").write_text(readme, encoding="utf-8")
    results["files_created"] += 1

    print(json.dumps({"success": True, "data": results}, indent=2))


if __name__ == "__main__":
    main()
