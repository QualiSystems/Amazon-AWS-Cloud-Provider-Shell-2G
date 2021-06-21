![Image][1]

# **Kubernetes Cloud Provider Shell 2G**

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

The Apps can be modeled a variety of types of services, depending on the Cloud Provider, including VMs, Containers, or Emulated instances.  

### Kubernetes Cloud Provider Shell 2G
Kubernetes Cloud Provider Shell 2G provides you with apps deployment and management capabilities on a Kubernetes cluster.

The shell supports connection to a self managed cluster, an Azure Kubernetes Service cluster, or an Amazon Elastic Kubernetes Service cluster.  

For more information on Kubernetes, see the vendor's official product documentation.

### Standard version
Kubernetes Cloud Provider Shell 2G is based on the Cloud Provider Standard version **1.0.0**.

For detailed information about the shell’s structure and attributes, see the [Cloud Provider Standard](https://github.com/QualiSystems/cloudshell-standards/blob/master/Documentation/cloud_provider_standard.md) in GitHub.

### Requirements

Release: Kubernetes Cloud Provider Shell 2G

▪ CloudShell version **9.3 and above**

▪ Kubernetes version **1.18**

**Note:** If your CloudShell version does not support this shell, you should consider upgrading to a later version of CloudShell or contact customer support. 

### Data Model

The shell's data model includes all shell metadata, families, and attributes.

#### **Kubernetes Cloud Provider Shell 2G Attributes**

The attribute names and types that are derived from the standard are listed in the following section of the Cloud Provider Shell Standard:

[Common Cloud Provider Attributes](https://github.com/QualiSystems/cloudshell-standards/blob/master/Documentation/cloud_provider_standard.md#attributes)

The following table describes attributes that are unique to this shell and are not documented in the Shell Standard: 

|Attribute Name|Data Type|Description|
|:---|:---|:---|
|Config File Path|String|Full Path to a standalone kubernetes config file containing all the relevant information for authentication. The file must reside on the Execution Server machine. To generate a portable config file, run command 'kubectl config view --flatten'.|
|AWS CP Resource Name|String|(Optional - EKS only) The CloudShell resource name for the AWS Cloud Provider Resource|
|External Service Type|String|The service type the shell will create for external services. __LoadBalancer type__ should be used when the Kubernetes cluster is hosted on a supported public cloud provider like AWS and Azure. Use __NodePort__ when the cluster is self-hosted.|


### Automation
This section describes the automation (driver) associated with the data model. 
The shell’s driver is provided as part of the shell package. 
There are two types of automation processes, Autoload and Resource Commands. 
Autoload is executed when creating the resource in the **Inventory** dashboard.

For detailed information on each available commands, see the following section of the Cloud Provider Standard:

[Common Cloud Provider Commands](https://github.com/QualiSystems/cloudshell-standards/blob/master/Documentation/cloud_provider_standard.md#commands)


# Downloading the Shell
The Kubernetes Cloud Provider Shell 2G shell is available from the [Quali Community Integrations](https://community.quali.com/integrations) page. 

Download the files into a temporary location on your local machine. 

The shell comprises of the following files:

|File name|Description|
|:---|:---|
|Kubernetes Cloud Provider Shell 2G.zip|Device shell package|
|cloudshell-kubernetes-dependencies-package-1.0.x.zip|Shell Python dependencies (for offline deployments only)|

# Importing and Configuring the Shell
This section describes how to import the Kubernetes Cloud Provider Shell 2G shell and configure and modify the Cloud Provider Resource created using the shell.

### Importing the shell into CloudShell

**To import the shell into CloudShell:**
  1. Make sure you have the shell’s zip package. 
  If not, download the shell from the [Quali Community's Integrations](https://community.quali.com/integrations) page or from the releases page of this repo.
  
  2. In CloudShell Portal, as a System Administrator, open the **Manage –- Shells** page (Global domain only).
  
  3. Click **Import**.
  
  4. In the dialog box, navigate to the shell's zip package, select it and click **Open**. 

<br><br>The shell is displayed in the **Shells** page and can be used by domain administrators in all CloudShell domains to create new inventory resources, as explained in [Adding Inventory Resources](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/INVN/Add-Rsrc-Tmplt.htm?Highlight=adding%20inventory%20resources). 

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

**To create a Kubernetes Cloud Provider Resource:**  
  1. In the CloudShell Portal, in the **Inventory** dashboard, click **Add New**.
     ![Image][2]
     
  3. From the list, select **Kubernetes Cloud Provider Shell 2G**.
  
  4. Click **Create**.
  
  5. In the **Resource** dialog box, enter the following attributes with data from step 1:
        - **Config File Path** - The full path to a standalone Kubernetes _config_ file (no extension) containing all the relevant information for authentication (e.g. "C:\Kubernetes\config". The file must reside on the Execution Server machine. To generate a portable config file, run command 'kubectl config view --flatten'. 
        - **AWS CP Resource Name** - **(Optional - EKS only)** The CloudShell resource name for the AWS Cloud Provider Resource
        - **External Service Type** - The service type the shell will create for external services. __LoadBalancer__ types should be used when the Kubernetes cluster is hosted on a supported public cloud provider like GCP, AWS or Azure. Use __NodePort__ when the cluster is self-hosted.
  
  6. Click **Continue**.

CloudShell will validate the provided settings and create the new resource.

_**in order to us the Kubernetes Cloud Provider Shell 2G Shell you must create an appropriate App template, which would be deployed as part of the sandbox reservation. For details on app templates, see the following CloudShell Help article: [Applications' Typical Workflow](https://help.quali.com/Online%20Help/0.0/Portal/Content/CSP/MNG/Mng-Apps.htm?Highlight=App#Adding)

for information on creating Kubernetes App Templates, see [Adding a Kubernetes App Template](#adding-a-kubernetes-app-template)**_

### Adding a Kubernetes App Template

**To add a Kubernetes based App Template into CloudShell:**
  1. As a Domain or System Administrator, go to Manage -- Apps
  
  2. Click on the **Add** button at the top of the page
  
  3. Choose the **Kubernetes Service** deployment option, fill in the app name and click **Create**
  
  4. Fill in the app's description, image and categories and click on **Deployment Paths** on the left side
  
  5. Under the **Kubernetes Service** deployment option, fill in the following details:

|Attribute Name|Data Type|Description|
|:---|:---|:---|
|Image Name|String|The name of the container image to use for creating the container. Image must exist in the image repository used by the cluster.|
|Image Tag|String|**(Optional)** The container image tag (usually represents the image version).|
|Internal Ports|String|**(Optional)** The ports required by the application for internal communications.|
|External Ports|String|Comma-separated list of the TCP ports required by the application for external communications (outside the cluster). For example: "34,161,15"|
|Replicas|Integer|The number of container instances that will be deployed. Default is 1.|
|Start Command|String|**(Optional)** Replace the default start command for executing the container.|
|Environment Variables|String|**(Optional)** Comma separated list of 'key=value' environment variables that will be defined in the container.|
|Wait for Replicas|Integer|Wait X number of seconds during power on for all replicas to be in ready state. When the value is zero or less the shell will not wait for replicas to be ready. Default is 120.|
|CPU Request|String|**(Optional)** The requested CPU for each container. Fractional requests are also allowed. For example '0.5'. Optional unless any resource request or limit is specified.|
|RAM Request|String|**(Optional)** The requested RAM for each container. Memory is measured in bytes. Memory is expressed as a plain integer or as a fixed-point integer using one of these suffixes - E, P, T, G, M, K. You can also use the power-of-two equivalents - Ei, Pi, Ti, Gi, Mi, Ki. For example, '256M'.|
|CPU Limit|String|**(Optional)** The CPU limit for each container. Fractional limits are also allowed. For example '0.5'.|
|RAM Limit|String|**(Optional)** The RAM limit for each container. Memory is measured in bytes. Memory is expressed as a plain integer or as a fixed-point integer using one of these suffixes - E, P, T, G, M, K. You can also use the power-of-two equivalents - Ei, Pi, Ti, Gi, Mi, Ki. For example, '256M'.|

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
