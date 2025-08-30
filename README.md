📑 Documentación del Proyecto


🔹 Subredes (VLSM)

VLAN / Red	ID de VLAN	Dirección de red	Máscara	Rango de hosts válidos	Broadcast

Gestión	1099	10.10.10.0	/29 (255.255.255.248)	10.10.10.1 – 10.10.10.6	10.10.10.7

Ventas	210	10.10.10.32	/27 (255.255.255.224)	10.10.10.33 – 10.10.10.62	10.10.10.63

Técnica	211	10.10.10.64	/28 (255.255.255.240)	10.10.10.65 – 10.10.10.78	10.10.10.79

Visitantes	212	10.10.10.80	/28 (255.255.255.240)	10.10.10.81 – 10.10.10.94	10.10.10.95



🔹 Objetivo del Script

El script red_config.py automatiza la configuración de la red mediante Netmiko, conectándose por SSH a los dispositivos de red (SW1, SW2, R1 y R2).

El script realiza:

En SW1 y SW2:
- Creación de VLANs (Ventas, Técnica, Visitantes).
- Asignación de puertos de acceso.
- Configuración de troncales entre switches y routers.
 
En R1 (Router Principal):
- Creación de subinterfaces con dot1Q.
- Configuración de DHCP para VLANs funcionales.
- Configuración de NAT solo para Ventas y Técnica.

En R2 (Router Secundario):
- Configuración de interfaz de gestión y trunk hacia SW2.

En todos los equipos:
- Comandos de verificación (show vlan brief, show ip route, show ip interface brief).



🔹 Cómo ejecutar el script

Clonar el repositorio:
git clone <URL-del-repo>
cd <nombre-repo>


Instalar dependencias en Debian:

sudo apt update 
sudo apt install python3 python3-pip -y
pip3 install netmiko


Ejecutar el script:

python3 red_config.py


Verificar la salida en consola:
- VLANs creadas en los switches.
- Subinterfaces y rutas en el router.
- Interfaces activas en R2.



🔹Pruebas

show vlan brief en SW1 → muestra VLANs 210, 211, 212, 219 y 1099.
show ip route en R1 → aparecen las subredes 10.10.10.32/27, 10.10.10.64/28 y 10.10.10.80/28.
show ip interface brief en R2 → confirma IP de gestión.
Test de DHCP en PCs de Ventas, Técnica y Visitantes.

Test de conectividad:
PC de Ventas y Técnica → Internet OK (ping 8.8.8.8).
PC de Visitantes → sin salida a Internet.
Debian (Gestión) → acceso SSH a todos los dispositivos.



📸 Imagenes del linux Debian cuando se ejecuto el scrpit

🔹 Captura 1

![Captura 1](https://github.com/user-attachments/assets/1c09720c-fded-4f30-a011-4a2aae574a4c)

🔹 Captura 2 

![Captura 2](https://github.com/user-attachments/assets/634c02d7-d320-48bd-a10f-ceeb76ac8723)

🔹 Captura 3

![Captura 3](https://github.com/user-attachments/assets/0ce35c04-acd3-4329-b996-5739ab8e5303)


