from typing import Dict, List, Any, Optional


class VirtualEnvironment:
    """
    A fully isolated, in-memory simulated environment for the Discovery Benchmark.
    """

    def __init__(
        self,
        failure_probability: float = 0.0,
        set_window: Optional[int] = None,
        trigger_command: Optional[str] = None,
    ):
        self.failure_probability = failure_probability
        self.set_window = set_window
        self.trigger_command = trigger_command
        self._init_state()

    def _init_state(self):
        self.window_ticks_left = 0
        self.window_active = False

        self.files: Dict[str, str] = {}  # path -> text content
        self.directories: Dict[str, List[str]] = {
            "/": []
        }  # path -> list of child item names

        self.file_metadata: Dict[str, Dict[str, Any]] = {}
        self.file_permissions: Dict[str, str] = {}
        self.file_types: Dict[str, str] = {}

        self.env_vars: Dict[str, str] = {}
        self.system_info: Dict[str, str] = {
            "os": "Linux 5.15.0-generic",
            "hardware": "x86_64",
            "env": "production",
        }

        self.routing_table: List[Dict[str, Any]] = []
        self.user_groups_db: Dict[str, List[str]] = {}
        self.cron_jobs: List[Dict[str, Any]] = []
        self.etc_hosts: List[Dict[str, Any]] = []
        self.cpu_info: Dict[str, Any] = {}
        self.kernel_logs: List[str] = []
        self.ssh_keys_metadata: List[Dict[str, Any]] = []
        self.kernel_modules: List[Dict[str, Any]] = []
        self.shell_info: Dict[str, Any] = {}
        self.network_interfaces: List[str] = []

        self.network_latency: Dict[str, int] = {}
        self.dns_records: Dict[str, str] = {}
        self.open_ports: Dict[str, List[int]] = {}
        self.active_connections: List[Dict[str, Any]] = []

        self.running_processes: List[Dict[str, Any]] = []
        self.current_user: str = "sysadmin"
        self.uptime: str = "14 days, 3:12"
        self.memory_usage: Dict[str, str] = {
            "total": "32GB",
            "used": "12GB",
            "free": "20GB",
        }
        self.disk_usage: Dict[str, Dict[str, str]] = {
            "/": {"total": "500GB", "used": "100GB", "free": "400GB"}
        }

        self.web_content: Dict[str, str] = {}
        self.archives: Dict[str, Dict[str, str]] = {}
        self.decryption_keys: Dict[str, Dict[str, str]] = (
            {}
        )  # encrypted_text -> {"key": key, "plaintext": plaintext}

        self.current_solution: Optional[str] = None

    def set_solution(self, solution: str):
        self.current_solution = solution

    def check_solution(self, solution: str) -> bool:
        return bool(
            self.current_solution
            and str(solution).strip() == str(self.current_solution).strip()
        )

    def add_file(
        self,
        path: str,
        content: str,
        metadata: dict = None,
        permissions: str = "-rw-r--r--",
        ftype: str = "text/plain",
    ):
        """Helper for Tasks to inject files into the environment."""
        self.files[path] = content
        self.file_permissions[path] = permissions
        self.file_types[path] = ftype
        self.file_metadata[path] = metadata or {
            "size": len(content),
            "owner": self.current_user,
            "mod_time": "2026-06-24 10:00:00",
        }

        # Update directory tree recursively
        parts = path.strip("/").split("/")
        current_dir = "/"
        for part in parts[:-1]:
            if current_dir not in self.directories:
                self.directories[current_dir] = []
            if part not in self.directories[current_dir]:
                self.directories[current_dir].append(part)
            current_dir = (
                current_dir + part if current_dir == "/" else current_dir + "/" + part
            )

        if current_dir not in self.directories:
            self.directories[current_dir] = []
        file_name = parts[-1]
        if file_name not in self.directories[current_dir]:
            self.directories[current_dir].append(file_name)

    # --- API IMPLEMENTATIONS ---

    def list_dir(self, path: str) -> Optional[List[str]]:
        return self.directories.get(path)

    def read_file(self, file_path: str) -> Optional[str]:
        content = self.files.get(file_path)
        if content and len(content.split("\n")) > 1000:
            return "Error: File too large to read entirely. Use regex_search."
        return content

    def search_text(self, query: str) -> List[str]:
        matches = []
        for path, content in self.files.items():
            if query in content:
                matches.append(path)
        return matches

    def get_system_info(self, category: str) -> Optional[str]:
        return self.system_info.get(category)

    def network_ping(self, host: str) -> Optional[int]:
        return self.network_latency.get(host)

    def get_env_variable(self, name: str) -> Optional[str]:
        return self.env_vars.get(name)

    def get_file_metadata(self, file_path: str) -> Optional[Dict[str, Any]]:
        return self.file_metadata.get(file_path)

    def get_file_type(self, file_path: str) -> Optional[str]:
        return self.file_types.get(file_path)

    def get_disk_usage(self, path: str) -> Optional[Dict[str, str]]:
        return self.disk_usage.get(path)

    def fetch_web_content(self, url: str) -> Optional[str]:
        return self.web_content.get(url)

    def dns_resolve(self, domain: str) -> Optional[str]:
        return self.dns_records.get(domain)

    def check_port_open(self, host: str, port: int) -> bool:
        return port in self.open_ports.get(host, [])

    def get_active_connections(self) -> List[Dict[str, Any]]:
        return self.active_connections

    def decrypt_payload(self, encrypted_text: str, secret_key: str) -> Optional[str]:
        mapping = self.decryption_keys.get(encrypted_text)
        if mapping and mapping.get("key") == secret_key:
            return mapping.get("plaintext")
        return None

    def get_current_user(self) -> str:
        return self.current_user

    def list_running_processes(self) -> List[Dict[str, Any]]:
        return self.running_processes

    def get_system_uptime(self) -> str:
        return self.uptime

    def get_memory_usage(self) -> Dict[str, str]:
        return self.memory_usage

    def get_file_permissions(self, file_path: str) -> Optional[str]:
        return self.file_permissions.get(file_path)

    def get_network_interfaces(self) -> Dict[str, Any]:
        if hasattr(self, "network_interfaces"):
            return {
                iface: {"ip": "192.168.x.x", "status": "up"}
                for iface in self.network_interfaces
            }
        return {
            "eth0": {"ip": "192.168.1.10", "status": "up"},
            "lo": {"ip": "127.0.0.1", "status": "up"},
        }

    def list_archive_contents(self, archive_path: str) -> Optional[List[str]]:
        if archive_path in self.archives:
            return list(self.archives[archive_path].keys())
        return None

    def read_file_from_archive(
        self, archive_path: str, file_name: str
    ) -> Optional[str]:
        if archive_path in self.archives:
            return self.archives[archive_path].get(file_name)
        return None
