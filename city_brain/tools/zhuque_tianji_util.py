#!/home/tops/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json
import errno
import yaml
import zhuque_ip_pool
import tianji_clt
import time
import argparse
import commands
import traceback

sys.setdefaultencoding('utf-8')
regionSite = {
    "dns-newapi-domain": True,
    "dns-newapi-key": True,
    "dns-newapi-user": True,
    "dns-oldapi-url": True,
    "internet-domain": True,
    "intranet-domain": True,
    "project": True,
    "city": True,
    "cloudType": True,
    "version": True,
    "yaochiaccesskey-id": True,
    "yaochiaccesssecret": True,
    "yunwei-domain": True,
    "region": True,
    "REGION": True,
    "location_tree": True,
    "networkProtocol": True,
    "registry_repo_dir": True,
    "tairGroupName": True,
    "tairConfigId": True,
    "db.dpphoenix.db_host": True,
    "db.dpphoenix.db_port": True,
    "db.dpphoenix.db_user": True,
    "db.dpphoenix.db_password": True,
    "account.superKey.id": True,
    "account.superKey.user": True,
    "account.superKey.accesskey-id": True,
    "account.superKey.accesskey-secret": True,
    "account.defaultUser.id": True,
    "account.defaultUser.user": True,
    "account.defaultUser.password": True,
    "account.defaultUser.accesskey-id": True,
    "account.defaultUser.accesskey-secret": True,
    "account.adminportal.id": True,
    "account.adminportal.user": True,
    "account.adminportal.accesskey-id": True,
    "account.adminportal.accesskey-secret": True,
    "account.oss.id": True,
    "account.oss.user": True,
    "account.oss.accesskey-id": True,
    "account.oss.accesskey-secret": True,
    "account.csc.id": True,
    "account.csc.user": True,
    "account.csc.accesskey-id": True,
    "account.csc.accesskey-secret": True,
    "account.sls.id": True,
    "account.sls.user": True,
    "account.sls.accesskey-id": True,
    "account.sls.accesskey-secret": True,
    "account.all.id": True,
    "account.all.user": True,
    "account.all.accesskey-id": True,
    "account.all.accesskey-secret": True,
    "account.ecs.id": True,
    "account.ecs.user": True,
    "account.ecs.accesskey-id": True,
    "account.ecs.accesskey-secret": True,
    "account.to-sls.id": True,
    "account.to-sls.user": True,
    "account.to-sls.accesskey-id": True,
    "account.to-sls.accesskey-secret": True,
    "account.tdc.id": True,
    "account.tdc.user": True,
    "account.tdc.accesskey-id": True,
    "account.tdc.accesskey-secret": True,
    "account.ots.id": True,
    "account.ots.user": True,
    "account.ots.accesskey-id": True,
    "account.ots.accesskey-secret": True,
    "account.odps.id": True,
    "account.odps.user": True,
    "account.odps.accesskey-id": True,
    "account.odps.accesskey-secret": True,
    "account.ads.id": True,
    "account.ads.user": True,
    "account.ads.password": True,
    "account.ads.accesskey-id": True,
    "account.ads.accesskey-secret": True,
    "account.odps-console.id": True,
    "account.odps-console.user": True,
    "account.odps-console.accesskey-id": True,
    "account.odps-console.accesskey-secret": True,
    "account.rds.id": True,
    "account.rds.user": True,
    "account.rds.accesskey-id": True,
    "account.rds.accesskey-secret": True,
    "account.ecs-console.id": True,
    "account.ecs-console.user": True,
    "account.ecs-console.accesskey-id": True,
    "account.ecs-console.accesskey-secret": True,
    "account.dxp.id": True,
    "account.dxp.user": True,
    "account.dxp.accesskey-id": True,
    "account.dxp.accesskey-secret": True,
    "account.oss-test1.id": True,
    "account.oss-test1.user": True,
    "account.oss-test1.accesskey-id": True,
    "account.oss-test1.accesskey-secret": True,
    "account.oss-test2.id": True,
    "account.oss-test2.user": True,
    "account.oss-test2.accesskey-id": True,
    "account.oss-test2.accesskey-secret": True,
    "account.oss-backup.id": True,
    "account.oss-backup.user": True,
    "account.oss-backup.accesskey-id": True,
    "account.oss-backup.accesskey-secret": True,
    "account.oss-manage.id": True,
    "account.oss-manage.user": True,
    "account.oss-manage.accesskey-id": True,
    "account.oss-manage.accesskey-secret": True,
    "account.oss-sync.id": True,
    "account.oss-sync.user": True,
    "account.oss-sync.accesskey-id": True,
    "account.oss-sync.accesskey-secret": True,
    "account.oss.ownerid": True,
    "account.drds.id": True,
    "account.drds.user": True,
    "account.drds.accesskey-id": True,
    "account.drds.accesskey-secret": True,
    "account.dts.id": True,
    "account.dts.user": True,
    "account.dts.accesskey-id": True,
    "account.dts.accesskey-secret": True,
    "account.location.id": True,
    "account.location.user": True,
    "account.location.accesskey-id": True,
    "account.location.accesskey-secret": True,
    "account.defaultUser.accesskey-id-encrypted": True,
    "account.defaultUser.accesskey-secret-encrypted": True,
    "centerRegion": True,
    "regionMap": True,
    "zoneList": True,
    "zoneA": True,
    "zoneB": True,
    "idc_roomA": True,
    "idc_roomB": True
}


