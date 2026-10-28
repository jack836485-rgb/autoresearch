import random
import base64
from typing import List, Optional
from .env import VirtualEnvironment


class Task:
    """Base class for tasks."""

    def __init__(self, name: str):
        self.name = name
        self.goal = ""
        self.milestones = []

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        """Setup environment."""
        raise NotImplementedError("Tasks must implement setup()")


class WebServiceAuditTask(Task):
    """Requires: get_active_connections, get_env_variable, check_port_open, fetch_web_content"""

    def __init__(self):
        super().__init__("Web Service Audit")

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        sol = f"{('%032x' % rng.getrandbits(128))[:8]}"
        env.set_solution(sol)

        # Randomize parameters.
        target_ip = f"192.168.1.{rng.randint(20, 250)}"
        target_port = rng.randint(1024, 65535)
        target_hostname = f"db-{rng.randint(1000, 9999)}.internal.net"
        process_name = f"db_engine_{rng.randint(10, 99)}"

        # Step 1: Read connections.
        env.active_connections = [
            {"pid": 1204, "process": process_name, "ip": target_ip, "port": target_port}
        ]

        # Step 2: Map to hostname.
        env.env_vars[process_name] = target_hostname

        # Instrument port knock.
        class InstrumentedVirtualEnvironment(env.__class__):
            def check_port_open(self, host: str, port: int) -> bool:
                # Enforce hostname.
                if host == target_hostname and port == target_port:
                    # Step 3: Port knock. Unlocks passcode.
                    root_url = f"http://{target_hostname}:{target_port}"
                    self.web_content[root_url] = sol
                    return True
                return super().check_port_open(host, port)

            def fetch_web_content(self, url: str) -> Optional[str]:
                normalized_url = url.rstrip("/")
                root_url = f"http://{target_hostname}:{target_port}"

                # Step 4: Check if unlocked.
                if root_url in self.web_content and normalized_url == root_url:
                    return sol

                return super().fetch_web_content(url)

        # Re-assign to subclass.
        env.__class__ = InstrumentedVirtualEnvironment

        self.goal = "Perform a service discovery audit starting from active connection logs to identify the database process name and port. Query the environment variables using the process name to find the internal hostname. Verify the database port is open on this hostname to unlock the service, then fetch the token from the root URL of that specific hostname and port."
        self.milestones = [
            "get_active_connections",
            "get_env_variable",
            "check_port_open",
            "fetch_web_content",
        ]


class EncryptedPayloadRetrievalTask(Task):
    """Requires: list_dir, read_file, decode_base64, decrypt_payload"""

    def __init__(self):
        super().__init__("Encrypted Payload Retrieval")

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        sol = f"{('%032x' % rng.getrandbits(128))[:8]}"
        env.set_solution(sol)

        # Randomize parameters.
        payload_filename = f"payload_{rng.randint(1000, 9999)}.enc"
        secret_key = f"master_key_{rng.randint(100, 999)}"
        ciphertext = f"cipher_blob_{rng.randint(10000, 99999)}"
        b64_ciphertext = base64.b64encode(ciphertext.encode()).decode()

        # Step 1 & 2: Get Base64 content.
        env.add_file(f"/mnt/secure/{payload_filename}", b64_ciphertext)

        # Step 3 & 4: Decrypt solution.
        env.decryption_keys[ciphertext] = {
            "key": secret_key,
            "plaintext": sol,
        }

        self.goal = f"List the directory '/mnt/secure' to find the randomized encrypted payload file. Read this file to obtain its Base64-encoded contents. Decode the Base64 string to retrieve the raw ciphertext blob. Finally, decrypt this ciphertext using the known secret key '{secret_key}' to extract the solution passcode."
        self.milestones = [
            "list_dir",
            "read_file",
            "decode_base64",
            "decrypt_payload",
        ]


