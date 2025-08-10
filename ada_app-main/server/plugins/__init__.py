"""
ADA Plugin System
Dynamic plugin discovery and loading for modular feature architecture
"""

import os
import importlib
import inspect
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod

class PluginBase(ABC):
    """Base class for all ADA plugins"""
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the plugin name"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Return the plugin description"""
        pass
    
    @abstractmethod
    def get_functions(self) -> List[Dict[str, Any]]:
        """Return list of function declarations for Gemini integration"""
        pass
    
    @abstractmethod
    async def execute_function(self, function_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a plugin function"""
        pass
    
    @abstractmethod
    def get_widget_info(self) -> Optional[Dict[str, Any]]:
        """Return frontend widget information if applicable"""
        pass

class PluginManager:
    """Manages plugin discovery, loading, and execution"""
    
    def __init__(self):
        self.plugins: Dict[str, PluginBase] = {}
        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))
    
    def discover_plugins(self) -> List[str]:
        """Discover available plugins in the plugins directory"""
        plugin_files = []
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                plugin_name = filename[:-3]  # Remove .py extension
                plugin_files.append(plugin_name)
        return plugin_files
    
    def load_plugins(self) -> Dict[str, PluginBase]:
        """Load all discovered plugins"""
        plugin_names = self.discover_plugins()
        
        for plugin_name in plugin_names:
            try:
                # Import the plugin module
                module = importlib.import_module(f'plugins.{plugin_name}')
                
                # Find PluginBase subclasses in the module
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, PluginBase) and 
                        obj != PluginBase):
                        # Instantiate the plugin
                        plugin_instance = obj()
                        self.plugins[plugin_instance.get_name()] = plugin_instance
                        print(f"Loaded plugin: {plugin_instance.get_name()}")
                        break
                        
            except Exception as e:
                print(f"Failed to load plugin {plugin_name}: {e}")
        
        return self.plugins
    
    def get_all_functions(self) -> List[Dict[str, Any]]:
        """Get all function declarations from all plugins"""
        functions = []
        for plugin in self.plugins.values():
            functions.extend(plugin.get_functions())
        return functions
    
    def get_function_mapping(self) -> Dict[str, callable]:
        """Get mapping of function names to their execution methods"""
        mapping = {}
        for plugin in self.plugins.values():
            for func_info in plugin.get_functions():
                func_name = func_info['name']
                mapping[func_name] = lambda plugin=plugin, func_name=func_name, **kwargs: \
                    plugin.execute_function(func_name, **kwargs)
        return mapping
    
    def get_widget_info(self) -> Dict[str, Dict[str, Any]]:
        """Get all widget information from plugins"""
        widgets = {}
        for plugin in self.plugins.values():
            widget_info = plugin.get_widget_info()
            if widget_info:
                widgets[plugin.get_name()] = widget_info
        return widgets

# Global plugin manager instance
plugin_manager = PluginManager()
