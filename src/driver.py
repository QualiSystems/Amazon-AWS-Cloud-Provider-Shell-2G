from typing import List

from cloudshell.api.cloudshell_api import InputNameValue
from cloudshell.api.common_cloudshell_api import CloudShellAPIError
from cloudshell.cp.core import DriverRequestParser
from cloudshell.cp.core.models import ConnectSubnet, DeployApp, DriverResponse
from cloudshell.cp.core.utils import single
from cloudshell.shell.core.driver_context import ResourceCommandContext
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext

from cloudshell.cp.aws.aws_shell import AWSShell
from cloudshell.cp.aws.models.deploy_aws_ec2_ami_instance_resource_model import (
    DeployAWSEc2AMIInstanceResourceModel,
)


OPA_RESOURCE_NAME = "OPA"


class AmazonAwsCloudProviderShell2GDriver(ResourceDriverInterface):
    def cleanup(self):
        pass

    def __init__(self):
        self.aws_shell = AWSShell()
        self.request_parser = DriverRequestParser()
        self.request_parser.add_deployment_model(
            deployment_model_cls=DeployAWSEc2AMIInstanceResourceModel
        )
        deploy_name = "Amazon AWS Cloud Provider 2G.Amazon AWS EC2 Instance 2G"
        self.deployments = {deploy_name: self.deploy_ami}

    def initialize(self, context):
        pass

    def Deploy(self, context, request=None, cancellation_context=None):
        self._execute_opa_validation_cmd(context, request)
        actions = self.request_parser.convert_driver_request_to_actions(request)
        deploy_action = single(actions, lambda x: isinstance(x, DeployApp))
        deployment_name = deploy_action.actionParams.deployment.deploymentPath
        self.parse_vnicename(actions)

        if deployment_name in self.deployments.keys():
            deploy_method = self.deployments[deployment_name]
            deploy_result = deploy_method(context, actions,
                                          cancellation_context)
            return DriverResponse(deploy_result).to_driver_response_json()
        else:
            raise Exception("Could not find the deployment")

    def _check_opa_exists(self, api, opa_resource_name):
        try:
            api.GetResourceCommands(opa_resource_name)
            return True
        except CloudShellAPIError:
            return

    def _execute_opa_validation_cmd(self, context, plan_json):
        resource_opa = OPA_RESOURCE_NAME
        api = CloudShellSessionContext(context).get_api()
        if not self._check_opa_exists(api, resource_opa):
            return
        try:
            api.ExecuteCommand(
                context.reservation.reservation_id,
                resource_opa,
                targetType="Resource",
                commandName="validate",
                commandInputs=[InputNameValue("validation_request", plan_json)],
                printOutput=True
            )
        except CloudShellAPIError as e:
            raise Exception(e.message)

    def parse_vnicename(self, actions):
        network_actions = [a for a in actions if isinstance(a, ConnectSubnet)]
        for network_action in network_actions:
            try:
                network_action.actionParams.vnicName = int(
                    network_action.actionParams.vnicName
                )
            except Exception:
                network_action.actionParams.vnicName = None

    def deploy_ami(self, context, actions, cancellation_context):
        return self.aws_shell.deploy_ami(context, actions, cancellation_context)

    def PowerOn(self, context, ports):
        return self.aws_shell.power_on_ami(context)

    def PowerOff(self, context, ports):
        return self.aws_shell.power_off_ami(context)

    def orchestration_power_on(self, context, ports):
        return self.aws_shell.power_on_ami(context)

    def orchestration_power_off(self, context, ports):
        return self.aws_shell.power_off_ami(context)

    def PowerCycle(self, context, ports, delay):
        pass

    def remote_refresh_ip(self, context, ports, cancellation_context):
        return self.aws_shell.refresh_ip(context)

    def DeleteInstance(self, context, ports):
        return self.aws_shell.delete_instance(context)

    def PrepareSandboxInfra(self, context, request, cancellation_context):
        self._execute_opa_validation_cmd(context, request)
        actions = self.request_parser.convert_driver_request_to_actions(request)
        action_results = self.aws_shell.prepare_connectivity(
            context, actions, cancellation_context
        )
        return DriverResponse(action_results).to_driver_response_json()

    def CleanupSandboxInfra(self, context, request):
        actions = self.request_parser.convert_driver_request_to_actions(request)
        return self.aws_shell.cleanup_connectivity(context, actions)

    def GetApplicationPorts(self, context, ports):
        return self.aws_shell.get_application_ports(context)

    def get_inventory(self, context):
        return self.aws_shell.get_inventory(command_context=context)

    def GetAccessKey(self, context, ports):
        return self.aws_shell.get_access_key(context)

    def SetAppSecurityGroups(self, context, request):
        return self.aws_shell.set_app_security_groups(context, request)

    def GetVmDetails(self, context, cancellation_context, requests):
        return self.aws_shell.get_vm_details(context, cancellation_context, requests)

    def CreateTrafficMirroring(self, context, request, cancellation_context=None):
        action_results = self.aws_shell.create_traffic_mirroring(
            context, cancellation_context, request
        )
        return DriverResponse(action_results).to_driver_response_json()

    def RemoveTrafficMirroring(self, context, request):
        action_results = self.aws_shell.remove_traffic_mirroring(context, request)
        return DriverResponse(action_results).to_driver_response_json()

    def AddCustomTags(self, context, request, ports):
        return self.aws_shell.add_custom_tags(context, request)

    def save_app(self, context, cancellation_context, ports):
        return self.aws_shell.save_app(context, cancellation_context)

    def remote_save_snapshot(
        self,
        context: ResourceCommandContext,
        ports: List[str],
        snapshot_name: str,
        save_memory: str,
    ):
        """Saves virtual machine to a snapshot.

        :param context: resource context of the vCenterShell
        :param ports:list[string] ports: the ports of the connection between the remote
            resource and the local resource
        :param snapshot_name: snapshot name to save to
        :param save_memory: Snapshot the virtual machine's memory. Lookup, Yes / No
        """
        self.aws_shell.remote_save_snapshot(context, snapshot_name)

    def remote_restore_snapshot(
        self, context: ResourceCommandContext, ports: List[str], snapshot_name: str
    ):
        """Restores virtual machine from a snapshot.

        :param context: resource context of the vCenterShell
        :param ports:list[string] ports: the ports of the connection between the remote
            resource and the local resource
        :param snapshot_name: Snapshot name to restore from
        """
        self.aws_shell.remote_restore_snapshot(context, snapshot_name)

    def remote_get_snapshots(
        self, context: ResourceCommandContext, ports: List[str]
    ) -> list:
        """Returns list of snapshots.

        :param context: resource context of the vCenterShell
        :param ports:list[string] ports: the ports of the connection between the remote
            resource and the local resource
        """
        return self.aws_shell.remote_get_snapshots(context)

    def assign_additional_private_ipv4s(self, context, ports, vnic_id, new_ips):
        return self.aws_shell.assign_additional_private_ipv4s(context, vnic_id, new_ips)