class ZhuqueTianjiGetter:
    def __init__(self, tianjiCltConf, azone, onlyProjectNames=None, debug=False, ippool=False):
        self.tianjiAPI = tianji_clt.TianjiAPI(tianjiCltConf)
        self.onlyProjectNames = onlyProjectNames
        self.azone = azone
        self.debug = debug
        self.ippool = ippool
        self.output = {"updated": time.strftime("%Y-%m-%d %X", time.localtime()), "toolVersion": "v3.3"}

    def GetProjectNames(self):
        projectNames = []
        projects = self.tianjiAPI.ListProjects()
        for projectName in projects:
            if self.onlyProjectNames and projectName not in self.onlyProjectNames:
                continue
            if projectName == "network" or projectName == "default" or projectName == "center-region-project":
                continue
            if projects[projectName] == "normal":
                projectNames.append(projectName)
        return projectNames

    def GetMachineNames(self):
        allMachines = {}
        projectNames = self.GetProjectNames()
        for projectName in projectNames:
            clusters = self.tianjiAPI.ListClusters(projectName)  ## return clusterName
            for clusterName in clusters:
                machines = self.tianjiAPI.ListClusterMachine(projectName, clusterName)
                for hostName in machines:
                    allMachines[hostName] = {"productName": projectName, "clusterName": clusterName}
        return allMachines

    def GetProductList(self):
        globalClusterInfo = {}
        tagConfMap = {}
        productList = []
        projectNames = self.GetProjectNames()
        isFound = False
        global_kvs = {}
        for projectName in projectNames:
            if projectName == "network" or projectName == "networks":
                continue
            print "---p", projectName
            productInfo = {"productName": projectName}
            clusterList = []
            clusters = self.tianjiAPI.ListClusters(projectName)  ## return clusterName
            for clusterName in clusters:
                print "---c", clusterName
                clusterConfig, version = self.tianjiAPI.CheckoutCluster(projectName, clusterName)
                if clusterConfig:
                    if clusterName == "default" or clusterName == "mock-center-region-cluster":
                        continue
                    tag_conf = clusterConfig.get("tag.conf")
                    try:
                        tag_conf_json = yaml.load(tag_conf)
                    except Exception as err:
                        print "load tag.conf error", err, tag_conf
                        exit(1)
                    tags = tag_conf_json.get("Tags")
                    clusterType = tags.get("__zhuque_tags_clusterType")

                    clusterInfo = {"clusterName": clusterName}
                    kv_conf = clusterConfig.get("kv.conf")
                    if kv_conf:
                        clusterFlags = {}
                        try:
                            kv_json = yaml.load(kv_conf)
                        except Exception as err:
                            print "load kv.conf err", err, kv_conf
                            exit(1)
                        kvs = kv_json.get("KeyValues")

                        zone = ""
                        if kvs.has_key("zone"):
                            zone = str(kvs["zone"])
                        elif kvs.has_key("biz_zone"):
                            zone = str(kvs["biz_zone"])
                        globalClusterInfo[clusterName] = {"zone": zone, "clusterType": clusterType,
                                                          "product": projectName}

                        if zone != "" and self.azone != "" and zone != self.azone:
                            continue

                        isFound = True
                        for k in kvs:
                            v = kvs[k]
                            # 跳过空value
                            if global_kvs.has_key(k) and len(str(v)) == 0:
                                continue

                            if regionSite.has_key(k):
                                global_kvs[k] = str(v)
                            else:
                                clusterFlags[k] = v
                        clusterInfo["clusterConfig"] = {
                            "ClusterFlags": clusterFlags
                        }

                    # clusterInfo
                    clusterInfo["serviceList"] = self._get_service_list(projectName, clusterName, clusterConfig)
                    clusterInfo["serverRoleGroupList"] = self._get_srg_list(projectName, clusterName, clusterConfig,
                                                                            clusterInfo["serviceList"])
                    clusterInfo["zhuqueClusterFlags"] = self._get_feature(tags)
                    clusterList.append(clusterInfo)

            productInfo["clusterList"] = clusterList
            productList.append(productInfo)

        global_config = []
        for k in global_kvs:
            global_config.append({"name": k, "value": global_kvs[k]})
        if not isFound and self.azone != "":
            print "input zone %s not found" % self.azone
            exit(1)
        return productList, global_config, globalClusterInfo

    def _get_feature(self, tags):
        try:
            if tags:
                return {"clusterType": tags.get("__zhuque_tags_clusterType"),
                        "cloudId": tags.get("__zhuque_tags_cloudId", ""),
                        "zhuqueVersionId": tags.get("__zhuque_tags_zhuqueVersionId", ""),
                        "customerId": tags.get("__zhuque_tags_customerId", ""),
                        "featureName": tags.get("__zhuque_tags_featureName"),
                        "productCommitId": tags.get("__zhuque_tags_productCommitId")}
            else:
                return {}
        except Exception as err:
            print str(err)
            exit(1)

    def _get_service_list(self, projectName, clusterName, clusterConfig):
        serviceList = []
        servicesConfig = clusterConfig.get("services")
        if servicesConfig:
            for serviceName in servicesConfig:
                if serviceName not in ["os"]:
                    serviceInfo = {"service": serviceName}
                    # 忽略role.conf, 但是有role.conf的serivce, 才添加到列表
                    role_conf = servicesConfig[serviceName].get("role.conf")
                    if role_conf:
                        # filename = "%s__%s__%s__role.conf" % (projectName, clusterName, serviceName)
                        # _save_file(filename, role_conf, True)
                        # serviceInfo["roleConfContent"] = role_conf
                        serviceList.append(serviceInfo)
                        # 忽略dependency_conf
                        # dependency_conf = servicesConfig[serviceName].get("dependency.conf")
                        # if dependency_conf:
                        #     serviceInfo["dependencies"] = self._get_service_dependencies(dependency_conf)

                        # 忽略resource_quota.json
                        # if servicesConfig[serviceName].get("tianji"):
                        #     resource_quota_json = servicesConfig[serviceName]["tianji"].get("resource_quota.json")
                        #     if resource_quota_json:
                        #         filename = "%s__%s__%s__resource_quota.json" % (projectName, clusterName, serviceName)
                        #         _save_file(filename, resource_quota_json, True)
                        #     else:
                        #         print "warn, %s__%s__%s, resource_quota.json is none" % ( projectName, clusterName, serviceName)

                        # 忽略serviceUserConfig
                        # if servicesConfig[serviceName].get("user"):
                        #     serviceUserConfig = []
                        #     for cfgName in servicesConfig[serviceName]["user"]:
                        #         cfgValue = servicesConfig[serviceName]["user"].get(cfgName)
                        #         if serviceName == "tianji" and cfgName == "Houyi":
                        #             continue
                        #         cfgContent = cfgValue
                        #         if isinstance(cfgContent, str):
                        #             serviceUserConfig.append({
                        #                 "CfgName": cfgName,
                        #                 "CfgContent": cfgContent
                        #             })
                        #             continue
                        #         else:
                        #             for subName in cfgValue:
                        #                 try:
                        #                     cfgContent = cfgValue[subName]
                        #                     if isinstance(cfgContent, str):
                        #                         serviceUserConfig.append({
                        #                             "CfgName": cfgName + "/" + subName,
                        #                             "CfgContent": cfgContent
                        #                         })
                        #                 except Exception as err:
                        #                     print "found user config err:", cfgValue
                        #                     exit(1)
                        #     if len(serviceUserConfig) > 0:
                        #         serviceInfo["serviceUserConfig"] = serviceUserConfig
        else:
            print "warn, %s__%s, services config is none" % (projectName, clusterName)
        return serviceList

    def _get_service_dependencies(self, dependency_conf):
        service_dependencies = []
        if dependency_conf:
            dependency_conf_json = json.loads(dependency_conf)
            if dependency_conf_json.has_key("Dependency"):
                for sr_name in dependency_conf_json.get("Dependency"):
                    if dependency_conf_json["Dependency"][sr_name].has_key("Service"):
                        for _depend in dependency_conf_json["Dependency"][sr_name]["Service"]:
                            if _depend not in service_dependencies:
                                service_dependencies.append(_depend)
        return service_dependencies

    def _get_srg_list(self, projectName, clusterName, clusterConfig, serviceList):
        srgList = []
        machine_group_conf = clusterConfig.get("machine_group.conf")
        if machine_group_conf:
            machine_group_conf_yaml_data = yaml.load(machine_group_conf)
            srgAttrsMap = {}
            srgAttrs = machine_group_conf_yaml_data.get("MachineGroupAttrs")
            if srgAttrs:
                for srg_name in srgAttrs:
                    if srgAttrs[srg_name] is None:
                        continue
                    srgAttr = {"serverRoleGroup": srg_name}
                    quota = srgAttrs[srg_name].get("quota")
                    shareQuota = srgAttrs[srg_name].get("shareQuota")
                    if quota:
                        srgAttr["quota"] = quota
                    if shareQuota:
                        srgAttr["shareQuota"] = shareQuota
                    srgAttrsMap[srg_name] = srgAttr

            srgs = machine_group_conf_yaml_data.get("MachineGroups")
            if srgs:
                map_server_roles = {}
                map_sr_build = {}
                map_sr_machines = {}
                for srg_name in srgs:
                    if srgs[srg_name] is None:
                        continue
                    srgInfo = {"serverRoleGroup": srg_name}
                    srgInfo["serverList"] = srgs[srg_name]
                    srgInfo["serverRoleList"] = []
                    # for tiangong
                    attr = srgAttrsMap[srg_name]
                    if attr:
                        if "quota" in attr:
                            srgInfo["ecsResourceQuota"] = attr["quota"]
                        if "shareQuota" in attr:
                            srgInfo["shareRoleTagResource"] = attr["shareQuota"]

                    for serviceInfo in serviceList:
                        serviceName = serviceInfo["service"]
                        server_roles = None

                        server_roles_key = "%s_%s" % (clusterName, serviceName)
                        if map_server_roles.has_key(server_roles_key):
                            print "get server roles cache", server_roles_key
                            server_roles = map_server_roles[server_roles_key]
                        else:
                            retry = 5
                            while retry > 0:
                                try:
                                    server_roles = self.tianjiAPI.ListInstanceServerrolesInService(clusterName,
                                                                                                   serviceName)
                                    if server_roles:
                                        map_server_roles[server_roles_key] = server_roles
                                        break
                                except Exception as e:
                                    print e
                                    retry -= 1
                                    time.sleep(1)

                        # for sr debug
                        if self.debug:
                            filename = "%s_%s_%s_sr.json" % (projectName, clusterName, serviceName)
                            save_json_file(filename, server_roles, True)

                        if server_roles and server_roles["ExpectedServerRoles"]:
                            for sr_name in server_roles["ExpectedServerRoles"]:
                                if_sr_in_srg = False
                                serverRoleInfo = {"serverRoleName": sr_name, "serviceName": serviceName}

                                sr_build_key = "%s_%s_%s_%s" % (projectName, clusterName, serviceName, sr_name)
                                if map_sr_build.has_key(sr_build_key):
                                    print "get sr buildId cache", sr_build_key
                                    serverRoleInfo["buildId"] = map_sr_build[sr_build_key]
                                else:
                                    serverRoleInfo["buildId"] = self._get_sr_build_id(clusterConfig, projectName,
                                                                                      clusterName, serviceName, sr_name)
                                    map_sr_build[sr_build_key] = serverRoleInfo["buildId"]

                                sr_machines = None
                                sr_machines_key = "%s_%s_%s" % (clusterName, serviceName, sr_name)
                                if map_sr_machines.has_key(sr_machines_key):
                                    print "get sr machines cache", sr_machines_key
                                    sr_machines = map_sr_machines[sr_machines_key]
                                else:
                                    retry = 5
                                    while retry > 0:
                                        try:
                                            sr_machines = self.tianjiAPI.ListInstanceServerroleMachinesInService(
                                                clusterName, serviceName, sr_name)
                                            if sr_machines:
                                                map_sr_machines[sr_machines_key] = sr_machines
                                                break
                                        except Exception as e:
                                            print e
                                            retry -= 1
                                            time.sleep(1)

                                # for sr debug
                                if self.debug:
                                    filename = "%s_%s_%s_sr_machines.json" % (clusterName, serviceName, sr_name)
                                    save_json_file(filename, sr_machines, True)

                                if sr_machines and sr_machines["ExpectedMachines"]:
                                    userContainerInfo = []
                                    for k in sr_machines["ExpectedMachines"]:
                                        sr_m = sr_machines["ExpectedMachines"][k]
                                        if sr_m["Hostname"] not in srgInfo["serverList"]:
                                            continue
                                        if_sr_in_srg = True
                                        if sr_m.get("DockerHostname"):
                                            userContainerInfo.append({
                                                "server": sr_m["Hostname"],
                                                "userContainerHostname": sr_m["DockerHostname"],
                                                "userContainerIp": sr_m["DockerIp"]
                                            })
                                    if len(userContainerInfo) > 0:
                                        serverRoleInfo["userContainerInfo"] = userContainerInfo
                                if if_sr_in_srg is True:
                                    srgInfo["serverRoleList"].append(serverRoleInfo)
                    srgList.append(srgInfo)
        else:
            print "warn, %s__%s, cluster.conf is none" % (projectName, clusterName)

        if len(srgList) == 0:
            print "error, %s__%s, srgs is none" % (projectName, clusterName)

        return srgList

    def _get_sr_build_id(self, clusterConfig, projectName, cluserName, serviceName, sr_name):
        sr_ids, errmsg = self.get_sr_version(clusterConfig, projectName, cluserName, serviceName, sr_name)
        if sr_ids and len(sr_ids) > 0:
            return sr_ids["*"]
        else:
            print "warn _get_sr_build_id fail,", projectName, cluserName, serviceName, sr_name, errmsg
            return ""

    def _get_sr_applications(self, clusterConfig, projectName, cluserName, serviceName, sr_name):
        app_rqs, errmsg = self.get_sr_resource_quota(clusterConfig, projectName, cluserName, serviceName, sr_name)
        if app_rqs and len(app_rqs) > 0:
            return app_rqs
        else:
            print "warn _get_sr_applications fail,", projectName, cluserName, serviceName, sr_name, errmsg
        return []

    def GetServerList(self, productList):
        self.vmHostList = self.GetVmHostList()
        serverList = []
        serverNameFilter = {}
        serverNameMapper = {}
        # 存储sys.conf避免每次都调用
        sysconfMapper = {}
        for pd in productList:
            pbName = pd["productName"]
            for clu in pd["clusterList"]:
                cluName = clu["clusterName"]
                clusterConfig, cvs = self.tianjiAPI.CheckoutCluster(pbName, cluName)
                # 解析clusterConfig，获得sys.conf部分
                serverListJson = clusterConfig.get("services")
                if "os" in serverListJson:
                    if "sys.conf" in serverListJson.get("os"):
                        sysconfMapper["%s.%s" % (pbName, cluName)] = serverListJson.get("os").get("sys.conf")
                    else:
                        sysconfMapper["%s.%s" % (pbName, cluName)] = ""

                for srg in clu["serverRoleGroupList"]:
                    srgName = srg["serverRoleGroup"]
                    for ser in srg["serverList"]:
                        serverNameFilter[ser] = True
                        serverNameMapper[ser] = "%s.%s.%s" % (pbName, cluName, srgName)

        serverNameMap = {}
        projectNames = self.GetProjectNames()
        for projectName in projectNames:
            print "---p", projectName
            bucket_list = self.tianjiAPI.ListMachineBucket(projectName)
            if not bucket_list:
                continue
            for bucket in bucket_list:
                machines = self.tianjiAPI.GetMachineBucket(projectName, bucket, "local")
                # _save_json_file(filename, machines, True)
                for name in machines:
                    attr = machines[name]["Attributes"]
                    machine_type = attr.get("machine_type_with_nic_type")
                    if not machine_type:
                        continue

                    hw_cpu = attr.get("hw_cpu")
                    hw_mem = attr.get("hw_mem")
                    hw_harddisk = attr.get("hw_harddisk")
                    resource_quota = json.dumps({
                        "cpu": hw_cpu and float(hw_cpu) or 0,
                        "memory": hw_mem and float(hw_mem) / 1024 or 0,
                        "diskSize": hw_harddisk and float(hw_harddisk) / 1024 or 0
                    })

                    srg_quota = "{}"
                    if attr.has_key("srg_quota"):
                        srg_quota = attr.get("srg_quota")
                    elif attr.has_key("reserved_quota") and attr.get("reserved_quota") != "":
                        srg_quota = attr.get("reserved_quota")
                    else:
                        srg_quota = resource_quota

                    spec = "{}"
                    if attr.has_key("spec"):
                        spec = attr.get("spec")

                    rack = attr.get("rack")
                    azone = attr.get("azone")
                    if self.azone != "":
                        azone = self.azone
                    if not serverNameFilter.has_key(str(attr["hostname"])):
                        continue
                    # 获取到这台机器所在的pd，clu，srg
                    info = serverNameMapper[name].split(".")
                    # 获取到所在的sys.conf
                    sysconf = sysconfMapper["%s.%s" % (info[0], info[1])]
                    os = ""
                    os_template = ""
                    part = ""
                    if "" != sysconf:
                        sysjson = json.loads(sysconf)
                        key = "OS#%s" % (info[2].replace('#', '__'))
                        # 设置os
                        if sysjson.has_key("os"):
                            if sysjson["os"].has_key(key):
                                os = sysjson["os"][key]
                            else:
                                os = sysjson["os"]["*"]
                        else:
                            print "无法读取到os信息,sysconf 内容为%s" % sysconf
                            exit(1)

                        # 设置os_template
                        if sysjson.has_key("app_name"):
                            if sysjson["app_name"].has_key(key):
                                os_template = sysjson["app_name"][key]
                            else:
                                os_template = sysjson["app_name"]["*"]
                        else:
                            print "无法读取到os_template(app_name)信息,sysconf 内容为%s" % sysconf
                            exit(1)

                        # 设置part,目前暂未使用
                        if sysjson.has_key("part"):
                            if sysjson["part"].has_key(key):
                                part = sysjson["part"][key]
                            else:
                                part = sysjson["part"]["*"]

                    if os == "" or os_template == "" or part == "":
                        print "os或者os_template或者part取不到信息，请确认：%s" % name

                    # if self.azone != "" and str(azone) != "" and self.azone != str(azone):
                    #     continue
                    rack_group = attr.get("rack_group")
                    expected_link = attr.get("expected_link")
                    mt = attr.get("sm_name")
                    if mt == "vm_ecs":
                        mt = "ECS"
                    serverInfo = {
                        "Attributes": {
                            "dev_function": attr.get("dev_function"),
                            "spec": spec,
                            "expected_link": expected_link and expected_link or "",
                            "hostname": attr["hostname"],
                            "idc": attr.get("idc"),
                            "ip": attr.get("ip"),
                            "machine_type": mt,
                            "machine_type_from_manufacturer": attr.get("machine_type_from_manufacturer"),
                            "machine_type_with_nic_type": attr.get("machine_type_with_nic_type"),
                            "node_group": attr.get("node_group"),
                            "oob_ip": attr.get("oob_ip"),
                            "os": os,
                            "os_template": os_template,
                            "part": part,
                            "parent_hostname": "",
                            "parent_sn": "",
                            "azone": azone,
                            "power": attr.get("power"),
                            "npod": attr.get("npod"),
                            "rack": rack and rack or "",
                            "rack_group": rack_group and rack_group or "",
                            "rack_position": attr.get("rack_sub_position"),
                            "rack_sub_position": attr.get("rack_sub_position"),
                            "rack_unit_id": attr.get("rack_unit_id"),
                            "rack_unit_mode": attr.get("rack_unit_mode"),
                            # "reserved_quota": attr.get("reserved_quota"),  # "{\"cpu\":0,\"diskSize\":0,\"memory\":0}",
                            "srg_quota": srg_quota,
                            "resource_quota": resource_quota,
                            "room": attr.get("room"),
                            "sn": attr.get("sn"),
                            "vm_host_tag": attr.get("vm_host_tag"),
                            "big_container_number": attr.get("big_container_number"),  # int  # 物理机上大容器上限的个数限制.
                            "use_big_container_number": attr.get("use_big_container_number"),  # int类型  # 大容器已使用的个数
                            "max_vm_number": attr.get("max_vm_number"),  # int类型  # 物理机上最大的kvm上限的个数限制.
                            "use_vm_number": attr.get("use_vm_number"),  # int 类型  # 已占用的kvm的个数.
                            "max_docker_number": attr.get("max_docker_number"),
                            "use_docker_number": attr.get("use_docker_number"),
                            "srg_docker_number": attr.get("srg_docker_number"),
                            "uplink_info": attr.get("uplink_info"),
                            "tj_project": attr.get("project"),
                            "tj_cluster": attr.get("cluster"),
                            "tj_bucket": attr.get("bucket")
                        },
                        # "Topology": machines[name]["Topology"]
                    }
                    serverNameMap[serverInfo["Attributes"]["hostname"]] = True
                    serverList.append(serverInfo)
        print "serverNameMap", serverNameMap
        print "serverNameFilter", serverNameFilter
        if len(serverList) == 0:
            print "found serverList is empty, may be input azone error: %s" % self.azone
            exit(1)
        return serverList, serverNameMap

    def GetVmHostInfoJson(self):
        projectName = "tianji"
        clusters = self.tianjiAPI.ListClusters(projectName)
        vm_host_info_json = {}
        for clusterName in clusters:
            clusterConfig, cvs = self.tianjiAPI.CheckoutCluster(projectName, clusterName)
            # filename = "cluster_%s#%s.json" % (projectName, clusterName)
            # _save_json_file(filename, clusterConfig, True)
            servicesConfig = clusterConfig.get("services")
            serviceInstance = "tianji"
            if servicesConfig and serviceInstance in servicesConfig and "user" in servicesConfig[serviceInstance]:
                if "vm_host_info.json" in servicesConfig[serviceInstance]["user"]:
                    vm_host_info_json_service = json.loads(
                        servicesConfig[serviceInstance]["user"]["vm_host_info.json"])
                    # filename = "vm_host_info.json"
                    # _save_json_file(filename, vm_host_info_json, True)
                    for key, value in vm_host_info_json_service.items():
                        if vm_host_info_json.has_key(key) and clusterName != "default":
                            continue
                        vm_host_info_json[key] = value
        return vm_host_info_json

    def GetVmHostList(self):
        vmHostMap = self.GetVmHostInfoJson()
        if not vmHostMap:
            print "error, GetVmHostInfoJson return none."
            exit(1)
        vmHostList = []
        hyperServerMap = {}
        for vm in vmHostMap:
            host = vmHostMap[vm]
            if host in vmHostList:
                continue
            else:
                vmHostList.append(host)
        return vmHostList

    # region下不需要考虑vm_host_info对az的影响
    def GetHyperServerMap(self, serverNameMap):
        vmHostMap = self.GetVmHostInfoJson()
        if not vmHostMap:
            print "error, GetVmHostInfoJson return none."
            exit(1)
        hyperServerMap = {}
        for vm in vmHostMap:
            vmHost = vmHostMap[vm]
            hyper = hyperServerMap.get(vmHost)
            if hyper is None:
                hyper = {
                    "server": vmHost,
                    "vServerList": []
                }
            if serverNameMap.has_key(vm):
                hyper["vServerList"].append(vm)
            hyperServerMap[vmHost] = hyper

        hyperServerMapList = [hyperServerMap[vmhost] for vmhost in hyperServerMap if
                              len(hyperServerMap[vmhost]["vServerList"]) > 0]
        return hyperServerMapList

    def GetZhuqueTianjiJson(self):
        # 提前ipPool是为了防止文件不存在
        if self.ippool:
            self.output["ipPoolContent"] = self.GetIpPoolContent()
        self.output["productList"], self.output["globalConfig"], self.output[
            "globalClusterInfo"] = self.GetProductList()
        self.output["serverList"], serverNameMap = self.GetServerList(self.output["productList"])
        self.output["hyperServerMap"] = self.GetHyperServerMap(serverNameMap)

        return self.output

    def SaveZhuqueTianjiJsonFile(self, outfile="zhuque2tj.json"):
        if not self.output.has_key("productList"):
            self.GetZhuqueTianjiJson()
        save_json_file(outfile, self.output, True)

    def GetIpPoolContent(self):
        return self.getIpPlanFileContent()

    def get_sr_version(self, cluster_config, project_name, cluster_name, service_name, sr_name):
        services_config = cluster_config.get("services", {})
        if service_name not in services_config:
            return {}, "no such service"
        service_config = services_config.get(service_name)
        if "version.conf" in service_config:
            version_config = yaml.load(service_config["version.conf"])
            versions = version_config.get("Versions", {})
            if not sr_name.endswith(("#")):
                sr_name = "%s#" % (sr_name)
            sr_config = versions.get(sr_name, {})
            sr_apps = sr_config.get("Applications", {})
            for key in sr_apps:
                lst = sr_apps[key].split("#")
                sr_apps[key] = lst[1].strip()
            return sr_apps, ""
        elif "template.conf" in service_config:
            conf_json = yaml.load(service_config["template.conf"])
            base_conf_json = conf_json.get("BaseTemplate")
            template_name = base_conf_json.get("TemplateName")
            template_version = base_conf_json.get("Version")
            # template_content = self.tianjiAPI.GetServiceTemplate(service_name, template_name)
            template_content = None
            retry = 5
            while retry > 0:
                try:
                    template_content = self.tianjiAPI.GetServiceTemplate(service_name, template_name)
                    if template_content:
                        break
                except Exception as e:
                    print e
                    retry -= 1
                    time.sleep(1)
            if "version.conf" in template_content:
                version_config = yaml.load(template_content["version.conf"])
                versions = version_config.get("Versions", {})
                if not sr_name.endswith(("#")):
                    sr_name = "%s#" % (sr_name)
                sr_config = versions.get(sr_name, {})
                sr_apps = sr_config.get("Applications", {})
                for key in sr_apps:
                    lst = sr_apps[key].split("#")
                    sr_apps[key] = lst[1].strip()
                return sr_apps, ""
        else:
            return {}, "not found"

    def get_sr_resource_quota(self, cluster_config, project_name, cluster_name, service_name, sr_name):
        result = []
        services_config = cluster_config.get("services", {})
        if service_name not in services_config:
            return [], "no such service"
        service_config = services_config.get(service_name)
        if "tianji" in service_config and "resource_quota.json" in service_config["tianji"]:
            resource_config = yaml.load(service_config["tianji"]["resource_quota.json"])
            quotas = resource_config.get("ResourceQuotas", {})
            sr_quotas = quotas.get("ServerRoles", {})
            if not sr_name.endswith(("#")):
                sr_name = "%s#" % (sr_name)
            sr_quota = sr_quotas.get(sr_name, {})
            for app, quota in sr_quota.get("Applications", {}).items():
                tmpDict = {}
                tmpDict["name"] = app
                tmpDict["resourceQuota"] = quota
                result.append(tmpDict)
            return result, ""
        else:
            return [], "not found"

    # def getIpPlanFileContent(self):
    #     project, tianjiClusterName = self.getTianjiProjectAndCluster()
    #     yamlDictForTool = {}
    #     usedIps = self.getUsedIpFromTianji(tianjiClusterName)
    #     tianjiClusterConf, baseVersion = self.tianjiAPI.CheckoutCluster(project, tianjiClusterName)
    #     if tianjiClusterConf.has_key("kv.conf"):
    #         kvConfDict = yaml.load(tianjiClusterConf["kv.conf"])
    #         yamlDictForTool = yaml.load(yaml.load(kvConfDict["KeyValues"].get("dockerNetworks", {})))
    #         for asw, aswInfo in yamlDictForTool.items():
    #             for item in aswInfo:
    #                 item["cidr"] = item.get("subnet")
    #                 item.pop("subnet")
    #                 item.pop("netdev")
    #                 item["type"] = "kvm_docker"
    #         tmpFile = tempfile.TemporaryFile()
    #         yaml.dump(yamlDictForTool, tmpFile)
    #         tmpFile.seek(0)
    #         content = tmpFile.read()
    #         tmpFile.close()
    #         self.ipToolForAsw = zhuque_ip_pool.ZhuqueIpPool(content)
    #         asw2Ips = {}
    #         for ip in usedIps:
    #             asw, type = self.ipToolForAsw.GetAswIdAndTypeByIp(ip)
    #             if asw and asw.strip() in yamlDictForTool:
    #                 asw2Ips.setdefault(asw, []).append(ip)
    #         for asw, aswInfo in yamlDictForTool.items():
    #             if asw in asw2Ips:
    #                 yamlDictForTool[asw][0]["used"] = ",".join(asw2Ips[asw])
    #     tmpFile = tempfile.TemporaryFile()
    #     yaml.dump(yamlDictForTool, tmpFile)
    #     tmpFile.seek(0)
    #     content = tmpFile.read()
    #     tmpFile.close()
    #     return content

    def getIpPlanFileContent(self):
        print "IP全量冲突检查（逐个ping的方式，3~10分钟左右）"
        # 改为直接从朱雀conf/aZone*_ip_pool.yml读取ipPlan信息
        zhuqueConfigPath = os.path.dirname(os.path.realpath(__file__)) + "/../conf"
        zhuqueIpPoolFile = zhuqueConfigPath + "/%s_ip_pool.yml" % self.azone
        content = ""
        if os.path.isfile(zhuqueIpPoolFile):
            file = open(zhuqueIpPoolFile)
            try:
                content = file.read()
                self.ipToolForAsw = zhuque_ip_pool.ZhuqueIpPool(content)
                data = self.ipToolForAsw.GetIpPoolData()

                for asw, aswInfo in data.items():
                    for i in range(len(aswInfo)):
                        used_list = data[asw][i]["used"]
                        data[asw][i]["used"] = ",".join(used_list)
                        data[asw][i].pop("pool")
                content = yaml.dump(data)
            except Exception as e:
                print e.message
                print traceback.format_exc()
            finally:
                file.close()
        else:
            print "%s 文件不存在，请检查" % zhuqueIpPoolFile
            exit(1)
        return content

    def getUsedIpFromTianji(self, tianjiClusterName):
        # get the ip that is already used by tianji
        usedIps = []
        dockerUsedIp = []
        for project in self.tianjiAPI.ListProjects():
            for cluster in self.tianjiAPI.ListClusters(project):
                clusterConf, baseVersion = self.tianjiAPI.CheckoutCluster(project, cluster)
                if clusterConf.has_key("services"):
                    for service in clusterConf["services"]:
                        if clusterConf["services"][service].has_key("role.conf"):
                            roleconf = yaml.load(clusterConf["services"][service]["role.conf"])
                            if roleconf.has_key("ServerRoles"):
                                for role in roleconf["ServerRoles"]:
                                    for instance in roleconf["ServerRoles"][role]:
                                        if len(instance.split(':')) > 1:
                                            dockerUsedIp.append(instance.split(':')[1])
        vmUsedIpList = []
        project = self.tianjiAPI.GetClusterProject(tianjiClusterName)
        tianjiClusterConf, baseVersion = self.tianjiAPI.CheckoutCluster(project, tianjiClusterName)
        if tianjiClusterConf.has_key("services"):
            if tianjiClusterConf["services"].has_key("tianji"):
                if tianjiClusterConf["services"]["tianji"].has_key("user"):
                    if tianjiClusterConf["services"]["tianji"]["user"]:
                        if tianjiClusterConf["services"]["tianji"]["user"].has_key("vm_host_info.json"):
                            for hostname in yaml.load(
                                    tianjiClusterConf["services"]["tianji"]["user"]["vm_host_info.json"]):
                                try:
                                    vmUsedIpList.append(self.tianjiAPI.GetMachineInfo(hostname, "ip")["ip"])
                                except Exception:
                                    print hostname, "not exists"
        usedIps.extend(dockerUsedIp)
        usedIps.extend(vmUsedIpList)
        return usedIps

    def getTianjiProjectAndCluster(self):
        tianjiProject = ""
        tianjiCluster = ""
        for project in self.tianjiAPI.ListProjects():
            for cluster in self.tianjiAPI.ListClusters(project):
                clusterConf, baseVersion = self.tianjiAPI.CheckoutCluster(project, cluster)
                servicesConfig = {}
                if "services" in clusterConf:
                    servicesConfig = clusterConf.get("services", {})
                tianjiServiceConfig = {}
                if "tianji" in servicesConfig:
                    tianjiServiceConfig = servicesConfig.get("tianji", {})
                roleConfDict = {}
                if "role.conf" in tianjiServiceConfig:
                    roleConfDict = yaml.load(tianjiServiceConfig["role.conf"])
                serverRoleDict = {}
                if "ServerRoles" in roleConfDict:
                    serverRoleDict = roleConfDict.get("ServerRoles", {})
                if "TianjiMaster#" in serverRoleDict:
                    tianjiProject = project
                    tianjiCluster = cluster
        return tianjiProject, tianjiCluster


