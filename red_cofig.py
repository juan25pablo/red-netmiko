devices = {
    "sw1": {
        "device_type": "cisco_ios",
        "host": "10.10.10.2",
        "username": "admin",
        "password": "admin",
    },
    "sw2": {
        "device_type": "cisco_ios",
        "host": "10.10.10.3",
        "username": "admin",
        "password": "admin",
    },
    "r1": {
        "device_type": "mikrotik_routeros",
        "host": "10.10.10.1",
        "username": "admin",
        "password": "juan",
    },
    "r2": {
        "device_type": "mikrotik_routeros",
        "host": "10.10.10.4",
        "username": "admin",
        "password": "juan",
    },
}


sw1_config = [
    "vlan 210",
    " name Ventas",
    "vlan 211",
    " name Tecnica",
    "vlan 212",
    " name Visitantes",
    "interface e0/1",
    " switchport mode access",
    " switchport access vlan 210",
    "interface e0/2",
    " switchport mode access",
    " switchport access vlan 211",
    "interface e0/3",
    " switchport mode access",
    " switchport access vlan 212",
    "interface e0/0",
    " switchport trunk encapsulation dot1q",
    " switchport mode trunk",
    " switchport trunk native vlan 219",
    " switchport trunk allowed vlan 210,211,212,1099,219",
]

sw2_config = [
    "vlan 210",
    " name Ventas",
    "vlan 211",
    " name Tecnica",
    "vlan 212",
    " name Visitantes",
    "interface e0/0",
    " switchport trunk encapsulation dot1q",
    " switchport mode trunk",
    " switchport trunk native vlan 219",
    " switchport trunk allowed vlan 210,211,212,1099,219",
]

r1_config = [
    "interface g0/0.210",
    " encapsulation dot1Q 210",
    " ip address 10.10.10.33 255.255.255.224",
    "interface g0/0.211",
    " encapsulation dot1Q 211",
    " ip address 10.10.10.65 255.255.255.240",
    "interface g0/0.212",
    " encapsulation dot1Q 212",
    " ip address 10.10.10.81 255.255.255.240",
    "ip dhcp pool VENTAS",
    " network 10.10.10.32 255.255.255.224",
    " default-router 10.10.10.33",
    "ip dhcp pool TECNICA",
    " network 10.10.10.64 255.255.255.240",
    " default-router 10.10.10.65",
    "ip nat inside source list 1 interface g0/1 overload",
    "access-list 1 permit 10.10.10.32 0.0.0.31",
    "access-list 1 permit 10.10.10.64 0.0.0.15",
]


r2_config = [
    "interface g0/0",
    " no shutdown",
    "description Trunk hacia SW2",
]

from netmiko import ConnectHandler

for name, device in devices.items():
    print(f"Conectando a {name}...")
    net_connect = ConnectHandler(**device)

    if name == "sw1":
        net_connect.send_config_set(sw1_config)
        output = net_connect.send_command("show vlan brief")
    elif name == "sw2":
        net_connect.send_config_set(sw2_config)
        output = net_connect.send_command("show vlan brief")
    elif name == "r1":
        net_connect.send_config_set(r1_config)
        output = net_connect.send_command("show ip route")
    elif name == "r2":
        net_connect.send_config_set(r2_config)
        output = net_connect.send_command("show ip interface brief")

    print(output)
    net_connect.disconnect()
