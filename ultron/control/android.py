"""
Android control module for Ultron Agent Kernel.

Uses ADB (Android Debug Bridge) - free and open-source.
"""

import logging
from typing import Optional, List

from ultron.utils.errors import ControlException
from ultron.utils.logger import setup_logger


class AndroidControl:
    """Android device control via ADB."""
    
    def __init__(self, agent=None, device_id: Optional[str] = None):
        self.agent = agent
        self.device_id = device_id
        self.logger = setup_logger("ultron.control.android")
        self.adb = None
        self._initialize_adb()
    
    def _initialize_adb(self) -> None:
        """Initialize ADB connection."""
        try:
            import subprocess
            # Check if adb is available
            result = subprocess.run(['adb', '--version'], capture_output=True)
            if result.returncode == 0:
                self.logger.info("ADB initialized")
            else:
                self.logger.warning("ADB not found. Install Android SDK tools.")
        except Exception as e:
            self.logger.warning(f"ADB initialization: {str(e)}")
    
    def get_devices(self) -> List[str]:
        """Get list of connected devices.
        
        Returns:
            List of device IDs
        """
        try:
            import subprocess
            result = subprocess.run(
                ['adb', 'devices', '-l'],
                capture_output=True,
                text=True
            )
            devices = []
            for line in result.stdout.split('\n')[1:]:
                if line.strip() and 'device' in line:
                    device_id = line.split()[0]
                    devices.append(device_id)
            self.logger.info(f"Found devices: {devices}")
            return devices
        except Exception as e:
            self.logger.error(f"Failed to get devices: {str(e)}")
            raise ControlException(f"Failed to get devices: {str(e)}")
    
    def execute_command(self, command: str) -> str:
        """Execute ADB command.
        
        Args:
            command: ADB command
            
        Returns:
            Command output
        """
        try:
            import subprocess
            cmd = ['adb']
            if self.device_id:
                cmd.extend(['-s', self.device_id])
            cmd.append(command)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.logger.info(f"Executed: {command}")
            return result.stdout
        except Exception as e:
            self.logger.error(f"Failed to execute command: {str(e)}")
            raise ControlException(f"Command execution failed: {str(e)}")
    
    def tap(self, x: int, y: int) -> None:
        """Tap at coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.execute_command(f"shell input tap {x} {y}")
        self.logger.info(f"Tapped at ({x}, {y})")
    
    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 300) -> None:
        """Swipe from one point to another.
        
        Args:
            x1: Start X
            y1: Start Y
            x2: End X
            y2: End Y
            duration: Duration in milliseconds
        """
        self.execute_command(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")
        self.logger.info(f"Swiped from ({x1}, {y1}) to ({x2}, {y2})")
    
    def type_text(self, text: str) -> None:
        """Type text on device.
        
        Args:
            text: Text to type
        """
        # Escape special characters
        escaped = text.replace(' ', '%s').replace('"', '\\"')
        self.execute_command(f"shell input text '{escaped}'")
        self.logger.info(f"Typed: {text}")
    
    def press_key(self, key: int) -> None:
        """Press a key.
        
        Args:
            key: Key code
        """
        self.execute_command(f"shell input keyevent {key}")
        self.logger.info(f"Pressed key: {key}")
    
    def install_app(self, apk_path: str) -> None:
        """Install APK.
        
        Args:
            apk_path: Path to APK file
        """
        try:
            import subprocess
            cmd = ['adb']
            if self.device_id:
                cmd.extend(['-s', self.device_id])
            cmd.extend(['install', apk_path])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.logger.info(f"Installed APK: {apk_path}")
        except Exception as e:
            self.logger.error(f"Failed to install APK: {str(e)}")
            raise ControlException(f"APK installation failed: {str(e)}")
    
    def uninstall_app(self, package_name: str) -> None:
        """Uninstall app.
        
        Args:
            package_name: Package name
        """
        self.execute_command(f"uninstall {package_name}")
        self.logger.info(f"Uninstalled: {package_name}")
    
    def take_screenshot(self, filename: str = "screenshot.png") -> None:
        """Take device screenshot.
        
        Args:
            filename: Output filename
        """
        try:
            import subprocess
            cmd = ['adb']
            if self.device_id:
                cmd.extend(['-s', self.device_id])
            cmd.extend(['shell', 'screencap', '-p', '/sdcard/screenshot.png'])
            
            subprocess.run(cmd, check=True)
            
            # Pull screenshot
            pull_cmd = ['adb']
            if self.device_id:
                pull_cmd.extend(['-s', self.device_id])
            pull_cmd.extend(['pull', '/sdcard/screenshot.png', filename])
            
            subprocess.run(pull_cmd, check=True)
            self.logger.info(f"Screenshot saved: {filename}")
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            raise ControlException(f"Screenshot failed: {str(e)}")
