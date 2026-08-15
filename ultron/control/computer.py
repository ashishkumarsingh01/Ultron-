"""
Computer control module for Ultron Agent Kernel.

Uses free, open-source tools for automation.
"""

import logging
from typing import Optional, Tuple

from ultron.utils.errors import ControlException
from ultron.utils.logger import setup_logger


class ComputerControl:
    """Computer automation and control."""
    
    def __init__(self, agent=None):
        self.agent = agent
        self.logger = setup_logger("ultron.control.computer")
        self._initialize_control()
    
    def _initialize_control(self) -> None:
        """Initialize computer control components."""
        try:
            import pyautogui
            self.pyautogui = pyautogui
            # Disable fail-safe for testing
            self.pyautogui.FAILSAFE = False
            self.logger.info("Computer control initialized")
        except ImportError:
            self.logger.warning("pyautogui not installed")
            self.pyautogui = None
    
    def move_mouse(self, x: int, y: int) -> None:
        """Move mouse to coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        try:
            if self.pyautogui is None:
                raise ControlException("pyautogui not available")
            self.pyautogui.moveTo(x, y)
            self.logger.info(f"Moved mouse to ({x}, {y})")
        except Exception as e:
            self.logger.error(f"Failed to move mouse: {str(e)}")
            raise ControlException(f"Mouse movement failed: {str(e)}")
    
    def click(self, x: int, y: int, button: str = 'left') -> None:
        """Click at coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            button: Mouse button (left, right, middle)
        """
        try:
            if self.pyautogui is None:
                raise ControlException("pyautogui not available")
            self.pyautogui.click(x, y, button=button)
            self.logger.info(f"Clicked at ({x}, {y}) with {button} button")
        except Exception as e:
            self.logger.error(f"Failed to click: {str(e)}")
            raise ControlException(f"Click failed: {str(e)}")
    
    def type_text(self, text: str, interval: float = 0.05) -> None:
        """Type text.
        
        Args:
            text: Text to type
            interval: Delay between keystrokes
        """
        try:
            if self.pyautogui is None:
                raise ControlException("pyautogui not available")
            self.pyautogui.typewrite(text, interval=interval)
            self.logger.info(f"Typed: {text}")
        except Exception as e:
            self.logger.error(f"Failed to type: {str(e)}")
            raise ControlException(f"Type failed: {str(e)}")
    
    def press_key(self, key: str) -> None:
        """Press a key.
        
        Args:
            key: Key name (e.g., 'enter', 'tab', 'shift')
        """
        try:
            if self.pyautogui is None:
                raise ControlException("pyautogui not available")
            self.pyautogui.press(key)
            self.logger.info(f"Pressed key: {key}")
        except Exception as e:
            self.logger.error(f"Failed to press key: {str(e)}")
            raise ControlException(f"Key press failed: {str(e)}")
    
    def hotkey(self, *keys: str) -> None:
        """Press multiple keys simultaneously.
        
        Args:
            *keys: Keys to press together (e.g., 'ctrl', 'c')
        """
        try:
            if self.pyautogui is None:
                raise ControlException("pyautogui not available")
            self.pyautogui.hotkey(*keys)
            self.logger.info(f"Hotkey: {' + '.join(keys)}")
        except Exception as e:
            self.logger.error(f"Failed hotkey: {str(e)}")
            raise ControlException(f"Hotkey failed: {str(e)}")
    
    def get_screen_size(self) -> Tuple[int, int]:
        """Get screen dimensions.
        
        Returns:
            (width, height) tuple
        """
        try:
            if self.pyautogui is None:
                raise ControlException("pyautogui not available")
            size = self.pyautogui.size()
            self.logger.info(f"Screen size: {size}")
            return size
        except Exception as e:
            self.logger.error(f"Failed to get screen size: {str(e)}")
            raise ControlException(f"Failed to get screen size: {str(e)}")
    
    def screenshot(self, filename: Optional[str] = None):
        """Take a screenshot.
        
        Args:
            filename: Optional filename to save screenshot
            
        Returns:
            Screenshot image
        """
        try:
            if self.pyautogui is None:
                raise ControlException("pyautogui not available")
            screenshot = self.pyautogui.screenshot()
            if filename:
                screenshot.save(filename)
                self.logger.info(f"Screenshot saved: {filename}")
            return screenshot
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            raise ControlException(f"Screenshot failed: {str(e)}")
    
    def scroll(self, x: int, y: int, clicks: int = 5) -> None:
        """Scroll at coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            clicks: Number of scroll clicks (positive = up, negative = down)
        """
        try:
            if self.pyautogui is None:
                raise ControlException("pyautogui not available")
            self.pyautogui.scroll(clicks, x, y)
            self.logger.info(f"Scrolled at ({x}, {y}) by {clicks} clicks")
        except Exception as e:
            self.logger.error(f"Failed to scroll: {str(e)}")
            raise ControlException(f"Scroll failed: {str(e)}")
