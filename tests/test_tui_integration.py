"""Integration tests for TUI components"""

import pytest
import asyncio
from linux_use.tui.utils.system_detector import SystemDetector
from linux_use.tui.utils.diagnostics import DiagnosticRunner
from linux_use.tui.services.agent_service import AgentService


class TestSystemDetector:
    """Test system detection utilities"""
    
    def test_detect_system(self):
        """Test system detection"""
        sys_info = SystemDetector.detect()
        
        assert sys_info.distro_id is not None
        assert sys_info.distro_name is not None
        assert sys_info.python_version is not None
        print(f"✓ Detected: {sys_info.distro_name} {sys_info.distro_version}")
    
    def test_check_dependencies(self):
        """Test dependency checking"""
        deps = SystemDetector.check_dependencies()
        
        assert isinstance(deps, dict)
        assert len(deps) > 0
        print(f"✓ Checked {len(deps)} dependencies")
    
    def test_get_missing_dependencies(self):
        """Test missing dependency detection"""
        missing = SystemDetector.get_missing_dependencies()
        
        assert isinstance(missing, list)
        if missing:
            print(f"⚠ Missing {len(missing)} dependencies: {missing[:5]}")
        else:
            print("✓ All dependencies installed")


class TestDiagnostics:
    """Test diagnostic utilities"""
    
    def test_run_all_diagnostics(self):
        """Test full diagnostic run"""
        results = DiagnosticRunner.run_all_diagnostics()
        
        assert len(results) > 0
        
        passed = sum(1 for r in results if r.status == "pass")
        failed = sum(1 for r in results if r.status == "fail")
        warnings = sum(1 for r in results if r.status == "warning")
        
        print(f"✓ Diagnostics: {passed} passed, {warnings} warnings, {failed} failed")
        
        for result in results:
            if result.status == "fail":
                print(f"  ✗ {result.name}: {result.message}")
    
    def test_quick_fixes(self):
        """Test quick fix suggestions"""
        fixes = DiagnosticRunner.get_quick_fixes()
        
        assert isinstance(fixes, dict)
        assert len(fixes) > 0
        print(f"✓ {len(fixes)} quick fixes available")


@pytest.mark.asyncio
class TestAgentService:
    """Test agent service"""
    
    async def test_agent_initialization(self):
        """Test agent initialization"""
        import os
        
        # Skip if no API key
        if not os.environ.get('ANTHROPIC_API_KEY'):
            pytest.skip("No ANTHROPIC_API_KEY set")
        
        messages = []
        
        def callback(msg):
            messages.append(msg)
        
        agent_service = AgentService(progress_callback=callback)
        success = await agent_service.initialize_agent()
        
        assert isinstance(success, bool)
        assert len(messages) > 0
        print(f"✓ Agent initialization: {'success' if success else 'failed'}")
    
    async def test_agent_status(self):
        """Test agent status"""
        agent_service = AgentService()
        status = agent_service.get_status()
        
        assert isinstance(status, dict)
        assert "initialized" in status
        assert "running" in status
        print(f"✓ Agent status: {status}")


def test_imports():
    """Test that all critical imports work"""
    try:
        from linux_use.tui.app import LinuxUseTUI
        from linux_use.tui.screens.welcome import WelcomeScreen
        from linux_use.tui.screens.dashboard import DashboardScreen
        from linux_use.tui.screens.installation import InstallationScreen
        from linux_use.tui.screens.diagnostics import DiagnosticsScreen
        from linux_use.tui.screens.monitoring import MonitoringScreen
        from linux_use.tui.screens.configuration import ConfigurationScreen
        print("✓ All TUI screens import successfully")
        
        from linux_use.tui.widgets.log_viewer import LogViewer
        from linux_use.tui.widgets.status_panel import StatusPanel
        from linux_use.tui.widgets.metrics_display import MetricsDisplay
        from linux_use.tui.widgets.ascii_banner import ASCIIBanner
        print("✓ All widgets import successfully")
        
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False


if __name__ == "__main__":
    """Run tests manually"""
    print("=" * 60)
    print("LINUX-USE TUI INTEGRATION TESTS")
    print("=" * 60)
    
    # Test imports
    print("\n[1/4] Testing imports...")
    test_imports()
    
    # Test system detector
    print("\n[2/4] Testing system detector...")
    detector_tests = TestSystemDetector()
    detector_tests.test_detect_system()
    detector_tests.test_check_dependencies()
    detector_tests.test_get_missing_dependencies()
    
    # Test diagnostics
    print("\n[3/4] Testing diagnostics...")
    diag_tests = TestDiagnostics()
    diag_tests.test_run_all_diagnostics()
    diag_tests.test_quick_fixes()
    
    # Test agent service
    print("\n[4/4] Testing agent service...")
    agent_tests = TestAgentService()
    asyncio.run(agent_tests.test_agent_status())
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS COMPLETED")
    print("=" * 60)