def printJson(obj):
    print json.dumps(obj, indent=4)


def save_file(filename, data, overwrite=False, comment=""):
    if not os.path.exists(os.path.dirname(filename)) and os.path.dirname(filename) != "":
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    if overwrite or os.path.exists(filename) is False:
        print("[%s]_save_json_file: %s" % (comment, filename))
        f = open(filename, 'w')
        f.write(data)
        f.flush()
        f.close()
    elif os.path.exists(filename):
        print("warn, [%s]_save_json_file: %s, it is exists. " % (comment, filename))


def save_json_file(filename, data, overwrite=False, comment=""):
    if not os.path.exists(os.path.dirname(filename)) and os.path.dirname(filename) != "":
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    if overwrite or os.path.exists(filename) is False:
        print("[%s]_save_json_file: %s" % (comment, filename))
        f = open(filename, 'w')
        f.write(json.dumps(data, indent=4))
        f.flush()
        f.close()
    elif os.path.exists(filename):
        print("warn, [%s]_save_json_file: %s, it is exists. " % (comment, filename))


def run_cmd(cmd, tranfer2json=False):
    s, r = commands.getstatusoutput(cmd)
    print s, r
    if s > 0:
        print ("error,run cmd: %s, cause: %s, exit %d" % (cmd, r, s))
        exit(s)
    if tranfer2json:
        data = json.loads(r)
        return data
    else:
        return r


