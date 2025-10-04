"""Diagnostics and Troubleshooting Screen"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from textual.widgets import Static, Button, DataTable, Label
from textual.worker import work_thread as work
from ..widgets.log_viewer import LogViewer
from ..utils.diagnostics import DiagnosticRunner
import asyncio

class DiagnosticsScreen(Screen):
    """Comprehensive diagnostics and auto-fix system"""
    
    CSS = """
    DiagnosticsScreen {
        background: $surface;
    }
    
    #diag-container {
        width: 100%;
        height: 100%;
        padding: 1;
    }
    
    #diag-header {
        width: 100%;
        height: 3;
        background: $surface-lighten-1;
        border: heavy $accent;
        content-align: center middle;
        margin-bottom: 1;
    }
    
    #diag-results {
        width: 100%;
        height: 1fr;
        border: heavy $accent;
        background: $surface;
    }
    
    #diag-log {
        width: 100%;
        height: 1fr;
        border: heavy $primary;
        margin-top: 1;
    }
    
    #diag-actions {
        width: 100%;
        height: auto;
        margin-top: 1;
        align: center middle;
    }
    
    DataTable {
        height: 100%;
    }
    """
    
    def compose(self) -> ComposeResult:
        """Create child widgets"""
        with Vertical(id="diag-container"):
            yield Static(
                "╔═══════════ SYSTEM DIAGNOSTICS & TROUBLESHOOTING ═══════════╗",
                id="diag-header"
            )
            
            # Results table
            with Container(id="diag-results"):
                table = DataTable()
                table.add_columns("CHECK", "STATUS", "MESSAGE", "FIX")
                yield table
            
            # Log viewer
            yield LogViewer(id="diag-log", max_lines=500)
            
            # Action buttons
            with Horizontal(id="diag-actions"):
                yield Button("▶ RUN DIAGNOSTICS", id="btn-run-diag", variant="primary")
                yield Button("🔧 AUTO-FIX ALL", id="btn-autofix", variant="warning")
                yield Button("◀ BACK", id="btn-back")
    
    def on_mount(self) -> None:
        """Called when screen is mounted"""
        log = self.query_one("#diag-log", LogViewer)
        log.log_system("Diagnostics system initialized")
        log.log_info("Ready to run system checks")
        log.log_warning("Some checks may require sudo privileges")
        
        # Auto-run diagnostics on mount
        self.run_diagnostics()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        \"\"\"Handle button presses\"\"\"
        if event.button.id == \"btn-run-diag\":
            self.run_diagnostics()
        elif event.button.id == \"btn-autofix\":
            self.run_autofix()
        elif event.button.id == \"btn-back\":
            self.app.pop_screen()
    
    @work(exclusive=True)
    async def run_diagnostics(self) -> None:
        \"\"\"Run all diagnostic checks\"\"\"
        log = self.query_one(\"#diag-log\", LogViewer)
        table = self.query_one(DataTable)
        
        log.log_system(\"═\" * 50)
        log.log_system(\"RUNNING DIAGNOSTIC SUITE\")
        log.log_system(\"═\" * 50)
        
        # Clear table
        table.clear()
        
        # Run diagnostics
        results = DiagnosticRunner.run_all_diagnostics()
        
        # Populate table
        for result in results:
            # Status icon
            if result.status == \"pass\":
                status_icon = \"✓\"
                style = \"green bold\"
            elif result.status == \"warning\":
                status_icon = \"⚠\"
                style = \"yellow bold\"
            else:
                status_icon = \"✗\"
                style = \"red bold\"
            
            # Fix suggestion
            fix = result.fix_suggestion if result.fix_suggestion else \"-\"
            
            table.add_row(
                result.name,
                status_icon,
                result.message,
                fix
            )
            
            # Log result
            if result.status == \"pass\":
                log.log_success(f\"{result.name}: {result.message}\")
            elif result.status == \"warning\":
                log.log_warning(f\"{result.name}: {result.message}\")
            else:
                log.log_error(f\"{result.name}: {result.message}\")
            
            if result.details:
                log.log_info(f\"  Details: {result.details}\")
            if result.fix_suggestion:
                log.log_info(f\"  Fix: {result.fix_suggestion}\")
        
        log.log_system(\"═\" * 50)
        log.log_system(\"DIAGNOSTICS COMPLETE\")
        log.log_system(\"═\" * 50)
        
        # Summary
        passed = sum(1 for r in results if r.status == \"pass\")
        warnings = sum(1 for r in results if r.status == \"warning\")
        failed = sum(1 for r in results if r.status == \"fail\")
        
        log.log_success(f\"Passed: {passed}\")
        if warnings:
            log.log_warning(f\"Warnings: {warnings}\")
        if failed:
            log.log_error(f\"Failed: {failed}\")
    
    @work(exclusive=True)
    async def run_autofix(self) -> None:
        \"\"\"Attempt to auto-fix common issues\"\"\"
        log = self.query_one(\"#diag-log\", LogViewer)
        
        log.log_system(\"═\" * 50)
        log.log_system(\"AUTO-FIX INITIATED\")
        log.log_system(\"═\" * 50)
        
        # Get quick fixes
        fixes = DiagnosticRunner.get_quick_fixes()
        
        for issue, fix_cmd in fixes.items():
            log.log_info(f\"Attempting fix for: {issue}\")
            log.log_command(fix_cmd)
            
            # Try to apply fix
            success, message = DiagnosticRunner.run_autofix(issue)
            if success:
                log.log_success(message)
            else:
                log.log_warning(message)
        
        log.log_system(\"═\" * 50)
        log.log_system(\"AUTO-FIX COMPLETE\")
        log.log_system(\"═\" * 50)
        log.log_info(\"Re-running diagnostics...\")
        
        await asyncio.sleep(1)
        await self.run_diagnostics()
