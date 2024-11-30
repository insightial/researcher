# Terraform Infrastructure Setup

This directory contains the Terraform configuration files for setting up the infrastructure for the Researcher project. The infrastructure is divided into several modules, each responsible for a specific part of the architecture.

## Main Configuration Files

- **[main.tf](./main.tf)**: This file defines the main Terraform configuration, including the backend configuration for storing the Terraform state in an S3 bucket. It also includes the module declarations for Cognito, S3, and Aurora.

- **[data.tf](./data.tf)**: Contains data sources to fetch information about the current AWS caller identity and region.

- **[config.tf](./config.tf)**: Specifies the required providers and configures the AWS provider with necessary credentials and region.

- **[networking.tf](./networking.tf)**: Defines the networking resources, including VPC, subnets, security groups, internet gateway, and route tables.

- **[variables.tf](./variables.tf)**: Declares the input variables used across the Terraform configuration, such as AWS credentials, region, and database details.

## Modules

### Aurora Module

Located in `modules/aurora`, this module is responsible for setting up the Aurora database cluster.

- **[user_db.tf](./modules/aurora/user_db.tf)**: (Currently commented out) Defines the AWS RDS Aurora cluster configuration, including engine type, scaling configuration, and security settings.

- **[variables.tf](./modules/aurora/variables.tf)**: Declares variables specific to the Aurora module, such as database name, username, password, subnet group name, and security group IDs.

### S3 Module

Located in `modules/s3`, this module manages the S3 bucket configuration.

- **[researcher.tf](./modules/s3/researcher.tf)**: Configures the S3 bucket with versioning, server-side encryption, lifecycle rules, and ownership controls.

- **[output.tf](./modules/s3/output.tf)**: Outputs the bucket name, ARN, and ID for use in other parts of the infrastructure.

### Cognito Module

Located in `modules/cognito`, this module sets up the Cognito user pool and client.

- **[researcher_user_pool.tf](./modules/cognito/researcher_user_pool.tf)**: Configures the Cognito user pool with alias attributes, password policy, and verification settings.

- **[researcher_user_pool_client.tf](./modules/cognito/researcher_user_pool_client.tf)**: Sets up the Cognito user pool client with authentication flows.

- **[output.tf](./modules/cognito/output.tf)**: Outputs the user pool ID, ARN, and client ID for integration with other services.

## Outputs

- **[output.tf](./output.tf)**: Provides outputs for the Cognito user pool and client IDs, which can be used by other components or services that need to interact with the Cognito service.

## Usage

1. Ensure you have Terraform installed and configured with your AWS credentials.
2. Initialize the Terraform configuration:
   ```bash
   terraform init
   ```
3. Plan the infrastructure changes:
   ```bash
   terraform plan
   ```
4. Apply the changes to set up the infrastructure:
   ```bash
   terraform apply
   ```

## Notes

- Ensure that the AWS credentials provided have the necessary permissions to create and manage the resources defined in this configuration.
- The Aurora module's RDS cluster resource is currently commented out. Uncomment and configure it as needed for your environment.

This setup is designed for the Researcher project and may need adjustments for other environments or projects.
