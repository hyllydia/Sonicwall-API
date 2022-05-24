#coding:utf-8
#Data-Body
#AO Subnet
path_AO='/address-objects/ipv4'
path_VPN='/vpn/policies/ipv4/site-to-site'
path_Auth='/auth'
path_Commit='/config/pending'
path_vlan_interfaces='/interfaces/ipv4'
path_sdwan_groups='/sdwan/groups'
path_sdwan_probes='/sdwan/sla-probes/ipv4'
path_sdwan_paths='/sdwan/path-selection-profiles'
#Add route policies
path_sdwan_rules='/route-policies/ipv4'
path_tunnel_vpn='/vpn/policies/ipv4/tunnel-interface'
path_tunnel_vpn_interface='/tunnel-interfaces/vpn'
AO_Subnet={
    "address_objects":
        [
            {
                "ipv4":
                 {
                "name": "ixia_2",
                "zone": "VPN",
                "network": {
                    "subnet": "31.1.2.0",
                    "mask": "255.255.255.0"
                }
            }
        }
    ]
}
#AO Host
AO_Host={
  "address_objects": [
    {
      "ipv4": {
        "name": "des",
        "zone": "LAN",
        "host": {"ip":"17.1.1.1"}
      }
    }
  ]
}
#Vlan_interfaces
Vlan_interfaces={
    "interfaces":[
        {
            "ipv4":{
                "name":"X28",
                "vlan":3003,
                "ip_assignment":{
                    "zone":"WAN",
                    "mode":{
                        "static":{
                            "ip":"31.111.3.2",
                            "netmask":"255.255.255.0",
                            "dns":{
                                "primary":"0.0.0.0",
                                "secondary":"0.0.0.0",
                                "tertiary":"0.0.0.0"
                            },
                        "gateway":""
                        }
                    }
                },
                "comment":"",
                "management":{
                    "https":True,
                    "ping":True,
                    "snmp":False,
                    "ssh":False,
                    "fqdn_assignment":""
                },
                "user_login":{
                    "http":False,
                    "https":False},
                "https_redirect":True,
                "mac":{"default":True},
                "flow_reporting":True,
                "multicast":False,
                "exclude_route":False,
                "asymmetric_route":False,
                "mtu":1500,
                "fragment_packets":True,
                "ignore_df_bit":False,
                "send_icmp_fragmentation":True
            }
        }
    ]
}
#Group VPN
Grp_vpn={
    "vpn": {
        "policy": [
            {
                "ipv4": {
                    "group_vpn": {
                        "name": "Group_VPN_Pol_3",
                        "enable": False,
                        "auth_method": {
                            "shared_secret": {
                                "shared_secret": "sonicwall2010"
                            }
                        },
                        "proposal": {
                            "ike": {
                                "encryption": "triple-des",
                                "authentication": "sha-1",
                                "dh_group": "2",
                                "lifetime": 28800
                            },
                            "ipsec": {
                                "protocol": "esp",
                                "encryption": {
                                    "triple_des": True
                                },
                                "authentication": {
                                    "sha_1": True
                                },
                                "perfect_forward_secrecy": {},
                                "lifetime": 28800
                            }
                        },
                        "anti_replay": True,
                        "multicast": False,
                        "management": {
                            "https": False,
                            "ssh": False,
                            "snmp": False
                        },
                        "accept_multiple_proposals": False,
                        "default_lan_gateway": "0.0.0.0",
                        "client": {
                            "cache_xauth": "never",
                            "virtual_adaptor": "none",
                            "allow_connections_to": "split-tunnels",
                            "default_route": {},
                            "simple_provisioning": False
                        },
                        "client_authentication": {
                            "require_xauth": "Trusted Users"
                        },
                        "ike_mode_configuration": {}
                    }
                }
            }
        ]
    }
}
#VPN IKEv2
VPN_IKEv2={
    "vpn": {
        "policy": [
            {
                "ipv4": {
                    "site_to_site": {
                        "name": "VPNPeer_2",
                        "enable": True,
                        "gateway": {
                            "primary": "8.2.1.3",
                            "secondary": "0.0.0.0"
                        },
                        "auth_method": {
                            "shared_secret": {
                                "shared_secret": "sonicwall2010",
                                "ike_id": {
                                    "local": {
                                        "ipv4": "0.0.0.0"
                                    },
                                    "peer": {
                                        "ipv4": "0.0.0.0"
                                    }
                                }
                            }
                        },
                        "network": {
                            "local": {
                                "name": "X20 Subnet"
                            },
                            "remote": {
                                "destination_network": {
                                    "name": "31.1.3.0"
                                }
                            }
                        },
                        "proposal": {
                            "ike": {
                                "exchange": "ikev2",
                                "encryption": "aes-128",
                                "authentication": "sha-1",
                                "dh_group": "2",
                                "lifetime": 288000
                            },
                            "ipsec": {
                                "protocol": "esp",
                                "encryption": {
                                    "aes_128": True
                                },
                                "authentication": {
                                    "sha_1": True
                                },
                                "perfect_forward_secrecy": {},
                                "lifetime": 288000
                            }
                        },
                        "netbios": False,
                        "anti_replay": True,
                        "multicast": False,
                        "management": {
                            "https": False,
                            "ssh": False,
                            "snmp": False
                        },
                        "keep_alive": False,
                        "user_login": {
                            "http": False,
                            "https": False
                        },
                        "default_lan_gateway": "0.0.0.0",
                        "bound_to": {
                            "zone": "WAN"
                        },
                        "suppress_trigger_packet": True,
                        "accept_hash": False,
                        "send_hash": "",
                        "suppress_auto_add_rule": True,
                        "apply_nat": False,
                        "translated_network": {
                            "local": {},
                            "remote": {}
                        }
                    }
                }
            }
        ]
    }
}
#VPN_Chained_3rd
VPN_Chained_3rd={
    "vpn": {
        "policy": [
            {
                "ipv4": {
                    "site_to_site": {
                        "name": "test",
                        "enable": True,
                        "gateway": {
                            "primary": "172.100.1.1",
                            "secondary": "0.0.0.0"
                        },
                        "auth_method": {
                            "certificate": {
                                "certificate": "xx",
                                "ike_id": {
                                    "local": "email-id",
                                    "peer": {
                                        "email_id": "ixia@ixiacom.com"
                                    }
                                }
                            }
                        },
                        "network": {
                            "local": {
                                "name": "X20 Subnet"
                            },
                            "remote": {
                                "destination_network": {
                                    "name": "remote"
                                }
                            }
                        },
                        "proposal": {
                            "ike": {
                                "exchange": "ikev2",
                                "encryption": "aes-128",
                                "authentication": "sha-1",
                                "dh_group": "2",
                                "lifetime": 28800
                            },
                            "ipsec": {
                                "protocol": "esp",
                                "encryption": {
                                    "aes_128": True
                                },
                                "authentication": {
                                    "sha_1": True
                                },
                                "perfect_forward_secrecy": {},
                                "lifetime": 28800
                            }
                        },
                        "netbios": False,
                        "anti_replay": True,
                        "multicast": False,
                        "ocsp_checking": False,
                        "responder_url": "",
                        "management": {
                            "https": False,
                            "ssh": False,
                            "snmp": False
                        },
                        "keep_alive": False,
                        "user_login": {
                            "http": False,
                            "https": False
                        },
                        "default_lan_gateway": "0.0.0.0",
                        "bound_to": {
                            "zone": "WAN"
                        },
                        "suppress_trigger_packet": True,
                        "accept_hash": False,
                        "send_hash": "",
                        "suppress_auto_add_rule": False,
                        "apply_nat": False,
                        "translated_network": {
                            "local": {},
                            "remote": {}
                        }
                    }
                }
            }
        ]
    }
}
#Access Rule
Access_Rule={
    "access_rules": [
{
            "ipv4": {
                "uuid": "00000000-0000-0015-0700-2cb8ed9d80d0",
                "name": "My Rule02",
                "enable": True,
                "auto_rule": False,
                "from": "any",
                "to": "any",
                "action": "deny",
                "source": {
                    "address": {
                        "name": "acc-src-1"
                    },
                    "port": {
                        "any": True
                    }
                },
                "service": {
                    "name": "BGP"
                },
                "destination": {
                    "address": {
                        "name": "acc-des-1"
                    }
                },
                "schedule": {
                    "always_on": True
                },
                "users": {
                    "included": {
                        "all": True
                    },
                    "excluded": {
                        "none": True
                    }
                },
                "comment": "",
                "fragments": True,
                "logging": True,
                "sip": False,
                "h323": False,
                "flow_reporting": False,
                "botnet_filter": False,
                "geo_ip_filter": {
                    "enable": False,
                    "global": True
                },
                "block": {
                    "countries": {
                        "unknown": False
                    }
                },
                "packet_monitoring": False,
                "management": False,
                "max_connections": 100,
                "priority": {
                    "auto": True
                },
                "tcp": {
                    "timeout": 15,
                    "urgent": False
                },
                "udp": {
                    "timeout": 30
                },
                "connection_limit": {
                    "source": {},
                    "destination": {}
                },
                "dpi": True,
                "dpi_ssl": {
                    "client": True,
                    "server": True
                },
                "redirect_unauthenticated_users_to_log_in": True,
                "quality_of_service": {
                    "class_of_service": {},
                    "dscp": {
                        "preserve": True
                    }
                }
            }
        },
	{
            "ipv4": {
                "uuid": "00000000-0000-0015-0700-2cb8ed9d80d0",
                "name": "My Rule02",
                "enable": True,
                "auto_rule": False,
                "from": "any",
                "to": "any",
                "action": "deny",
                "source": {
                    "address": {
                        "name": "acc-src-1"
                    },
                    "port": {
                        "any": True
                    }
                },
                "service": {
                    "name": "HTTP"
                },
                "destination": {
                    "address": {
                        "name": "acc-des-1"
                    }
                },
                "schedule": {
                    "always_on": True
                },
                "users": {
                    "included": {
                        "all": True
                    },
                    "excluded": {
                        "none": True
                    }
                },
                "comment": "",
                "fragments": True,
                "logging": True,
                "sip": False,
                "h323": False,
                "flow_reporting": False,
                "botnet_filter": False,
                "geo_ip_filter": {
                    "enable": False,
                    "global": True
                },
                "block": {
                    "countries": {
                        "unknown": False
                    }
                },
                "packet_monitoring": False,
                "management": False,
                "max_connections": 100,
                "priority": {
                    "auto": True
                },
                "tcp": {
                    "timeout": 15,
                    "urgent": False
                },
                "udp": {
                    "timeout": 30
                },
                "connection_limit": {
                    "source": {},
                    "destination": {}
                },
                "dpi": True,
                "dpi_ssl": {
                    "client": True,
                    "server": True
                },
                "redirect_unauthenticated_users_to_log_in": True,
                "quality_of_service": {
                    "class_of_service": {},
                    "dscp": {
                        "preserve": True
                    }
                }
            }
        },
	{
            "ipv4": {
                "uuid": "00000000-0000-0015-0700-2cb8ed9d80d0",
                "name": "My Rule02",
                "enable": True,
                "auto_rule": False,
                "from": "any",
                "to": "any",
                "action": "deny",
                "source": {
                    "address": {
                        "name": "acc-src-1"
                    },
                    "port": {
                        "any": True
                    }
                },
                "service": {
                    "name": "HTTPS"
                },
                "destination": {
                    "address": {
                        "name": "acc-des-1"
                    }
                },
                "schedule": {
                    "always_on": True
                },
                "users": {
                    "included": {
                        "all": True
                    },
                    "excluded": {
                        "none": True
                    }
                },
                "comment": "",
                "fragments": True,
                "logging": True,
                "sip": False,
                "h323": False,
                "flow_reporting": False,
                "botnet_filter": False,
                "geo_ip_filter": {
                    "enable": False,
                    "global": True
                },
                "block": {
                    "countries": {
                        "unknown": False
                    }
                },
                "packet_monitoring": False,
                "management": False,
                "max_connections": 100,
                "priority": {
                    "auto": True
                },
                "tcp": {
                    "timeout": 15,
                    "urgent": False
                },
                "udp": {
                    "timeout": 30
                },
                "connection_limit": {
                    "source": {},
                    "destination": {}
                },
                "dpi": True,
                "dpi_ssl": {
                    "client": True,
                    "server": True
                },
                "redirect_unauthenticated_users_to_log_in": True,
                "quality_of_service": {
                    "class_of_service": {},
                    "dscp": {
                        "preserve": True
                    }
                }
            }
        },
	{
            "ipv4": {
                "uuid": "00000000-0000-0015-0700-2cb8ed9d80d0",
                "name": "My Rule02",
                "enable": True,
                "auto_rule": False,
                "from": "any",
                "to": "any",
                "action": "deny",
                "source": {
                    "address": {
                        "name": "acc-src-1"
                    },
                    "port": {
                        "any": True
                    }
                },
                "service": {
                    "name": "LDAP"
                },
                "destination": {
                    "address": {
                        "name": "acc-des-1"
                    }
                },
                "schedule": {
                    "always_on": True
                },
                "users": {
                    "included": {
                        "all": True
                    },
                    "excluded": {
                        "none": True
                    }
                },
                "comment": "",
                "fragments": True,
                "logging": True,
                "sip": False,
                "h323": False,
                "flow_reporting": False,
                "botnet_filter": False,
                "geo_ip_filter": {
                    "enable": False,
                    "global": True
                },
                "block": {
                    "countries": {
                        "unknown": False
                    }
                },
                "packet_monitoring": False,
                "management": False,
                "max_connections": 100,
                "priority": {
                    "auto": True
                },
                "tcp": {
                    "timeout": 15,
                    "urgent": False
                },
                "udp": {
                    "timeout": 30
                },
                "connection_limit": {
                    "source": {},
                    "destination": {}
                },
                "dpi": True,
                "dpi_ssl": {
                    "client": True,
                    "server": True
                },
                "redirect_unauthenticated_users_to_log_in": True,
                "quality_of_service": {
                    "class_of_service": {},
                    "dscp": {
                        "preserve": True
                    }
                }
            }
        },
        {
            "ipv4": {
                "uuid": "00000000-0000-0015-0700-2cb8ed9d80d0",
                "name": "My Rule02",
                "enable": True,
                "auto_rule": False,
                "from": "any",
                "to": "any",
                "action": "deny",
                "source": {
                    "address": {
                        "name": "acc-src-1"
                    },
                    "port": {
                        "any": True
                    }
                },
                "service": {
                    "name": "IDENT"
                },
                "destination": {
                    "address": {
                        "name": "acc-des-1"
                    }
                },
                "schedule": {
                    "always_on": True
                },
                "users": {
                    "included": {
                        "all": True
                    },
                    "excluded": {
                        "none": True
                    }
                },
                "comment": "",
                "fragments": True,
                "logging": True,
                "sip": False,
                "h323": False,
                "flow_reporting": False,
                "botnet_filter": False,
                "geo_ip_filter": {
                    "enable": False,
                    "global": True
                },
                "block": {
                    "countries": {
                        "unknown": False
                    }
                },
                "packet_monitoring": False,
                "management": False,
                "max_connections": 100,
                "priority": {
                    "auto": True
                },
                "tcp": {
                    "timeout": 15,
                    "urgent": False
                },
                "udp": {
                    "timeout": 30
                },
                "connection_limit": {
                    "source": {},
                    "destination": {}
                },
                "dpi": True,
                "dpi_ssl": {
                    "client": True,
                    "server": True
                },
                "redirect_unauthenticated_users_to_log_in": True,
                "quality_of_service": {
                    "class_of_service": {},
                    "dscp": {
                        "preserve": True
                    }
                }
            }
        },
        {
            "ipv4": {
                "uuid": "00000000-0000-0015-0700-2cb8ed9d80d0",
                "name": "My Rule02",
                "enable": True,
                "auto_rule": False,
                "from": "any",
                "to": "any",
                "action": "deny",
                "source": {
                    "address": {
                        "name": "acc-src-1"
                    },
                    "port": {
                        "any": True
                    }
                },
                "service": {
                    "name": "GRE"
                },
                "destination": {
                    "address": {
                        "name": "acc-des-1"
                    }
                },
                "schedule": {
                    "always_on": True
                },
                "users": {
                    "included": {
                        "all": True
                    },
                    "excluded": {
                        "none": True
                    }
                },
                "comment": "",
                "fragments": True,
                "logging": True,
                "sip": False,
                "h323": False,
                "flow_reporting": False,
                "botnet_filter": False,
                "geo_ip_filter": {
                    "enable": False,
                    "global": True
                },
                "block": {
                    "countries": {
                        "unknown": False
                    }
                },
                "packet_monitoring": False,
                "management": False,
                "max_connections": 100,
                "priority": {
                    "auto": True
                },
                "tcp": {
                    "timeout": 15,
                    "urgent": False
                },
                "udp": {
                    "timeout": 30
                },
                "connection_limit": {
                    "source": {},
                    "destination": {}
                },
                "dpi": True,
                "dpi_ssl": {
                    "client": True,
                    "server": True
                },
                "redirect_unauthenticated_users_to_log_in": True,
                "quality_of_service": {
                    "class_of_service": {},
                    "dscp": {
                        "preserve": True
                    }
                }
            }
        },
        {
            "ipv4": {
                "uuid": "00000000-0000-0015-0700-2cb8ed9d80d0",
                "name": "My Rule02",
                "enable": True,
                "auto_rule": False,
                "from": "any",
                "to": "any",
                "action": "deny",
                "source": {
                    "address": {
                        "name": "acc-src-1"
                    },
                    "port": {
                        "any": True
                    }
                },
                "service": {
                    "name": "DRP"
                },
                "destination": {
                    "address": {
                        "name": "acc-des-1"
                    }
                },
                "schedule": {
                    "always_on": True
                },
                "users": {
                    "included": {
                        "all": True
                    },
                    "excluded": {
                        "none": True
                    }
                },
                "comment": "",
                "fragments": True,
                "logging": True,
                "sip": False,
                "h323": False,
                "flow_reporting": False,
                "botnet_filter": False,
                "geo_ip_filter": {
                    "enable": False,
                    "global": True
                },
                "block": {
                    "countries": {
                        "unknown": False
                    }
                },
                "packet_monitoring": False,
                "management": False,
                "max_connections": 100,
                "priority": {
                    "auto": True
                },
                "tcp": {
                    "timeout": 15,
                    "urgent": False
                },
                "udp": {
                    "timeout": 30
                },
                "connection_limit": {
                    "source": {},
                    "destination": {}
                },
                "dpi": True,
                "dpi_ssl": {
                    "client": True,
                    "server": True
                },
                "redirect_unauthenticated_users_to_log_in": True,
                "quality_of_service": {
                    "class_of_service": {},
                    "dscp": {
                        "preserve": True
                    }
                }
            }
        },
	{
            "ipv4": {
                "uuid": "00000000-0000-0015-0700-2cb8ed9d80d0",
                "name": "My Rule02",
                "enable": True,
                "auto_rule": False,
                "from": "any",
                "to": "any",
                "action": "deny",
                "source": {
                    "address": {
                        "name": "acc-src-1"
                    },
                    "port": {
                        "any": True
                    }
                },
                "service": {
                    "name": "FTP"
                },
                "destination": {
                    "address": {
                        "name": "acc-des-1"
                    }
                },
                "schedule": {
                    "always_on": True
                },
                "users": {
                    "included": {
                        "all": True
                    },
                    "excluded": {
                        "none": True
                    }
                },
                "comment": "",
                "fragments": True,
                "logging": True,
                "sip": False,
                "h323": False,
                "flow_reporting": False,
                "botnet_filter": False,
                "geo_ip_filter": {
                    "enable": False,
                    "global": True
                },
                "block": {
                    "countries": {
                        "unknown": False
                    }
                },
                "packet_monitoring": False,
                "management": False,
                "max_connections": 100,
                "priority": {
                    "auto": True
                },
                "tcp": {
                    "timeout": 15,
                    "urgent": False
                },
                "udp": {
                    "timeout": 30
                },
                "connection_limit": {
                    "source": {},
                    "destination": {}
                },
                "dpi": True,
                "dpi_ssl": {
                    "client": True,
                    "server": True
                },
                "redirect_unauthenticated_users_to_log_in": True,
                "quality_of_service": {
                    "class_of_service": {},
                    "dscp": {
                        "preserve": True
                    }
                }
            }
        }
		
    ]
}
#SDWAN_groups
sdwan_groups={
    "sdwan": {
        "group": [
            {
                "name": "sdwan-group1",
                "interface": [
                    {
                        "name": "X28:V3002",
                        "priority": 1
                    },
                    {
                        "name": "X28:V3001",
                        "priority": 2
                    }
                ]
            }
        ]
    }
}
#SDWAN_probes
sdwan_probes={
    "sdwan": {
        "sla_probe": [
            {
                "ipv4": {
                    "name": "sdwna_probe1",
                    "comment": "",
                    "sdwan_group": "sdwan_group1",
                    "probe": {
                        "target": {
                            "name": "31.112.1.1"
                        },
                        "type": {
                            "ping": {
                                "explicit": True
                            }
                        },
                        "interval": 3
                    },
                    "reply_timeout": 1,
                    "interval": {
                        "missed": 3,
                        "successful": 1
                    }
                }
            },
            {
                "ipv4": {
                    "name": "sdwan_probe2",
                    "comment": "",
                    "sdwan_group": "sdwan-group1",
                    "probe": {
                        "target": {
                            "name": "31.112.1.1"
                        },
                        "type": {
                            "tcp": {
                                "explicit": True,
                                "port": 80
                            }
                        },
                        "interval": 3
                    },
                    "reply_timeout": 1,
                    "interval": {
                        "missed": 3,
                        "successful": 1
                    },
                    "rst_as_miss": True
                }
            }
        ]
    }
}
#sdwan_path
sdwan_paths={
    "sdwan": {
        "path_selection_profile": [
            {
                "name": "sdwan-path1",
                "sdwan_group": "sdwan-group1",
                "sla_probe": "sdwna_probe1",
                "sla_class": "Lowest Latency",
                "backup_interface": "",
                "probe_default_up": True,
                "reset_connections": False
            },
            {
                "name": "sdwan-path2",
                "sdwan_group": "sdwan-group1",
                "sla_probe": "sdwna_probe1",
                "sla_class": "Lowest Packet Loss",
                "backup_interface": "",
                "probe_default_up": True,
                "reset_connections": False
            },
            {
                "name": "sdwan-path3",
                "sdwan_group": "sdwan-group1",
                "sla_probe": "sdwna_probe1",
                "sla_class": "Lowest Jitter",
                "backup_interface": "",
                "probe_default_up": True,
                "reset_connections": False
            }
        ]
    }
}
#sdwan_vpn_paths
sdwan_vpn_paths={
    "sdwan": {
        "path_selection_profile": [
            {
                "name": "sdwan_vpan_path1",
                "sdwan_group": "sdwan_vpn_group1",
                "sla_probe": "VPN Probe - sdwan_vpn_group1",
                "sla_class": "Lowest Latency",
                "backup_interface": "",
                "probe_default_up": True
            },
            {
                "name": "sdwan_vpan_path1",
                "sdwan_group": "sdwan_vpn_group1",
                "sla_probe": "VPN Probe - sdwan_vpn_group1",
                "sla_class": "Lowest Packet Loss",
                "backup_interface": "",
                "probe_default_up": True
            },
            {
                "name": "sdwan-path3",
                "sdwan_group": "sdwan-group1",
                "sla_probe": "sdwna_probe1",
                "sla_class": "Lowest Jitter",
                "backup_interface": "",
                "probe_default_up": True,
            }
        ]
    }
}
#sdwan_rules
sdwan_rules={
    "route_policies": [
        {
            "ipv4": {
                "interface": "sdwan_group1",
                "metric": 10,
                "source": {
                    "any": True
                },
                "destination": {
                    "any": True
                },
                "service": {
                    "name": "HTTP Management"
                },
                "gateway": {
                    "default": True
                },
                "tos": "0x00",
                "mask": "0x00",
                "distance": {
                    "auto": True
                },
                "path_selection_profile": "sdwan-path1",
                "name": "sdwan-rule2",
                "type": "sdwan",
                "priority": 73,
                "comment": "",
                "disable_on_interface_down": True,
                "tcp_acceleration": False,
                "ticket": {
                    "tag1": "",
                    "tag2": "",
                    "tag3": ""
                }
            }
        },
        {
            "ipv4": {
                "interface": "sdwan-group1",
                "metric": 20,
                "source": {
                    "any": True
                },
                "destination": {
                    "any": True
                },
                "service": {
                    "name": "HTTPS Management"
                },
                "gateway": {
                    "default": True
                },
                "tos": "0x00",
                "mask": "0x00",
                "distance": {
                    "auto": True
                },
                "path_selection_profile": "sdwan-path1",
                "name": "sdwan-rule2",
                "type": "sdwan",
                "priority": 73,
                "comment": "",
                "disable_on_interface_down": True,
                "tcp_acceleration": False,
                "ticket": {
                    "tag1": "",
                    "tag2": "",
                    "tag3": ""
                }
            }
        },
        {
            "ipv4": {
                "interface": "sdwan-group1",
                "metric": 10,
                "source": {
                    "any": True
                },
                "destination": {
                    "any": True
                },
                "service": {
                    "name": "FTP"
                },
                "gateway": {
                    "default": True
                },
                "tos": "0x00",
                "mask": "0x00",
                "distance": {
                    "auto": True
                },
                "path_selection_profile": "sdwan-path1",
                "name": "sdwan-rule2",
                "type": "sdwan",
                "priority": 73,
                "comment": "",
                "disable_on_interface_down": True,
                "tcp_acceleration": False,
                "ticket": {
                    "tag1": "",
                    "tag2": "",
                    "tag3": ""
                }
            }
        }
    ]
}
#sdwan_vpn_rules
sdwan_vpn_rules={
    "route_policies": [
        {
            "ipv4": {
                "interface": "sdwan_group1",
                "metric": 10,
                "source": {
                    "any": True
                },
                "destination": {
                    "any": True
                },
                "service": {
                    "name": "HTTP"
                },
                "gateway": {
                    "default": True
                },
                "tos": "0x00",
                "mask": "0x00",
                "distance": {
                    "auto": True
                },
                "path_selection_profile": "sdwan-path1",
                "name": "sdwan-rule2",
                "type": "sdwan",
                "priority": 73,
                "comment": "",
                "disable_on_interface_down": True,
                "tcp_acceleration": False,
                "ticket": {
                    "tag1": "",
                    "tag2": "",
                    "tag3": ""
                }
            }
        },
        {
            "ipv4": {
                "interface": "sdwan-group1",
                "metric": 20,
                "source": {
                    "any": True
                },
                "destination": {
                    "any": True
                },
                "service": {
                    "name": "HTTPS"
                },
                "gateway": {
                    "default": True
                },
                "tos": "0x00",
                "mask": "0x00",
                "distance": {
                    "auto": True
                },
                "path_selection_profile": "sdwan-path1",
                "name": "sdwan-rule2",
                "type": "sdwan",
                "priority": 73,
                "comment": "",
                "disable_on_interface_down": True,
                "tcp_acceleration": False,
                "ticket": {
                    "tag1": "",
                    "tag2": "",
                    "tag3": ""
                }
            }
        },
        {
            "ipv4": {
                "interface": "sdwan-group1",
                "metric": 10,
                "source": {
                    "any": True
                },
                "destination": {
                    "any": True
                },
                "service": {
                    "any": True
                },
                "gateway": {
                    "default": True
                },
                "tos": "0x00",
                "mask": "0x00",
                "distance": {
                    "auto": True
                },
                "path_selection_profile": "sdwan-path1",
                "name": "sdwan-rule2",
                "type": "sdwan",
                "priority": 73,
                "comment": "",
                "disable_on_interface_down": True,
                "tcp_acceleration": False,
                "ticket": {
                    "tag1": "",
                    "tag2": "",
                    "tag3": ""
                }
            }
        }
    ]
}
#tunnel_vpn
tunnel_vpn={
  "vpn": {
    "policy": [
      {
        "ipv4": {
          "tunnel_interface": {
            "name": "tunnel_vpn1",
            "enable": True,
            "gateway": {
              "primary": "14.110.1.2"
            },
            "auth_method": {
              "shared_secret": {
                "shared_secret": "sonicwall2010",
                "ike_id": {
                  "local": {
                    "ipv4": ""
                  },
                  "peer": {
                    "ipv4": "14.110.1.2"
                  }
                }
              }
            },
            "proposal": {
              "ike": {
                "exchange": "ikev2",
                "encryption": "aes-128",
                "authentication": "sha-1",
                "dh_group": "2",
                "lifetime": 28800
              },
              "ipsec": {
                "protocol": "esp",
                "encryption": {
                  "aes_gcm16_256": True
                },
                "authentication": {},
                "perfect_forward_secrecy": {},
                "lifetime": 28800
              }
            },
            "netbios": False,
            "anti_replay": True,
            "multicast": False,
            "management": {
              "https": False,
              "ssh": False,
              "snmp": False
            },
            "user_login": {
              "http": False,
              "https": False
            },
            "suppress_trigger_packet": False,
            "accept_hash": False,
            "apply_nat": False,
            "send_hash": "",
            "keep_alive": True,
            "bound_to": {
              "interface": "X23:V3401"
            },
            "advanced_routing": False
          }
        }
      }
    ]
  }
}
#tunnel_vpn_interface
tunnel_vpn_interface={
    "tunnel_interfaces": [
        {
            "vpn": {
                "name": "tunnel_1",
                "ip_assignment": {
                    "zone": "VPN",
                    "mode": {
                        "static": {
                            "ip": "150.1.1.1",
                            "netmask": "255.255.255.0"
                        }
                    }
                },
                "policy": "tunnel_vpn1",
                "comment": "",
                "management": {
                    "https": True,
                    "ping": True,
                    "snmp": False,
                    "ssh": False,
                    "fqdn_assignment": ""
                },
                "user_login": {
                    "http": False,
                    "https": False
                },
                "flow_reporting": True,
                "multicast": False,
                "asymmetric_route": False,
                "fragment_packets": True,
                "ignore_df_bit": False
            }
        }
    ]
}
#Test tunnel vpn disable/enable
test_tunnel_vpn={
  "vpn": {
    "policy": [
      {
        "ipv4": {
          "tunnel_interface": {
            "name": "tunnel_vpn2",
            "enable": False,
            "gateway": {
              "primary": "14.110.2.1"
            },
            "auth_method": {
              "shared_secret": {
                "shared_secret": "sonicwall2010",
                "ike_id": {
                  "local": {
                    "ipv4": ""
                  },
                  "peer": {
                    "ipv4": "14.110.2.1"
                  }
                }
              }
            },
            "proposal": {
              "ike": {
                "exchange": "ikev2",
                "encryption": "aes-128",
                "authentication": "sha-1",
                "dh_group": "2",
                "lifetime": 28800
              },
              "ipsec": {
                "protocol": "esp",
                "encryption": {
                  "aes_gcm16_256": True
                },
                "authentication": {},
                "perfect_forward_secrecy": {},
                "lifetime": 28800
              }
            },
            "netbios": False,
            "anti_replay": True,
            "permit_acceleration": False,
            "multicast": False,
            "management": {
              "https": False,
              "ssh": False,
              "snmp": False
            },
            "keep_alive": True,
            "allow_sonicpointn_layer3": False,
            "user_login": {
              "https": False
            },
            "bound_to": {
              "interface": "X28:V3402"
            },
            "suppress_trigger_packet": False,
            "accept_hash": False,
            "send_hash": "",
            "apply_nat": False,
            "advanced_routing": False
          }
        }
      }
    ]
  }
}