class ScheduledBackupAuditTask(Task):
    """Requires: list_cron_jobs, read_file, get_file_metadata, get_env_variable"""

    def __init__(self):
        super().__init__("Scheduled Backup Audit")

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        sol = f"{('%032x' % rng.getrandbits(128))[:8]}"
        env.set_solution(sol)

        # Randomize parameters.
        rand_id = rng.randint(1000, 9999)
        script_path = f"/opt/security/backup_{rand_id}.sh"
        log_path = f"/var/log/backup_{rand_id}.log"
        owner_name = f"backup_admin_{rng.randint(100, 999)}"

        # Step 1: Find script path.
        env.cron_jobs = [
            {"schedule": "0 0 * * *", "command": script_path},
            {"schedule": "*/15 * * * *", "command": "/usr/local/bin/cleanup_temp.py"},
        ]

        # Step 2: Find log path.
        env.add_file(
            script_path,
            f'#!/bin/bash\n# Scheduled backup utility\nLOG_FILE="{log_path}"',
        )

        # Step 3: Find owner.
        env.add_file(
            log_path,
            "Backup completed successfully.",
            metadata={
                "size": 1024,
                "owner": owner_name,
                "mod_time": "2026-06-24 10:00:00",
            },
        )

        # Step 4: Find passcode.
        env.env_vars[owner_name] = sol

        self.goal = "Identify the active cron job script, read its configuration to find the dynamic backup log path, retrieve the file metadata of the log to find its owner, and query the environment variable matching the owner's name to extract the registration passcode."
        self.milestones = [
            "list_cron_jobs",
            "read_file",
            "get_file_metadata",
            "get_env_variable",
        ]


class HostVerificationDiagnosticsTask(Task):
    """Requires: get_network_interfaces, network_ping, dns_resolve, fetch_web_content"""

    def __init__(self):
        super().__init__("Host Verification & Diagnostics")

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        sol = f"{('%032x' % rng.getrandbits(128))[:8]}"
        env.set_solution(sol)

        # Randomize parameters.
        interface_name = f"eth_{rng.randint(100, 999)}"
        local_ip = f"10.0.0.{rng.randint(10, 250)}"
        latency = rng.randint(15, 99)
        remote_ip = f"192.168.1.{rng.randint(10, 250)}"

        # Step 1: Get local IP.
        class InstrumentedVirtualEnvironment(env.__class__):
            def get_network_interfaces(self):
                return {interface_name: {"ip": local_ip, "status": "up"}}

        env.__class__ = InstrumentedVirtualEnvironment

        # Step 2: Get latency.
        env.network_latency[local_ip] = latency

        # Step 3: Get remote IP.
        diagnostic_domain = f"diag-{latency}.local"
        env.dns_records[diagnostic_domain] = remote_ip

        # Step 4: Get passcode.
        env.web_content[f"http://{remote_ip}/status"] = sol

        self.goal = "Retrieve active network interfaces to find the assigned local IP address. Ping this local IP to determine the exact network routing latency. Resolve the dynamic diagnostic hostname 'diag-<latency>.local' (replacing <latency> with the ping result) to find the remote diagnostic server IP. Finally, fetch the web content from 'http://<remote_ip>/status' to retrieve the verification passcode."
        self.milestones = [
            "get_network_interfaces",
            "network_ping",
            "dns_resolve",
            "fetch_web_content",
        ]


class SystemFingerprintingProfileTask(Task):
    """Requires: get_shell_info, get_env_variable, get_file_metadata, get_system_info"""

    def __init__(self):
        super().__init__("System Fingerprinting")

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        sol = f"{('%032x' % rng.getrandbits(128))[:8]}"
        env.set_solution(sol)

        # Randomize parameters.
        term_id = f"xterm-256color-{rng.randint(1000, 9999)}"
        log_path = f"/tmp/sysinfo_{rng.randint(100, 999)}.log"
        owner_name = f"admin_{rng.randint(1000, 9999)}"

        # Step 1: Get term_id.
        env.shell_info = {
            "shell": "/bin/bash",
            "version": "GNU bash, version 5.1.16(1)-release",
            "term": term_id,
            "columns": 80,
            "rows": 24,
        }

        # Step 2: Get log_path.
        env.env_vars[term_id] = log_path

        # Step 3: Get owner_name.
        env.add_file(
            log_path,
            "System profile logged.",
            metadata={
                "size": 512,
                "owner": owner_name,
                "mod_time": "2026-06-24 12:00:00",
            },
        )

        # Step 4: Get passcode.
        env.system_info[owner_name] = sol

        self.goal = "Retrieve the current shell terminal environment details to find the active terminal identifier. Use this identifier to query the environment variables for a dynamically generated system log path. Retrieve the file metadata of this system log to identify its owner. Finally, query the system info database using the owner name as the category to extract the passcode."
        self.milestones = [
            "get_shell_info",
            "get_env_variable",
            "get_file_metadata",
            "get_system_info",
        ]


