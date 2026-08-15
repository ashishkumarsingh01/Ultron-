"""
Plugin manager for Ultron Agent Kernel.
"""

import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
import importlib
import sys

from ultron.plugins.plugin_base import UltronPlugin
from ultron.utils.errors import PluginException
from ultron.utils.logger import setup_logger


class PluginManager:
    """Manages Ultron plugins."""
    
    def __init__(self, plugin_dir: str = "./plugins"):
        """Initialize plugin manager.
        
        Args:
            plugin_dir: Directory containing plugins
        """
        self.plugin_dir = Path(plugin_dir)
        self.plugins: Dict[str, UltronPlugin] = {}
        self.logger = setup_logger("ultron.plugins.manager")
    
    def load_plugin(self, plugin_path: str) -> UltronPlugin:
        """Load a plugin from file.
        
        Args:
            plugin_path: Path to plugin file
            
        Returns:
            Loaded plugin instance
        """
        try:
            plugin_path = Path(plugin_path)
            if not plugin_path.exists():
                raise PluginException(f"Plugin not found: {plugin_path}")
            
            # Dynamically import plugin
            spec = importlib.util.spec_from_file_location(
                plugin_path.stem,
                plugin_path
            )
            module = importlib.util.module_from_spec(spec)
            sys.modules[plugin_path.stem] = module
            spec.loader.exec_module(module)
            
            # Find plugin class
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, UltronPlugin) and 
                    attr != UltronPlugin):
                    plugin = attr()
                    plugin.initialize()
                    self.plugins[plugin.name] = plugin
                    self.logger.info(f"Loaded plugin: {plugin.name}")
                    return plugin
            
            raise PluginException(f"No plugin class found in {plugin_path}")
        except Exception as e:
            self.logger.error(f"Failed to load plugin: {str(e)}")
            raise PluginException(f"Plugin loading failed: {str(e)}")
    
    def load_plugins_from_dir(self) -> List[UltronPlugin]:
        """Load all plugins from plugin directory.
        
        Returns:
            List of loaded plugins
        """
        loaded = []
        if not self.plugin_dir.exists():
            self.logger.warning(f"Plugin directory not found: {self.plugin_dir}")
            return loaded
        
        for plugin_file in self.plugin_dir.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue
            try:
                plugin = self.load_plugin(str(plugin_file))
                loaded.append(plugin)
            except Exception as e:
                self.logger.error(f"Failed to load {plugin_file}: {str(e)}")
        
        return loaded
    
    def execute_plugin(self, plugin_name: str, *args, **kwargs) -> Any:
        """Execute a plugin.
        
        Args:
            plugin_name: Name of plugin to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Plugin execution result
        """
        try:
            if plugin_name not in self.plugins:
                raise PluginException(f"Plugin not found: {plugin_name}")
            
            plugin = self.plugins[plugin_name]
            if not plugin.enabled:
                raise PluginException(f"Plugin disabled: {plugin_name}")
            
            result = plugin.execute(*args, **kwargs)
            self.logger.info(f"Executed plugin: {plugin_name}")
            return result
        except Exception as e:
            self.logger.error(f"Plugin execution failed: {str(e)}")
            raise PluginException(f"Plugin execution error: {str(e)}")
    
    def disable_plugin(self, plugin_name: str) -> None:
        """Disable a plugin.
        
        Args:
            plugin_name: Name of plugin to disable
        """
        if plugin_name in self.plugins:
            self.plugins[plugin_name].enabled = False
            self.logger.info(f"Disabled plugin: {plugin_name}")
    
    def enable_plugin(self, plugin_name: str) -> None:
        """Enable a plugin.
        
        Args:
            plugin_name: Name of plugin to enable
        """
        if plugin_name in self.plugins:
            self.plugins[plugin_name].enabled = True
            self.logger.info(f"Enabled plugin: {plugin_name}")
    
    def get_plugins(self) -> Dict[str, UltronPlugin]:
        """Get all loaded plugins.
        
        Returns:
            Dictionary of plugins
        """
        return self.plugins.copy()
    
    def unload_plugin(self, plugin_name: str) -> None:
        """Unload a plugin.
        
        Args:
            plugin_name: Name of plugin to unload
        """
        if plugin_name in self.plugins:
            self.plugins[plugin_name].shutdown()
            del self.plugins[plugin_name]
            self.logger.info(f"Unloaded plugin: {plugin_name}")
