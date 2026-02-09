import os

import paramiko
from notion_client import Client

# --- CONFIG ---
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_DHCP_DATASOURCE = os.environ.get("NOTION_DHCP_DATASOURCE")
ROUTER_IP = os.environ.get("ROUTER_IP")
ROUTER_USER = os.environ.get("ROUTER_USER")
ROUTER_PASS = os.environ.get("ROUTER_PASS")

# --- Notion ---
notion = Client(auth=NOTION_TOKEN)


def get_property_from_device(device, property_name) -> str | None:
    properties = device.get("properties", {})
    property = properties.get(property_name, {})
    if property.get("type") == "rich_text":
        rich_text = property.get("rich_text", [])
        if rich_text:
            return rich_text[0].get("plain_text", "")
    return None


def get_devices():
    data_source = notion.data_sources.query(data_source_id=NOTION_DHCP_DATASOURCE)

    devices = data_source.get("results", [])

    dhcp_list = []
    for device in devices:
        mac = get_property_from_device(device, 'Dirección MAC')
        ip = get_property_from_device(device, 'IP asignada')
        name = get_property_from_device(device, 'Nombre Lógico')

        if not mac or not ip or not name:
            continue
        dhcp_list.append({
            "mac": mac,
            "ip": ip,
            "name": name
        })

    def ip_to_tuple(ip_str):
        """Convierte una IP string a tupla de números para comparación correcta."""
        return tuple(map(int, ip_str.split('.')))

    dhcp_list.sort(key=lambda x: ip_to_tuple(x['ip']))
    return dhcp_list


def format_device(device) -> str:
    """
    Format a device dictionary into a string.

    :param device:
    :return: <00:00:00:00:00:00>192.168.50.33>>my-host
    """
    return f"<{device['mac']}>{device['ip']}>>{device['name']}"


def execute_command_on_router(device_str):
    """
    Ejecuta un comando en el router por SSH con confirmación previa.

    :param device_str: Comando a ejecutar en el router
    """

    command = f'nvram set dhcp_staticlist="{device_str}"; nvram commit; service restart_dnsmasq;'
    print("This is the command to execute on the router:")
    print(command)

    # Pedir confirmación
    confirmation = input("\n¿Deseas ejecutar este comando? (s/n): ").strip().lower()
    if confirmation != 's':
        print("Operación cancelada.")
        return 1

    try:
        # Conectar al router
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ROUTER_IP, username=ROUTER_USER, password=ROUTER_PASS)

        # Ejecutar comando
        stdin, stdout, stderr = ssh.exec_command(command)

        exit_code = stdout.channel.recv_exit_status()

        output = stdout.read().decode()
        error = stderr.read().decode()

        if output:
            print(output)

        if error:
            print("ERROR:", error)

        return exit_code
    except Exception as e:
        print(f"Error al conectar o ejecutar comando: {e}")
        return 1


# --- Main ---
def main():
    devices = get_devices()

    devices_str = ""
    for device in devices:
        print("Processing device:", device)
        devices_str += format_device(device)

    return execute_command_on_router(devices_str)


if __name__ == "__main__":
    main()