class ArchiveForensicAuditTask(Task):
    """Requires: list_dir, list_archive_contents, read_file_from_archive, decode_base64"""

    def __init__(self):
        super().__init__("Archive Forensic Audit")

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        sol = f"{('%032x' % rng.getrandbits(128))[:8]}"
        env.set_solution(sol)

        # Randomize parameters.
        archive_name = f"archive_{rng.randint(1000, 9999)}.zip"
        log_name = f"conf_{rng.randint(100, 999)}.log"
        archive_path = f"/backups/{archive_name}"

        # Step 1: Get archive_name.
        env.directories["/backups"] = [archive_name]
        env.add_file(archive_path, "fake ZIP bytes")

        # Step 2 & 3: Get encoded solution.
        encoded_sol = base64.b64encode(sol.encode()).decode()
        env.archives[archive_path] = {log_name: encoded_sol}

        # Step 4: Decode solution.

        self.goal = "List the file system directories inside '/backups' to locate the randomly generated archive package. Enumerate the files bundled within the archive to find the configuration log. Extract and read this log directly from inside the archive to retrieve its Base64-encoded string, then decode this string to find the decrypted solution token."
        self.milestones = [
            "list_dir",
            "list_archive_contents",
            "read_file_from_archive",
            "decode_base64",
        ]


class DriverIntegrityTask(Task):
    """Requires: list_kernel_modules, search_text, get_file_metadata, get_user_groups"""

    def __init__(self):
        super().__init__("Driver Integrity Verification")

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        sol = f"{('%032x' % rng.getrandbits(128))[:8]}"
        env.set_solution(sol)

        # Randomize parameters.
        module_name = f"driver_{rng.randint(1000, 9999)}"
        log_path = f"/var/log/kernel_{rng.randint(100, 999)}.log"
        owner_name = f"sysadmin_{rng.randint(1000, 9999)}"

        # Step 1: Get module_name.
        env.kernel_modules = [
            {"name": "ext4", "size_bytes": 393216, "used_by": ["root"]},
            {"name": module_name, "size_bytes": 98304, "used_by": []},
        ]

        # Step 2: Get log_path.
        # Step 3: Get owner_name.
        env.add_file(
            log_path,
            f"{module_name} verification PASSED.",
            metadata={
                "size": 1024,
                "owner": owner_name,
                "mod_time": "2026-06-24 10:00:00",
            },
        )

        # Step 4: Get solution.
        env.user_groups_db[owner_name] = ["sudo", "adm", sol]

        self.goal = "Enumerate the loaded active kernel driver modules to find the dynamically generated module name. Globally search the filesystem logs for occurrences of this module name to find its verification log. Retrieve the file metadata of this log file to identify the user who owns it. Finally, query the system user groups for this owner to extract the registration passcode."
        self.milestones = [
            "list_kernel_modules",
            "search_text",
            "get_file_metadata",
            "get_user_groups",
        ]


