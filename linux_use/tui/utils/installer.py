"""Automatic package installer"""

import subprocess
import asyncio
from typing import List, Optional, Callable
from .system_detector import SystemDetector

class PackageInstaller:
    """Install system and Python packages"""
    
    def __init__(self, progress_callback: Optional[Callable[[str], None]] = None):
        self.progress_callback = progress_callback
        self.system_info = SystemDetector.detect()
    
    def _log(self, message: str):
        """Log progress"""
        if self.progress_callback:
            self.progress_callback(message)
    
    async def install_system_packages(self, packages: List[str]) -> bool:
        """Install system packages"""
        if not self.system_info.package_manager:
            self._log("❌ No package manager detected")
            return False
        
        pm = self.system_info.package_manager
        self._log(f"📦 Using package manager: {pm}")
        
        # Map package names for different distros
        mapped_packages = self._map_package_names(packages, pm)
        
        if pm == 'apt':
            return await self._install_apt(mapped_packages)
        elif pm in ['yum', 'dnf']:
            return await self._install_yum_dnf(mapped_packages, pm)
        elif pm == 'pacman':
            return await self._install_pacman(mapped_packages)
        else:
            self._log(f"❌ Unsupported package manager: {pm}")
            return False
    
    def _map_package_names(self, packages: List[str], pm: str) -> List[str]:
        """Map Debian package names to other distros"""
        if pm == 'apt':
            return packages
        
        # Package name mappings
        mappings = {
            'yum': {
                'python3-xlib': 'python3-xlib',
                'python3-pyatspi': 'python3-pyatspi2',
                'at-spi2-core': 'at-spi2-core',
                'wmctrl': 'wmctrl',
                'xdotool': 'xdotool',
                'python3-gi': 'python3-gobject',
                'python3-tk': 'python3-tkinter',
                'dbus-x11': 'dbus-x11',
            },
            'dnf': {
                'python3-xlib': 'python3-xlib',
                'python3-pyatspi': 'python3-pyatspi2',
                'at-spi2-core': 'at-spi2-core',
                'wmctrl': 'wmctrl',
                'xdotool': 'xdotool',
                'python3-gi': 'python3-gobject',
                'python3-tk': 'python3-tkinter',
                'dbus-x11': 'dbus-x11',
            },
            'pacman': {
                'python3-xlib': 'python-xlib',
                'python3-pyatspi': 'python-atspi',
                'at-spi2-core': 'at-spi2-core',
                'wmctrl': 'wmctrl',
                'xdotool': 'xdotool',
                'python3-gi': 'python-gobject',
                'python3-tk': 'tk',
                'dbus-x11': 'dbus',
            }
        }
        
        mapping = mappings.get(pm, {})
        return [mapping.get(pkg, pkg) for pkg in packages]
    
    async def _install_apt(self, packages: List[str]) -> bool:
        """Install packages using apt"""
        try:
            self._log("📥 Updating package lists...")
            proc = await asyncio.create_subprocess_exec(
                'sudo', 'apt-get', 'update',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc.communicate()
            
            self._log(f"📦 Installing {len(packages)} packages...")
            proc = await asyncio.create_subprocess_exec(
                'sudo', 'apt-get', 'install', '-y', *packages,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode == 0:
                self._log("✅ System packages installed successfully")
                return True
            else:
                self._log(f"❌ Installation failed: {stderr.decode()}")
                return False
                
        except Exception as e:
            self._log(f"❌ Error: {e}")
            return False
    
    async def _install_yum_dnf(self, packages: List[str], pm: str) -> bool:
        """Install packages using yum/dnf"""
        try:
            self._log(f"📦 Installing {len(packages)} packages...")
            proc = await asyncio.create_subprocess_exec(
                'sudo', pm, 'install', '-y', *packages,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode == 0:
                self._log("✅ System packages installed successfully")
                return True
            else:
                self._log(f"❌ Installation failed: {stderr.decode()}")
                return False
                
        except Exception as e:
            self._log(f"❌ Error: {e}")
            return False
    
    async def _install_pacman(self, packages: List[str]) -> bool:
        """Install packages using pacman"""
        try:
            self._log(f"📦 Installing {len(packages)} packages...")
            proc = await asyncio.create_subprocess_exec(
                'sudo', 'pacman', '-S', '--noconfirm', *packages,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode == 0:
                self._log("✅ System packages installed successfully")
                return True
            else:
                self._log(f"❌ Installation failed: {stderr.decode()}")
                return False
                
        except Exception as e:
            self._log(f"❌ Error: {e}")
            return False
    
    async def install_python_packages(self) -> bool:
        """Install Python packages"""
        self._log("🐍 Installing Python dependencies...")
        
        try:
            proc = await asyncio.create_subprocess_exec(
                'pip', 'install', '-e', '/app',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode == 0:
                self._log("✅ Python packages installed successfully")
                return True
            else:
                self._log(f"❌ Python installation failed: {stderr.decode()}")
                return False
                
        except Exception as e:
            self._log(f"❌ Error: {e}")
            return False
    
    async def setup_pyatspi_symlink(self) -> bool:
        """Create symlink for pyatspi in venv"""
        self._log("🔗 Setting up pyatspi symlink...")
        
        try:
            import sys
            import os
            
            site_packages = None
            for path in sys.path:
                if 'site-packages' in path:
                    site_packages = path
                    break
            
            if not site_packages:
                self._log("⚠️  Could not find site-packages directory")
                return False
            
            system_pyatspi = '/usr/lib/python3/dist-packages/pyatspi'
            system_gi = '/usr/lib/python3/dist-packages/gi'
            
            if not os.path.exists(system_pyatspi):
                self._log("⚠️  System pyatspi not found, skipping symlink")
                return True
            
            target_pyatspi = os.path.join(site_packages, 'pyatspi')
            target_gi = os.path.join(site_packages, 'gi')
            
            # Create symlinks
            for target, source in [(target_pyatspi, system_pyatspi), (target_gi, system_gi)]:
                if not os.path.exists(target) and os.path.exists(source):
                    os.symlink(source, target)
                    self._log(f"✅ Created symlink: {target}")
            
            return True
            
        except Exception as e:
            self._log(f"⚠️  Symlink setup: {e}")
            return True  # Non-critical
    
    async def full_installation(self) -> bool:
        """Perform full installation"""
        self._log("🚀 Starting full installation...")
        self._log(f"📍 Detected: {self.system_info.distro_name} {self.system_info.distro_version}")
        self._log(f"🖥️  Desktop: {self.system_info.desktop_environment}")
        self._log(f"🎨 Display: {self.system_info.display_server}")
        
        # Check sudo
        if not self.system_info.has_sudo:
            self._log("⚠️  Warning: No sudo access detected")
            self._log("   You may need to run with sudo or enter password")
        
        # Get missing dependencies
        missing = SystemDetector.get_missing_dependencies()
        system_missing = [dep for dep in missing if not dep.startswith('python:') and not dep.startswith('cli:')]
        
        if system_missing:
            self._log(f"📦 Installing {len(system_missing)} missing system packages...")
            success = await self.install_system_packages(system_missing)
            if not success:
                self._log("⚠️  Some system packages failed to install")
        else:
            self._log("✅ All system packages already installed")
        
        # Install Python packages
        await self.install_python_packages()
        
        # Setup pyatspi
        await self.setup_pyatspi_symlink()
        
        self._log("✅ Installation complete!")
        return True
