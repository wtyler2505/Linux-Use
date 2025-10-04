"""Diagnostic and troubleshooting utilities"""

import os
import shutil
import subprocess
import psutil
from typing import Dict, List, Tuple
from dataclasses import dataclass
from .system_detector import SystemDetector

@dataclass
class DiagnosticResult:
    """Result of a diagnostic check"""
    name: str
    status: str  # 'pass', 'fail', 'warning'
    message: str
    details: str = ""
    fix_suggestion: str = ""

class DiagnosticRunner:
    """Run diagnostics and troubleshooting"""
    
    @staticmethod
    def run_all_diagnostics() -> List[DiagnosticResult]:
        """Run all diagnostic checks"""
        results = []
        
        # System checks
        results.append(DiagnosticRunner._check_display())
        results.append(DiagnosticRunner._check_dbus())
        results.append(DiagnosticRunner._check_atspi())
        results.append(DiagnosticRunner._check_xserver())
        results.append(DiagnosticRunner._check_dependencies())
        results.append(DiagnosticRunner._check_python_env())
        results.append(DiagnosticRunner._check_permissions())
        results.append(DiagnosticRunner._check_system_resources())
        
        return results
    
    @staticmethod
    def _check_display() -> DiagnosticResult:
        """Check DISPLAY environment variable"""
        display = os.environ.get('DISPLAY')
        if display:
            return DiagnosticResult(
                name="Display Server",
                status="pass",
                message=f"✓ DISPLAY set to {display}",
                details="X11 display is properly configured"
            )
        else:
            return DiagnosticResult(
                name="Display Server",
                status="fail",
                message="✗ DISPLAY not set",
                details="No display server detected",
                fix_suggestion="Run: export DISPLAY=:0"
            )
    
    @staticmethod
    def _check_dbus() -> DiagnosticResult:
        """Check D-Bus session"""
        dbus_addr = os.environ.get('DBUS_SESSION_BUS_ADDRESS')
        if dbus_addr:
            return DiagnosticResult(
                name="D-Bus Session",
                status="pass",
                message="✓ D-Bus session active",
                details=f"Address: {dbus_addr[:50]}..."
            )
        else:
            return DiagnosticResult(
                name="D-Bus Session",
                status="warning",
                message="⚠ D-Bus session not detected",
                details="AT-SPI2 may not work properly",
                fix_suggestion="Run: eval $(dbus-launch --sh-syntax)"
            )
    
    @staticmethod
    def _check_atspi() -> DiagnosticResult:
        """Check AT-SPI2 availability"""
        try:
            import pyatspi
            return DiagnosticResult(
                name="AT-SPI2",
                status="pass",
                message="✓ AT-SPI2 available",
                details="UI tree navigation enabled"
            )
        except ImportError:
            return DiagnosticResult(
                name="AT-SPI2",
                status="fail",
                message="✗ pyatspi not found",
                details="Cannot detect UI elements",
                fix_suggestion="Install: sudo apt install python3-pyatspi"
            )
    
    @staticmethod
    def _check_xserver() -> DiagnosticResult:
        """Check if X server is responding"""
        if not os.environ.get('DISPLAY'):
            return DiagnosticResult(
                name="X Server",
                status="fail",
                message="✗ No display",
                details="X server not accessible"
            )
        
        if shutil.which('xdpyinfo'):
            try:
                result = subprocess.run(
                    ['xdpyinfo'],
                    capture_output=True,
                    timeout=2
                )
                if result.returncode == 0:
                    return DiagnosticResult(
                        name="X Server",
                        status="pass",
                        message="✓ X server responding",
                        details="Display server is healthy"
                    )
            except Exception:
                pass
        
        return DiagnosticResult(
            name="X Server",
            status="warning",
            message="⚠ Cannot verify X server",
            details="xdpyinfo not available"
        )
    
    @staticmethod
    def _check_dependencies() -> DiagnosticResult:
        """Check all dependencies"""
        missing = SystemDetector.get_missing_dependencies()
        
        if not missing:
            return DiagnosticResult(
                name="Dependencies",
                status="pass",
                message="✓ All dependencies installed",
                details=f"Checked {len(SystemDetector.check_dependencies())} items"
            )
        elif len(missing) < 5:
            return DiagnosticResult(
                name="Dependencies",
                status="warning",
                message=f"⚠ {len(missing)} dependencies missing",
                details="\n".join(missing[:5]),
                fix_suggestion="Use Installation Wizard to fix"
            )
        else:
            return DiagnosticResult(
                name="Dependencies",
                status="fail",
                message=f"✗ {len(missing)} dependencies missing",
                details="\n".join(missing[:5]),
                fix_suggestion="Run full installation"
            )
    
    @staticmethod
    def _check_python_env() -> DiagnosticResult:
        """Check Python environment"""
        import sys
        version = f"{sys.version_info.major}.{sys.version_info.minor}"
        
        if sys.version_info.major >= 3 and sys.version_info.minor >= 11:
            return DiagnosticResult(
                name="Python Environment",
                status="pass",
                message=f"✓ Python {version}",
                details=f"Interpreter: {sys.executable}"
            )
        else:
            return DiagnosticResult(
                name="Python Environment",
                status="warning",
                message=f"⚠ Python {version}",
                details="Python 3.11+ recommended",
                fix_suggestion="Upgrade Python version"
            )
    
    @staticmethod
    def _check_permissions() -> DiagnosticResult:
        """Check file permissions"""
        app_dir = "/app"
        if os.access(app_dir, os.R_OK | os.W_OK):
            return DiagnosticResult(
                name="Permissions",
                status="pass",
                message="✓ File permissions OK",
                details=f"Can read/write {app_dir}"
            )
        else:
            return DiagnosticResult(
                name="Permissions",
                status="fail",
                message="✗ Permission denied",
                details=f"Cannot access {app_dir}",
                fix_suggestion="Check file ownership"
            )
    
    @staticmethod
    def _check_system_resources() -> DiagnosticResult:
        """Check system resources"""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        issues = []
        if cpu_percent > 90:
            issues.append(f"High CPU: {cpu_percent}%")
        if mem.percent > 90:
            issues.append(f"High Memory: {mem.percent}%")
        if disk.percent > 90:
            issues.append(f"High Disk: {disk.percent}%")
        
        if issues:
            return DiagnosticResult(
                name="System Resources",
                status="warning",
                message="⚠ Resource pressure detected",
                details="\n".join(issues),
                fix_suggestion="Close unnecessary applications"
            )
        else:
            return DiagnosticResult(
                name="System Resources",
                status="pass",
                message="✓ Resources healthy",
                details=f"CPU: {cpu_percent}%, RAM: {mem.percent}%, Disk: {disk.percent}%"
            )
    
    @staticmethod
    def get_quick_fixes() -> Dict[str, str]:
        """Get common quick fixes"""
        return {
            "No DISPLAY": "export DISPLAY=:0",
            "No D-Bus": "eval $(dbus-launch --sh-syntax)",
            "pyatspi missing": "sudo apt install python3-pyatspi gir1.2-atspi-2.0",
            "AT-SPI daemon": "/usr/libexec/at-spi-bus-launcher &",
            "Xvfb virtual display": "Xvfb :99 -screen 0 1920x1080x24 &",
            "wmctrl not found": "sudo apt install wmctrl xdotool",
        }
    
    @staticmethod
    def run_autofix(issue: str) -> Tuple[bool, str]:
        """Attempt automatic fix for common issues"""
        fixes = {
            "No DISPLAY": lambda: os.environ.update({'DISPLAY': ':0'}),
            "Xvfb": lambda: subprocess.run(['Xvfb', ':99', '-screen', '0', '1920x1080x24'], 
                                           stdout=subprocess.DEVNULL, 
                                           stderr=subprocess.DEVNULL),
        }
        
        if issue in fixes:
            try:
                fixes[issue]()
                return True, f"Applied fix for: {issue}"
            except Exception as e:
                return False, f"Fix failed: {e}"
        
        return False, "No automatic fix available"