class ProcessSSHKeyInspectionTask(Task):
    """Requires: list_running_processes, get_user_groups, read_file, decode_base64"""

    def __init__(self):
        super().__init__("Process and SSH Key Inspection")

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        sol = f"{('%032x' % rng.getrandbits(128))[:8]}"
        env.set_solution(sol)

        # Randomize parameters.
        owner_name = f"user_{rng.randint(1000, 9999)}"
        key_filename = f"/home/{owner_name}/.ssh/id_rsa_{rng.randint(100, 999)}"

        # Step 1: Get owner_name.
        env.running_processes = [
            {
                "pid": rng.randint(1000, 9999),
                "name": "ssh-daemon",
                "user": owner_name,
            }
        ]

        # Step 2: Get key_filename.
        env.user_groups_db[owner_name] = ["users", "ssh-access", key_filename]

        # Step 3 & 4: Get solution.
        encoded_sol = base64.b64encode(sol.encode()).decode()
        env.add_file(key_filename, encoded_sol)

        self.goal = "Inspect active running processes to find the user running the 'ssh-daemon' process. Query the system user group access records for this dynamically generated process owner to discover an embedded SSH key file path. Read this key file to extract its Base64-encoded string, and decode it to retrieve the final passcode solution."
        self.milestones = [
            "list_running_processes",
            "get_user_groups",
            "read_file",
            "decode_base64",
        ]


class NetworkRouteInterfaceMappingTask(Task):
    """Requires: get_routing_table, search_text, read_file, get_env_variable"""

    def __init__(self):
        super().__init__("Network Route Interface Mapping")

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        sol = f"{('%032x' % rng.getrandbits(128))[:8]}"
        env.set_solution(sol)

        # Randomize parameters.
        gateway_ip = f"192.168.{rng.randint(1, 250)}.{rng.randint(1, 250)}"
        log_path = f"/var/log/network_{rng.randint(1000, 9999)}.log"
        env_var_name = f"ROUTE_CONF_{rng.randint(1000, 9999)}"

        # Step 1: Get gateway_ip.
        env.routing_table = [
            {"destination": "0.0.0.0/0", "gateway": gateway_ip, "interface": "eth0"}
        ]

        # Step 2 & 3: Get env_var_name.
        env.add_file(
            log_path, f"Gateway {gateway_ip} configured. See env var: {env_var_name}"
        )

        # Step 4: Get solution.
        env.env_vars[env_var_name] = sol

        self.goal = "Retrieve the active kernel routing table to discover the dynamic default gateway IP address. Globally search the filesystem for this IP address to find the network configuration log. Read this log file to extract the name of the environment variable storing the gateway credentials. Finally, query this environment variable to extract the registration passcode."
        self.milestones = [
            "get_routing_table",
            "search_text",
            "read_file",
            "get_env_variable",
        ]


class KernelModuleForensicTask(Task):
    """Requires: list_kernel_modules, search_text, read_file, get_file_type"""

    def __init__(self):
        super().__init__("Kernel Module Forensic Discovery")

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        sol = f"{('%032x' % rng.getrandbits(128))[:8]}"
        env.set_solution(sol)

        # Randomize parameters.
        module_name = f"mod_{rng.randint(1000, 9999)}"
        log_path = f"/var/log/kernel_{rng.randint(1000, 9999)}.log"
        error_path = f"/opt/kernel/error_{rng.randint(1000, 9999)}.dump"

        # Step 1: Get module_name.
        env.kernel_modules = [
            {"name": "ext4", "size_bytes": 393216, "used_by": ["root"]},
            {"name": module_name, "size_bytes": 1024, "used_by": []},
        ]

        # Step 2: Get log_path.
        # Step 3: Get error_path.
        env.add_file(
            log_path, f"Kernel panic in {module_name}. Core dump saved to {error_path}"
        )

        # Step 4: Get solution.
        env.add_file(error_path, "binary_dump_data")
        env.file_types[error_path] = sol

        self.goal = "Enumerate the active kernel modules to find a dynamically generated suspicious module. Globally search the filesystem for this module name to find its associated kernel log. Read this log file to discover the file path of the kernel core dump. Finally, query the file type of this core dump file to extract the registration passcode."
        self.milestones = [
            "list_kernel_modules",
            "search_text",
            "read_file",
            "get_file_type",
        ]


