from netmiko import ConnectHandler

# ========= Definición de dispositivos =========
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

# ========= Configuración de Switches =========
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

# ========= Configuración de Router1 (MikroTik) =========
# Subinterfaces VLAN, direcciones, NAT y DHCP
r1_config = [
    # Crear VLANs sobre ether2 (troncal con SW1)
    "/interface vlan add interface=ether2 name=vlan210 vlan-id=210",
    "/interface vlan add interface=ether2 name=vlan211 vlan-id=211",
    "/interface vlan add interface=ether2 name=vlan212 vlan-id=212",
    # Direccionamiento
    "/ip address add address=10.10.10.33/27 interface=vlan210",
    "/ip address add address=10.10.10.65/28 interface=vlan211",
    "/ip address add address=10.10.10.81/28 interface=vlan212",
    # DHCP para Ventas
    "/ip pool add name=ventas_pool ranges=10.10.10.34-10.10.10.62",
    "/ip dhcp-server add name=ventas_dhcp interface=vlan210 address-pool=ventas_pool disabled=no",
    "/ip dhcp-server network add address=10.10.10.32/27 gateway=10.10.10.33 dns-server=8.8.8.8",
    # DHCP para Técnica
    "/ip pool add name=tecnica_pool ranges=10.10.10.66-10.10.10.78",
    "/ip dhcp-server add name=tecnica_dhcp interface=vlan211 address-pool=tecnica_pool disabled=no",
    "/ip dhcp-server network add address=10.10.10.64/28 gateway=10.10.10.65 dns-server=8.8.8.8",
    # NAT para Ventas y Técnica (salida a Internet por ether1)
    "/ip firewall nat add chain=srcnat src-address=10.10.10.32/27 out-interface=ether1 action=masquerade",
    "/ip firewall nat add chain=srcnat src-address=10.10.10.64/28 out-interface=ether1 action=masquerade",
]

# ========= Configuración de Router2 (MikroTik remoto) =========
# Acá solo confirmamos trunk hacia SW2
r2_config = [
    "/interface bridge add name=br-trunk vlan-filtering=yes",
    "/interface bridge port add bridge=br-trunk interface=ether1 pvid=219",
    "/interface bridge port add bridge=br-trunk interface=ether2 pvid=219",
    "/interface bridge vlan add bridge=br-trunk vlan-ids=1099 tagged=br-trunk,ether1,ether2",
    "/interface bridge vlan add bridge=br-trunk vlan-ids=219 untagged=ether1,ether2",
]

# ========= Ejecución =========
for name, device in devices.items():
    print(f"\n===== Conectando a {name.upper()} ({device['host']}) =====")
    net_connect = ConnectHandler(**device)

    if name == "sw1":
        output = net_connect.send_config_set(sw1_config)
        print(net_connect.send_command("show vlan brief"))
    elif name == "sw2":
        output = net_connect.send_config_set(sw2_config)
        print(net_connect.send_command("show vlan brief"))
    elif name == "r1":
        for cmd in r1_config:
            net_connect.send_command(cmd)
        print(net_connect.send_command("/ip address print"))
        print(net_connect.send_command("/ip firewall nat print"))
    elif name == "r2":
        for cmd in r2_config:
            net_connect.send_command(cmd)
        print(net_connect.send_command("/interface bridge vlan print"))

    net_connect.disconnect()
