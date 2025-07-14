"""
Design a Plugin System for IDE
Design a plugin system for an IDE that supports dynamic creation, registration, unregistration, and management of various plugins. The system must support:

Version Control for Plugins - Handle different plugin versions and compatibility
Dependency Management - Manage dependencies between plugins, prevent circular dependencies
Event System - Enable IDE notifications and inter-plugin communication

Required Plugin Types to Support:

Syntax Highlighter
Code Formatter
Logger
Debugger

Key Requirements:

Plugins should be dynamically loaded and unloaded at runtime
System should prevent activation of plugins with unmet dependencies
Support plugin lifecycle management (register, activate, deactivate, unregister)
Provide event-driven communication between plugins
Handle version compatibility between dependent plugins
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Set, Optional
from collections import defaultdict, deque

class PluginType(Enum):
    SYNTAX_HIGHLIGHTER = "syntax_highlighter"
    CODE_FORMATTER = "code_formatter"
    LOGGER = "logger"
    DEBUGGER = "debugger"

class PluginStatus(Enum):
    INACTIVE = "inactive"
    ACTIVE = "active"
    DISABLED = "disabled"

class BasePlugin(ABC):
    def __init__(self, name: str, version: str, plugin_type: PluginType):
        # basic plugin properties that all plugins must have
        self.name = name
        self.version = version
        self.plugin_type = plugin_type
        self.status = PluginStatus.INACTIVE
        self.dependencies = []  # list of plugin names this plugin depends on
    
    @abstractmethod
    def activate(self):
        # plugin-specific activation logic
        pass
    
    @abstractmethod
    def deactivate(self):
        # plugin-specific deactivation logic
        pass
    
    def get_info(self):
        # return plugin metadata for management
        return {
            'name': self.name,
            'version': self.version,
            'type': self.plugin_type.value,
            'status': self.status.value,
            'dependencies': self.dependencies
        }

class SyntaxHighlighter(BasePlugin):
    def __init__(self, name: str, version: str):
        super().__init__(name, version, PluginType.SYNTAX_HIGHLIGHTER)
        self.supported_languages = []
    
    def activate(self):
        # register syntax highlighting rules with IDE
        self.status = PluginStatus.ACTIVE
        print(f"Syntax highlighter {self.name} activated")
    
    def deactivate(self):
        # unregister syntax highlighting rules
        self.status = PluginStatus.INACTIVE
        print(f"Syntax highlighter {self.name} deactivated")

class EventBus:
    def __init__(self):
        # event system for plugin communication
        self.listeners = defaultdict(list)  # {event_type: [callback_functions]}
    
    def register_listener(self, event_type: str, callback):
        # plugins can register to listen for specific events
        self.listeners[event_type].append(callback)
    
    def emit_event(self, event_type: str, data=None):
        # broadcast event to all registered listeners
        for callback in self.listeners[event_type]:
            try:
                callback(data)
            except Exception as e:
                print(f"Error in event listener: {e}")

class PluginManager:
    def __init__(self):
        # core plugin management data structures
        self.registered_plugins = {}  # {plugin_name: plugin_instance}
        self.plugin_dependencies = defaultdict(list)  # {plugin_name: [dependency_names]}
        self.event_bus = EventBus()
        self.active_plugins = set()  # track currently active plugins
    
    def register_plugin(self, plugin: BasePlugin) -> bool:
        # register new plugin with dependency validation
        if plugin.name in self.registered_plugins:
            print(f"Plugin {plugin.name} already registered")
            return False
        
        # check if all dependencies are available
        if not self._validate_dependencies(plugin):
            print(f"Plugin {plugin.name} has unmet dependencies")
            return False
        
        # register plugin and update dependency graph
        self.registered_plugins[plugin.name] = plugin
        self.plugin_dependencies[plugin.name] = plugin.dependencies
        
        # emit registration event for other plugins
        self.event_bus.emit_event('plugin_registered', plugin.get_info())
        print(f"Plugin {plugin.name} registered successfully")
        return True
    
    def unregister_plugin(self, plugin_name: str) -> bool:
        # unregister plugin and handle dependent plugins
        if plugin_name not in self.registered_plugins:
            print(f"Plugin {plugin_name} not found")
            return False
        
        # check if other plugins depend on this one
        dependents = self._find_dependents(plugin_name)
        if dependents:
            print(f"Cannot unregister {plugin_name}, other plugins depend on it: {dependents}")
            return False
        
        # deactivate and remove plugin
        if plugin_name in self.active_plugins:
            self.deactivate_plugin(plugin_name)
        
        plugin = self.registered_plugins[plugin_name]
        del self.registered_plugins[plugin_name]
        del self.plugin_dependencies[plugin_name]
        
        # emit unregistration event
        self.event_bus.emit_event('plugin_unregistered', plugin.get_info())
        print(f"Plugin {plugin_name} unregistered successfully")
        return True
    
    def activate_plugin(self, plugin_name: str) -> bool:
        # activate plugin with dependency resolution
        if plugin_name not in self.registered_plugins:
            print(f"Plugin {plugin_name} not registered")
            return False
        
        plugin = self.registered_plugins[plugin_name]
        
        # activate all dependencies first using topological sort
        activation_order = self._get_activation_order(plugin_name)
        if not activation_order:
            print(f"Circular dependency detected for {plugin_name}")
            return False
        
        # activate plugins in dependency order
        for dep_name in activation_order:
            if dep_name not in self.active_plugins:
                dep_plugin = self.registered_plugins[dep_name]
                dep_plugin.activate()
                self.active_plugins.add(dep_name)
        
        print(f"Plugin {plugin_name} activated successfully")
        return True
    
    def deactivate_plugin(self, plugin_name: str) -> bool:
        # deactivate plugin and handle dependents
        if plugin_name not in self.active_plugins:
            print(f"Plugin {plugin_name} not active")
            return False
        
        plugin = self.registered_plugins[plugin_name]
        plugin.deactivate()
        self.active_plugins.remove(plugin_name)
        
        print(f"Plugin {plugin_name} deactivated successfully")
        return True
    
    def _validate_dependencies(self, plugin: BasePlugin) -> bool:
        # check if all plugin dependencies are registered
        for dep_name in plugin.dependencies:
            if dep_name not in self.registered_plugins:
                return False
        return True
    
    def _find_dependents(self, plugin_name: str) -> List[str]:
        # find all plugins that depend on the given plugin
        dependents = []
        for name, deps in self.plugin_dependencies.items():
            if plugin_name in deps:
                dependents.append(name)
        return dependents
    
    def _get_activation_order(self, plugin_name: str) -> Optional[List[str]]:
        # use topological sort to determine plugin activation order
        visited = set()
        rec_stack = set()
        order = []
        
        def dfs(name):
            if name in rec_stack:
                return False  # circular dependency
            if name in visited:
                return True
            
            visited.add(name)
            rec_stack.add(name)
            
            for dep in self.plugin_dependencies[name]:
                if not dfs(dep):
                    return False
            
            rec_stack.remove(name)
            order.append(name)
            return True
        
        if dfs(plugin_name):
            return order
        return None  # circular dependency detected
    
    def get_plugin_status(self):
        # return current status of all plugins
        return {
            'registered': len(self.registered_plugins),
            'active': len(self.active_plugins),
            'plugins': [plugin.get_info() for plugin in self.registered_plugins.values()]
        }