class AutomatedJobStorageTask(Task):
    """Requires: list_cron_jobs, read_file, list_dir, get_disk_usage"""

    def __init__(self):
        super().__init__("Automated Job and Storage Auditing")

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        sol = f"{('%032x' % rng.getrandbits(128))[:8]}"
        env.set_solution(sol)

        # Randomize parameters.
        script_path = f"/opt/jobs/job_{rng.randint(1000, 9999)}.sh"
        storage_dir = f"/mnt/storage_{rng.randint(100, 999)}"
        storage_file = f"data_{rng.randint(1000, 9999)}.bin"
        storage_path = f"{storage_dir}/{storage_file}"

        # Step 1: Get script_path.
        env.cron_jobs = [{"schedule": "0 0 * * *", "command": script_path}]

        # Step 2: Get storage_dir.
        env.add_file(
            script_path,
            f'#!/bin/bash\n# Archiving to target directory\nARCHIVE_DIR="{storage_dir}"',
        )

        # Step 3: Get storage_file.
        env.directories[storage_dir] = [storage_file]
        env.add_file(storage_path, "binary data")

        # Step 4: Get solution.
        env.disk_usage[storage_path] = {
            "total": "500GB",
            "used": sol,
            "free": "100GB",
        }

        self.goal = "Query the active automated crontab tasks to find the scheduled backup script. Read this script to extract the dynamically generated storage directory path. List the contents of this storage directory to find the binary data archive. Finally, query the disk usage of this specific archive file; the 'used' space value contains the registration passcode."
        self.milestones = [
            "list_cron_jobs",
            "read_file",
            "list_dir",
            "get_disk_usage",
        ]


class HostnameAccessDiagnosticsTask(Task):
    """Requires: get_etc_hosts, network_ping, get_file_metadata, get_user_groups"""

    def __init__(self):
        super().__init__("Hostname and Access Diagnostics")

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        sol = f"{('%032x' % rng.getrandbits(128))[:8]}"
        env.set_solution(sol)

        # Randomize parameters.
        target_ip = f"10.0.0.{rng.randint(10, 250)}"
        target_hostname = f"internal.db.{rng.randint(1000, 9999)}.local"
        latency = rng.randint(15, 99)
        config_path = f"/etc/config_{latency}.conf"
        owner_name = f"sysadmin_{rng.randint(1000, 9999)}"

        # Step 1: Get target_ip.
        env.etc_hosts = [{"ip": target_ip, "hostnames": [target_hostname]}]

        # Step 2: Get latency.
        env.network_latency[target_ip] = latency

        # Step 3: Get owner_name.
        env.add_file(
            config_path,
            "dummy config data",
            metadata={
                "size": 1024,
                "owner": owner_name,
                "mod_time": "2026-06-24 10:00:00",
            },
        )

        # Step 4: Get solution.
        env.user_groups_db[owner_name] = ["sudo", "adm", sol]

        self.goal = "Query the static hostname definitions to discover the internal database IP address. Execute a network-level ping to this IP to verify its connection latency. Use this latency integer to construct a dynamic configuration file path (/etc/config_<latency>.conf) and retrieve its file metadata to extract the owner's username. Finally, query the system user groups for this owner to extract the registration passcode."
        self.milestones = [
            "get_etc_hosts",
            "network_ping",
            "get_file_metadata",
            "get_user_groups",
        ]


class CPUCapabilitySystemTask(Task):
    """Requires: get_cpu_info, get_system_info, dns_resolve, fetch_web_content"""

    def __init__(self):
        super().__init__("CPU Capability and OS Fingerprinting")

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        sol = f"{('%032x' % rng.getrandbits(128))[:8]}"
        env.set_solution(sol)

        # Randomize parameters.
        cpu_model = f"Intel_Core_{rng.randint(1000, 9999)}"
        domain_name = f"sys-{rng.randint(100, 999)}.local"
        server_ip = f"192.168.1.{rng.randint(10, 250)}"

        # Step 1: Get cpu_model.
        env.cpu_info = {
            "model": cpu_model,
            "cores": 8,
            "architecture": "x86_64",
            "threads_per_core": 2,
            "cache_size_kb": 12288,
        }

        # Step 2: Get domain_name.
        env.system_info[cpu_model] = domain_name

        # Step 3: Get server_ip.
        env.dns_records[domain_name] = server_ip

        # Step 4: Get solution.
        env.web_content[f"http://{server_ip}/auth"] = sol

        self.goal = "Retrieve core physical and hardware properties of the CPU to find its specific model name. Query the high-level operating system distribution using this CPU model as the category to discover a dynamic internal domain name. Resolve this internal domain name to its corresponding IP address. Finally, make an HTTP GET query to the API web endpoint 'http://<ip>/auth' on this server to extract the passcode."
        self.milestones = [
            "get_cpu_info",
            "get_system_info",
            "dns_resolve",
            "fetch_web_content",
        ]


