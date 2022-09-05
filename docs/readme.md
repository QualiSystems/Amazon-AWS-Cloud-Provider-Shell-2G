![Image][1]

# **Amazon AWS Cloud Provider Shell 2G**

Release date: December 2020

`Shell version: 1.0.0`

`Document version: 1.0`

# In This Guide

* [Overview](#overview)
* [Downloading the Shell](#downloading-the-shell)
* [Importing and Configuring the Shell](#importing-and-configuring-the-shell)
* [Updating Python Dependencies for Shells](#updating-python-dependencies-for-shells)
* [Typical Workflows](#typical-workflows)
* [References](#references)
* [Release Notes](#release-notes)


# Overview
A shell integrates a device model, application or other technology with CloudShell. 
A shell consists of a data model that defines how the device or service and its properties are modeled in CloudShell, alongside automation that enables interaction with the device or service via CloudShell.

### Cloud Provider Shells
CloudShell Cloud Providers shells provide the ability to provision Apps on a virtualization platform or a service provider platform.

The Apps can be modeled on a variety of types of services, depending on the Cloud Provider, including VMs, Containers, or Emulated instances.  

### Amazon AWS Cloud Provider Shell 2G
Amazon AWS Cloud Provider Shell 2G provides you with app deployment and management capabilities on AWS EC2. These include: 
* Pyhon 3.7 support
* Capability to deploy, manage and tear down AWS infrastructure as part of CloudShell sandboxes, including virtual networks, subnets, EC2 instances and security groups
* Option to deploy to existing shared VPC
* Enable source destination checks

For details, see the [Add an AWS Cloud Provider Resource](https://help.quali.com/Online%20Help/0.0/Portal/Content/Admn/VPC-AWS-Cld-Prvdr-Rsc.htm) CloudShell Help article. For more information on AWS, see the vendor's official product documentation.

### Standard version
Amazon AWS Cloud Provider Shell 2G is based on the Cloud Provider Standard version **1.0.0**.

For detailed information about the shell’s structure and attributes, see the [Cloud Provider Standard](https://github.com/QualiSystems/cloudshell-standards/blob/master/Documentation/cloud_provider_standard.md) in GitHub.

### Requirements

Release: Amazon AWS Cloud Provider Shell 2G

▪ CloudShell version **9.3 and above**

**Note:** If your CloudShell version does not support this shell, you should consider upgrading to a later version of CloudShell or contact customer support. 

### Data Model

The shell's data model includes all shell metadata, families, and attributes.

#### **Amazon AWS Cloud Provider Shell 2G Attributes**

The attribute names and types that are derived from the standard are listed in the following section of the Cloud Provider Shell Standard:

[Common Cloud Provider Attributes](https://github.com/QualiSystems/cloudshell-standards/blob/master/Documentation/cloud_provider_standard.md#attributes)

The following table describes attributes that are unique to this shell and are not documented in the Shell Standard: 

|Attribute Name|Data Type|Description|
|:---|:---|:---|
|REGION|Lookup|The public cloud region to be used by this cloud provider resource.|
|AWS MGMT SG ID|string|The Management VPC's security group. Use the __SG1id__ output when configuring the Management VPC for the region. For example, "sg-71240198". This value is used by the Setup process to configure the communication between the Management VPC's instances and the Sandbox instances.|
|AWS MGMT VPC ID|string|ID of the Management VPC. Used by the Setup process to set up the VPC and subnet for the sandbox. Use the __ManagementVPCID__ output when configuring the Management VPC for the region. For example “vpc-633fb904”.|
|KEYPAIRS LOCATION|string|The name of an S3 bucket in which PEM files will be located. Each active Sandbox will have a PEM file under a designated folder.  <br>Use the __S3Name__ output when configuring the Management VPC for the region. For example: "sandbox-management".|
|MAX STORAGE SIZE|numeric|The max number of GiB of the root volume. Must be greater than zero or the size of the snapshot used. If kept empty the default size of the snapshot will be used. For example 8.|
|MAX STORAGE IOPS|numeric|The max number of I/O operations per second that the volume can support. For Provisioned IOPS (SSD) volumes, you can provision up to 30 IOPS per GiB. If left empty the default in the AMI will be used. For example 240.|
|NETWORKS IN USE|string|Reserved networks that will be excluded when allocating Sandbox networks. Should include at least the management network. The syntax is comma separated CIDRs. For example: 10.0.0.0/24, 10.1.0.0/16, 172.31.0.0/24.|
|INSTANCE TYPE|string|The AWS EC2 instance type. The instance type determines the CPU, memory and networking capacity of the instance. For example: "t2.large".|
|VPC MODE|lookup|Every sandbox with AWS apps deploys a VPC to AWS. This setting determines how the sandbox VPC will chose a CIDR block. In __DYNAMIC__ mode, the CIDR block is chosen by Cloudshell Server. In __STATIC__ mode, the CIDR block for all sandboxes allocated will be taken from VPC CIDR attribute on AWS cloud provider. Select __SHARED__ to indicate that the cloud provider resource will deploy to the shared VPC defined in __Shared VPC ID__. Select __Single__ to deploy Apps based on this cloud provider resource to the Management VPC.|
|STATIC VPC CIDR|string|The CIDR used for sandbox VPC when __VPC MODE__ is __STATIC__.|
|SHARED VPC ID|string|V(Mandatory for Shared VPC mode) Shared VPC’s ID. For example: “vpc-0bf24b1ebrd855e30”.|
|Shared VPC Role ARN| string|(Mandatory for Shared VPC mode) Role created by the CloudFormation process with read/write permissions in the AWS account. This role is used by CloudShell to operate in the shared VPC. To find the role, open the main CloudFormation stack, click the __Outputs__ tab and copy the __SharedRoleARN__.|
|TRANSIT GATEWAY ID|string|(Mandatory for Shared VPC mode) ID of the transit gateway. To find the transit gateway id, open the CloudFormation stack that has “VPCNAT” in its name, click the __Outputs__ tab and copy the __TGWid__ value.|
|ADDITIONAL MANAGEMENT NETWORKS|string|Networks to be allowed to interact with all sandboxes. This is used for allowing connectivity to AWS resources outside the Management VPC. The syntax is comma separated CIDRs. For example, "10.0.0.0/24,10.1.0.0/16,172.31.0.0/24".|
|VPN GATEWAY ID|string|(Mandatory for Shared VPC mode) ID of the gateway to use. Leave empty if the __UseTransitGateway__ attribute was enabled in the CloudFormation, specify the VPN gateway ID if the attribute was set to “False”. To find the VPN gateway ID, open the shared VPC's CloudFormation stack, click the __Outputs__ tab and copy the __VPNGWid__ value.|
|VPN CIDR|string|(Mandatory for Shared VPC mode if VPN Gateway ID is defined) Comma-separated list of CIDRs in the local network to be used to VPN to the shared VPC. For example: "10.1.0.0/24,10.3.0.0/16".|


### Automation
This section describes the automation (driver) associated with the data model. 
The shell’s driver is provided as part of the shell package. 
There are two types of automation processes, Autoload and Resource Commands. 
Autoload is executed when creating the resource in the **Inventory** dashboard.

For detailed information on each available commands, see the following section of the Cloud Provider Standard:

[Common Cloud Provider Commands](https://github.com/QualiSystems/cloudshell-standards/blob/master/Documentation/cloud_provider_standard.md#commands)

# AWS Integration Process
In order to integrate CloudShell with AWS, you need to first deploy the CloudShell management and sandbox VPCs on your AWS region. This is done using CloudFormation templates that define the VPC deployment type (dedicated VPCs per sandbox or shared VPCs in which the sandboxes deploy to a pre-defined VPC), the connection to your Quali Server and more. Additional steps are required, such as configuring the integration's management instances and creating App templates which include the definition of the instances to deploy, image and configuration management to be performed on the deployed instances. For details, see CloudShell Help's [AWS Integration](https://help.quali.com/Online%20Help/0.0/Portal/Content/Admn/VPC-Ovrv.htm) chapter. 

# Downloading the Shell
The Amazon AWS Cloud Provider Shell 2G shell is available from the [Quali Community Integrations](https://community.quali.com/integrations) page. 

Download the files into a temporary location on your local machine. 

The shell comprises of the following files:

|File name|Description|
|:---|:---|
|Amazon AWS Cloud Provider Shell 2G.zip|Device shell package|
|cloudshell-Amazon-AWS-Cloud-Provider-Shell-2G-dependencies-win32-package-1.0.x.zip, cloudshell-Amazon-AWS-Cloud-Provider-Shell-2G-dependencies-linux-package-1.0.x.zip - 
|Shell Python dependencies (for offline deployments only)|

# Importing and Configuring the Shell
This section describes how to import the Amazon AWS Cloud Provider Shell 2G shell and configure and modify the Cloud Provider Resource created using the shell.

### Importing the shell into CloudShell

**To import the shell into CloudShell:**
  1. Make sure you have the shell’s zip package. 
  If not, download the shell from the [Quali Community's Integrations](https://community.quali.com/integrations) page or from the releases page of this repo.
  
  2. In CloudShell Portal, as a System Administrator, open the **Manage –- Shells** page (Global domain only).
  
  3. Click **Import**.
  
  4. In the dialog box, navigate to the shell's zip package, select it and click **Open**. 

<br>The shell is displayed in the **Shells** page and can be used by domain administrators in all CloudShell domains to create new inventory resources, as explained in [Adding Inventory Resources](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/INVN/Add-Rsrc-Tmplt.htm?Highlight=adding%20inventory%20resources). 

### Offline installation of a shell
**Note:** Offline installation instructions are relevant only if the CloudShell Execution Server has no access to PyPi.org. You can skip this section if your execution server has access to PyPi.org. For additional information, see the online help topic on offline dependencies.

In offline mode, import the shell into CloudShell and place any dependencies in the appropriate dependencies folder.

See [Adding Shell and script packages to the local PyPi Server repository](#adding-shell-and-script-packages-to-the-local-pypi-server-repository).

### Adding shell and script packages to the local PyPi Server repository
If your Quali Server and/or execution servers work offline, you will need to copy all required Python packages, including the out-of-the-box ones, to the PyPi Server's repository on the Quali Server computer. 

(by default *C:\Program Files (x86)\QualiSystems\CloudShell\Server\Config\Pypi Server Repository*).

For more information, see [Configuring CloudShell to Execute Python Commands in Offline Mode](http://help.quali.com/Online%20Help/9.0/Portal/Content/Admn/Cnfgr-Pyth-Env-Wrk-Offln.htm?Highlight=Configuring%20CloudShell%20to%20Execute%20Python%20Commands%20in%20Offline%20Mode).

**To add Python packages to the local PyPi Server repository:**
  1. If you haven't created and configured the local PyPi Server repository to work with the execution server, perform the steps in [Add Python packages to the local PyPi Server repository (offline mode)](http://help.quali.com/Online%20Help/9.0/Portal/Content/Admn/Cnfgr-Pyth-Env-Wrk-Offln.htm?Highlight=offline%20dependencies#Add). 
  
  2. For each shell or script you add into CloudShell, do one of the following (from an online computer):
      * Connect to the Internet and download each dependency specified in the *requirements.txt* file with the following command: 
`pip download -r requirements.txt`. 
     The shell or script's requirements are downloaded as zip files.

      * In the [Quali Community's Integrations](https://community.quali.com/integrations) page, locate the shell and click the shell's **Download** link. In the page that is displayed, from the Downloads area, extract the dependencies package zip file.

3. Place these zip files in the local PyPi Server repository.
 
### Configuring the Cloud Provider Resource
This section explains how to create a new Cloud Provider Resource using the shell.

**To create a Amazon AWS Cloud Provider Resource:**  
  1. In the CloudShell Portal, in the **Inventory** dashboard, click **Add New**.
     ![Image][2]
     
  3. From the list, select **Amazon AWS Cloud Provider Shell 2G**.
  
  4. Click **Create**.
  
  5. In the **Resource** dialog box, enter the following attributes with data from step 1:
     - __REGION__: The public cloud region to be used by this cloud provider resource.
     - __AWS MGMT SG ID__: The Management VPC's security group. Use the __SG1id__ output when configuring the Management VPC for the region. For example, "sg-71240198".
<br>This value is used by the Setup process to configure the communication between the Management VPC's instances and the Sandbox instances.
     - __AWS MGMT VPC ID__: ID of the Management VPC. Used by the Setup process to set up the VPC and subnet for the sandbox.
     <br>Use the __ManagementVPCID__ output when configuring the Management VPC for the region. For example “vpc-633fb904”.
     - __KEYPAIRS LOCATION__: The name of an S3 bucket in which PEM files will be located. Each active Sandbox will have a PEM file under a designated folder.  <br>Use the __S3Name__ output when configuring the Management VPC for the region. For example: "sandbox-management".
     - __MAX STORAGE SIZE__: The max number of GiB of the root volume. Must be greater than zero or the size of the snapshot used. If kept empty the default size of the snapshot will be used. For example 8.
     - __MAX STORAGE IOPS__: The max number of I/O operations per second that the volume can support. For Provisioned IOPS (SSD) volumes, you can provision up to 30 IOPS per GiB. If left empty the default in the AMI will be used. For example 240.
     - __NETWORKS IN USE__: Reserved networks that will be excluded when allocating Sandbox networks. Should include at least the management network. The syntax is comma separated CIDRs. For example: 10.0.0.0/24, 10.1.0.0/16, 172.31.0.0/24.
     - __INSTANCE TYPE__: The AWS EC2 instance type. The instance type determines the CPU, memory and networking capacity of the instance. For example: t2.large.
     - __VPC MODE__: Every sandbox with AWS apps deploys a VPC to AWS. This setting determines how the sandbox VPC will chose a CIDR block. Options are:
        - __DYNAMIC__: The CIDR block is chosen by Cloudshell Server. In other words, CloudShell deploys a new VPC with a dedicated CIDR for every sandbox.
        - __STATIC__: The CIDR block for all sandboxes allocated will be taken from VPC CIDR attribute on AWS cloud provider.
        - __SHARED__: Indicates that the cloud provider resource will deploy to the shared VPC defined in __Shared VPC ID__.
        - __Single__: Apps based on this cloud provider resource will be deployed to the Management VPC.
     - __STATIC VPC CIDR__: The CIDR used for sandbox VPC when __VPC Mode__ is __Static__.
     - __SHARED VPC ID__: (Mandatory for Shared VPC mode) Shared VPC’s ID. For example: “vpc-0bf24b1ebrd855e30”.
     - __SHARED VPC ROLE ARN__: (Mandatory for Shared VPC mode) Role created by the CloudFormation process with read/write permissions in the AWS account. This role is used by CloudShell to operate in the shared VPC. To find the role, open the main CloudFormation stack, click the __Outputs__ tab and copy the __SharedRoleARN__.
     - __TRANSIT GATEWAY ID__: (Mandatory for Shared VPC mode) ID of the transit gateway. To find the transit gateway id, open the CloudFormation stack that has “VPCNAT” in its name, click the __Outputs__ tab and copy the __TGWid__ value.
     - __ADDITIONAL MANAGEMENT NETWORKS__: Networks to be allowed to interact with all sandboxes. This is used for allowing connectivity to AWS resources outside the Management VPC. 
<br>The syntax is comma separated CIDRs. For example, "10.0.0.0/24,10.1.0.0/16,172.31.0.0/24".
     - __VPN GATEWAY ID__: (Mandatory for Shared VPC mode) ID of the gateway to use. Required to connect the shared VPC's sandbox subnets to the VPN gateway. CloudShell does this by creating a route between the specified VPN gateway and the connected subnet within the VPC CIDR. To find the role, open the shared VPC CloudFormation stack, click the __Outputs__ tab and copy the __VPNGWid__ value.
     - __VPN CIDR__: (Mandatory for Shared VPC mode if VPN Gateway ID is defined) Comma-separated list of CIDRs in the local network to be used to VPN to the shared VPC. For example: "10.1.0.0/24,10.3.0.0/16".
  
  6. Click **Continue**.

CloudShell will validate the provided settings and create the new resource.

_**in order to use the Amazon AWS Cloud Provider Shell 2G Shell you must create an appropriate App template, which will be deployed as part of the sandbox reservation. For details on app templates, see the following CloudShell Help article: [Add an AWS EC2 App Template](https://help.quali.com/Online%20Help/0.0/Portal/Content/Admn/VPC-AWS-App.htm)

# Updating Python Dependencies for Shells
This section explains how to update your Python dependencies folder. This is required when you upgrade a shell that uses new/updated dependencies. It applies to both online and offline dependencies.
### Updating offline Python dependencies
**To update offline Python dependencies:**
1. Download the latest Python dependencies package zip file locally.

2. Extract the zip file to the suitable offline package folder(s). 

3. Terminate the shell’s instance, as explained [here](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/MNG/Mng-Exctn-Srv-Exct.htm#Terminat). 

### Updating online Python dependencies
In online mode, the execution server automatically downloads and extracts the appropriate dependencies file to the online Python dependencies repository every time a new instance of the driver or script is created.

**To update online Python dependencies:**
* If there is a live instance of the shell's driver or script, terminate the shell’s instance, as explained [here](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/MNG/Mng-Exctn-Srv-Exct.htm#Terminat). If an instance does not exist, the execution server will download the Python dependencies the next time a command of the driver or script runs.

# Typical Workflows

### Configuring CloudShell to allow Static Mode in AWS EC2
Perform these steps to allow CloudShell to deploy sandboxes using the __Static__ VPC Mode option. For details, see "Static Mode" in [Add an AWS EC2 Cloud Provider Resource
](https://help.quali.com/Online%20Help/0.0/Portal/Content/Admn/VPC-AWS-Cld-Prvdr-Rsc.htm). 

1. In Resource Manager Client, open the __Attributes__ tab and select the __Allocated CIDR__ attribute.
2. Click the __Edit__ button, unselect the __Read-only__ checkbox, and save your changes.
3. Open the __Resource Families__ tab.
4. Expand __Virtual Network__ and select __Subnet__.
5. Select __Allocated CIDR__ and click __Edit Rules__.
6. Select the __User Input__ checkbox and save.
6. In CloudShell Portal, open the suitable blueprint, specify the appropriate CIDR in the __Allocated CIDR__ attribute for each subnet service.

# References
To download and share integrations, see [Quali Community's Integrations](https://community.quali.com/integrations). 

For instructional training and documentation, see [Quali University](https://www.quali.com/university/).

To suggest an idea for the product, see [Quali's Idea box](https://community.quali.com/ideabox). 

To connect with Quali users and experts from around the world, ask questions and discuss issues, see [Quali's Community forums](https://community.quali.com/forums). 

# Release Notes 

### What's New

For release updates, see the shell's [GitHub releases page](https://github.com/QualiSystems/Microsoft-Azure-Cloud-Provider-Shell-2G/releases).


[1]: https://github.com/QualiSystems/cloudshell-shells-documentaion-templates/blob/master/cloudshell_logo.png
[2]: https://github.com/QualiSystems/cloudshell-shells-documentaion-templates/blob/master/create_a_resource_device.png