def _printJson(obj):
    print json.dumps(obj, indent=4)


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Unsupported value encountered.')


if __name__ == "__main__":
    isOldFormat = True
    for arg in sys.argv:
        if str(arg).startswith("-"):
            isOldFormat = False

    if isOldFormat:
        print "old input format"
        configPath = sys.argv[1]
        azone = len(sys.argv) > 2 and str(sys.argv[2]) or ""
        onlyProjectNames = []
        tjGetter = ZhuqueTianjiGetter(configPath, azone)
        tjGetter.SaveZhuqueTianjiJsonFile()
    else:
        print "new input format"
        print "功能: 通过tianji_clt调用天基API还原朱雀规划的终态文件（zhuque2tj.json)"
        parser = argparse.ArgumentParser(sys.argv[0])
        parser.add_argument("-c", "--tianji_clt_conf", required=False, default="./tianji_clt.conf")
        parser.add_argument("-z", "--azone", required=True)
        parser.add_argument("-F", "--onlyProjectNames", required=False, default=[])
        parser.add_argument("-o", "--outfile", required=False, default="./zhuque2tj.json")
        parser.add_argument("-x", "--action", required=False, default="")
        parser.add_argument("-d", "--debug", required=False, default=False, type=str2bool)
        parser.add_argument("-i", "--ippool", required=False, default=False, type=str2bool)
        ar = parser.parse_args()

        tjGetter = ZhuqueTianjiGetter(ar.tianji_clt_conf, ar.azone, ar.onlyProjectNames, ar.debug, ar.ippool)
        if ar.action == "":
            tjGetter.SaveZhuqueTianjiJsonFile(ar.outfile)
        elif ar.action == "projects":
            print tjGetter.GetProjectNames()