class DNSFirewallVerificationTask(Task):
    """Requires: dns_resolve, get_system_info, check_port_open, fetch_web_content"""

    def __init__(self):
        super().__init__("Network DNS and Socket Mapping")

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        sol = f"{('%032x' % rng.getrandbits(128))[:8]}"
        env.set_solution(sol)

        # Randomize parameters.
        domain_name = f"gateway-{rng.randint(100, 999)}.internal"
        target_ip = f"10.0.{rng.randint(1, 255)}.{rng.randint(1, 255)}"
        target_port = rng.randint(1024, 65535)

        # Step 1: Get target_ip.
        env.dns_records[domain_name] = target_ip

        # Step 2: Get target_port.
        env.system_info[target_ip] = str(target_port)

        # Step 3: Port knock.
        class InstrumentedVirtualEnvironment(env.__class__):
            def check_port_open(self, host: str, port: int) -> bool:
                if host == target_ip and port == target_port:
                    self.web_content[f"http://{target_ip}:{target_port}/passcode"] = sol
                    return True
                return super().check_port_open(host, port)

        env.__class__ = InstrumentedVirtualEnvironment

        self.goal = f"Translate the internal domain hostname '{domain_name}' into an IP address. Query the system information database using this IP address as the category to find the assigned firewall port. Check port reachability on that IP and port to unlock the gateway. Finally, make an HTTP GET request to 'http://<ip>:<port>/passcode' to retrieve the registration passcode."
        self.milestones = [
            "dns_resolve",
            "get_system_info",
            "check_port_open",
            "fetch_web_content",
        ]


class CompressedLogsTask(Task):
    """Requires: list_dir, list_archive_contents, read_file_from_archive, encode_base64"""

    def __init__(self):
        super().__init__("Compressed Logs Diagnostics")

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        sol = f"{('%032x' % rng.getrandbits(128))[:8]}"
        encoded_sol = base64.b64encode(sol.encode()).decode()
        env.set_solution(encoded_sol)

        # Randomize parameters.
        archive_name = f"logs_{rng.randint(1000, 9999)}.tar.gz"
        log_name = f"boot_{rng.randint(100, 999)}.log"
        archive_path = f"/var/backups/{archive_name}"

        # Step 1: Get archive_name.
        env.directories["/var/backups"] = [archive_name]
        env.add_file(archive_path, "tar_data")

        # Step 2 & 3: Get solution.
        env.archives[archive_path] = {log_name: sol}

        self.goal = "List the file system directories inside '/var/backups' to find the dynamic archive file. Enumerate the files bundled inside this archive to find the log file. Extract the log file directly from the archive to get its text content, encode this text content to Base64, and submit the encoded string."
        self.milestones = [
            "list_dir",
            "list_archive_contents",
            "read_file_from_archive",
            "encode_base64",
        ]


class CryptographicHandshakeTask(Task):
    """Requires: encode_base64, fetch_web_content, decode_base64, decrypt_payload"""

    def __init__(self):
        super().__init__("Cryptographic Payload Handshake")

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        sol = f"{('%032x' % rng.getrandbits(128))[:8]}"
        env.set_solution(sol)

        client_id = f"client_{rng.randint(1000, 9999)}"
        server_domain = f"api.secure-{rng.randint(100, 999)}.internal"

        encoded_id = base64.b64encode(client_id.encode()).decode()
        raw_ciphertext = f"cipher_{rng.randint(10000, 99999)}"
        b64_ciphertext = base64.b64encode(raw_ciphertext.encode()).decode()

        env.web_content[f"http://{server_domain}/handshake?id={encoded_id}"] = (
            b64_ciphertext
        )
        env.decryption_keys[raw_ciphertext] = {
            "key": client_id,
            "plaintext": sol,
        }

        self.goal = f"Encode the dynamic client identifier string '{client_id}' into Base64. Query the HTTP API endpoint at 'http://{server_domain}/handshake?id=<ENCODED_ID>' (replace <ENCODED_ID> with the base64 string) to receive a Base64-encoded ciphertext response. Decode this response content from Base64 to get the raw ciphertext blob, and decrypt it using the original client identifier '{client_id}' as the secret key to recover the solution passcode."
        self.milestones = [
            "encode_base64",
            "fetch_web_content",
            "decode_base64",
            "decrypt_payload",
        ]


