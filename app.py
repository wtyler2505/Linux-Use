import psutil

def get_process_details(pid):
    try:
        proc = psutil.Process(pid)
        details = {
            "name": proc.name(),
            "exe": proc.exe(),
            "cmdline": proc.cmdline(),
            "status": proc.status(),
            "ppid": proc.ppid(),
            "username": proc.username(),
            "create_time": proc.create_time(),
            "memory_info": proc.memory_info(),
            "cpu_times": proc.cpu_times(),
        }
        return details
    except psutil.NoSuchProcess:
        return f"No process found with PID {pid}"
    except Exception as e:
        return f"Error: {e}"

# Example usage
pid = 8760  # Replace with the actual PID
print(get_process_details(pid))
