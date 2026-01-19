from mcp.server.fastmcp import FastMCP
import subprocess

mcp = FastMCP("Ubuntu Detector Tools")

@mcp.tool()
def get_disk_usage() -> str:
    """Checks disk usage (df -h)."""
    try:
        return subprocess.check_output(["df", "-h"], text=True)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def read_recent_logs(line_count: int = 50) -> str:
    """Reads last n lines of /var/log/syslog."""
    try:
        return subprocess.check_output(["tail", "-n", str(line_count), "/var/log/syslog"], text=True)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def check_service_status(service_name: str) -> str:
    """Checks systemctl status of a service."""
    try:
        result = subprocess.run(["systemctl", "status", service_name], capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run()