class UserProcessAccessTask(Task):
    """Requires: list_running_processes, get_user_groups, search_text, read_file"""

    def __init__(self):
        super().__init__("User and Process Access Auditing")

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        sol = f"{('%032x' % rng.getrandbits(128))[:8]}"
        env.set_solution(sol)

        # Randomize parameters.
        owner_name = f"guest_{rng.randint(1000, 9999)}"
        group_name = f"access_{rng.randint(100, 999)}"
        log_path = f"/var/log/audit_{rng.randint(1000, 9999)}.log"

        # Step 1: Get owner_name.
        env.running_processes = [
            {
                "pid": rng.randint(1000, 9999),
                "name": "rogue_miner",
                "user": owner_name,
            }
        ]

        # Step 2: Get group_name.
        env.user_groups_db[owner_name] = ["users", group_name]

        # Step 3: Get log_path.
        # Step 4: Get solution.
        env.add_file(log_path, f"Audit log for {group_name}. Passcode: {sol}")

        self.goal = "Inspect active user-space processes to find the user running the suspicious 'rogue_miner' process. Enumerate the user group access permissions for this dynamically generated user to discover their specific access group. Globally search the filesystem for this access group name to find its associated audit log file. Finally, read this audit log file to retrieve the registration passcode."
        self.milestones = [
            "list_running_processes",
            "get_user_groups",
            "search_text",
            "read_file",
        ]


class FileTypeSecurityAuditTask(Task):
    """Requires: get_env_variable, get_disk_usage, get_file_type, get_file_permissions"""

    def __init__(self):
        super().__init__("File Type and Security Auditing")

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        sol = f"{('%032x' % rng.getrandbits(128))[:8]}"
        env.set_solution(sol)

        # Randomize parameters.
        env_var_name = f"AUDIT_DIR_{rng.randint(1000, 9999)}"
        target_dir = f"/opt/security_{rng.randint(100, 999)}"
        log_name = f"audit_{rng.randint(1000, 9999)}.log"
        target_file = f"{target_dir}/{log_name}"
        mime_type = f"application/x-secure-{rng.randint(100, 999)}"

        # Step 1: Get target_dir.
        env.env_vars[env_var_name] = target_dir

        # Step 2: Get log_name.
        env.disk_usage[target_dir] = {
            "total": "500GB",
            "used": log_name,
            "free": "100GB",
        }

        # Step 3: Get mime_type.
        env.add_file(target_file, "binary content")
        env.file_types[target_file] = mime_type

        # Step 4: Get solution. Mock permissions.
        env.add_file(mime_type, "virtual file")
        env.file_permissions[mime_type] = sol

        self.goal = f"Query the environment variable '{env_var_name}' to discover the target security directory path. Query the disk usage of this directory, where the 'used' field contains the name of the audit log file. Construct the full path to this log file (directory/filename) and query its MIME file type. Finally, use this MIME type string as a virtual file path to query its file permissions, which will return the registration passcode."
        self.milestones = [
            "get_env_variable",
            "get_disk_usage",
            "get_file_type",
            "get_file_permissions",
        ]


class HardwareSpecsShellTask(Task):
    """Requires: get_system_info, get_env_variable, get_user_groups, read_file"""

    def __init__(self):
        super().__init__("Hardware Specs and Shell Diagnostics")

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        sol = f"{('%032x' % rng.getrandbits(128))[:8]}"
        env.set_solution(sol)

        # Randomize parameters.
        cpu_model = f"Intel_Core_{rng.randint(1000, 9999)}"
        sys_user = f"hw_admin_{rng.randint(100, 999)}"
        key_path = f"/home/{sys_user}/.ssh/id_rsa.pub"

        # Step 1: Get cpu_model.
        env.system_info["hardware"] = cpu_model

        # Step 2: Get sys_user.
        env.env_vars[cpu_model] = sys_user

        # Step 3: Get key_path.
        env.user_groups_db[sys_user] = ["admin", "hardware", key_path]

        # Step 4: Get solution.
        env.add_file(key_path, f"ssh-rsa AAAA... {sol}")

        self.goal = "Query the system info database using the category 'hardware' to retrieve the specific CPU model string. Query the environment variables using this CPU model string to discover the assigned system user. Enumerate the user groups for this system user to find the file path to their public SSH key. Finally, read this SSH key file to extract the key verification passcode."
        self.milestones = [
            "get_system_info",
            "get_env_variable",
            "get_user_groups",
            "read_file",
        ]


class DNSFirewallRoutingTask(Task):
    """Requires: dns_resolve, network_ping, check_port_open, get_env_variable"""

    def __init__(self):
        super().__init__("DNS and Firewall Routing")

    def setup(self, env: VirtualEnvironment, rng: random.Random):
        sol = f"{('%032x' % rng.getrandbits(128))[:8]}"
        env.set_solution(sol)

        # Randomize parameters.
        domain_name = f"router-{rng.randint(100, 999)}.local"
        target_ip = f"192.168.{rng.randint(1, 250)}.{rng.randint(1, 250)}"
        latency = rng.randint(10, 99)
        target_port = 8000 + latency
        env_var_name = f"ROUTER_PASS_{rng.randint(1000, 9999)}"

        # Step 1: Get target_ip.
        env.dns_records[domain_name] = target_ip

        # Step 2: Get latency.
        env.network_latency[target_ip] = latency

        # Step 3: Port knock.
        class InstrumentedVirtualEnvironment(env.__class__):
            def check_port_open(self, host: str, port: int) -> bool:
                if host == target_ip and port == target_port:
                    self.env_vars[env_var_name] = sol
                    return True
                return super().check_port_open(host, port)

        env.__class__ = InstrumentedVirtualEnvironment

        self.goal = f"Resolve the gateway domain '{domain_name}' to its IP address. Ping that IP address to check its reachability latency. Use this latency to calculate a target port number (8000 + latency) and probe that port to verify connectivity and unlock the router configuration. Finally, retrieve the environment configuration variable '{env_var_name}' to extract the registration passcode."
        self.milestones = [
            "dns_resolve",
            "network_ping",
            "check_port_open",
            "get_env_variable",
        ]


class TaskPool:
    """Task pool."""

    TASKS = [
        WebServiceAuditTask,
        EncryptedPayloadRetrievalTask,
        ScheduledBackupAuditTask,
        HostVerificationDiagnosticsTask,
        SystemFingerprintingProfileTask,
        ArchiveForensicAuditTask,
        DriverIntegrityTask,
        ProcessSSHKeyInspectionTask,
        NetworkRouteInterfaceMappingTask,
        KernelModuleForensicTask,
        AutomatedJobStorageTask,
        HostnameAccessDiagnosticsTask,
        CPUCapabilitySystemTask,
        DNSFirewallVerificationTask,
        CompressedLogsTask,
        CryptographicHandshakeTask,
        UserProcessAccessTask,
        FileTypeSecurityAuditTask,
        HardwareSpecsShellTask,
        DNSFirewallRoutingTask,
    ]

    @classmethod
    def generate_curriculum(
        cls, n_tasks: int = 10, rng: random.Random = None
    ) -> List[Task]:
        """Sample task curriculum."""
        effective_rng = rng or random
        sampled_indices = effective_rng.sample(
            range(len(cls.TASKS)), min(n_tasks, len(cls.TASKS))
        )
        sampled_indices.sort()
        return [cls.TASKS[i]() for i in sampled_indices]
