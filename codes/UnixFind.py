import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Set

# Abstract filter interface for flexible filtering logic
class FileFilter(ABC):
    @abstractmethod
    def matches(self, file_path: str) -> bool:
        # return True if file matches filter criteria
        pass

# Size-based filter for files over specified size
class SizeFilter(FileFilter):
    def __init__(self, min_size_mb: float):
        # store minimum size in bytes for comparison
        self.min_size_bytes = min_size_mb * 1024 * 1024
    
    def matches(self, file_path: str) -> bool:
        try:
            # get file size and compare with threshold
            file_size = os.path.getsize(file_path)
            return file_size >= self.min_size_bytes
        except OSError:
            # handle permission errors or file not found
            return False

# Extension-based filter for specific file types
class ExtensionFilter(FileFilter):
    def __init__(self, extensions: Set[str]):
        # store extensions in lowercase for case-insensitive matching
        self.extensions = {ext.lower().lstrip('.') for ext in extensions}
    
    def matches(self, file_path: str) -> bool:
        # extract file extension and check against allowed extensions
        file_ext = Path(file_path).suffix.lower().lstrip('.')
        return file_ext in self.extensions

# Composite filter for combining multiple filters with AND/OR logic
class CompositeFilter(FileFilter):
    def __init__(self, filters: List[FileFilter], operator: str = 'AND'):
        self.filters = filters
        self.operator = operator.upper()
    
    def matches(self, file_path: str) -> bool:
        if not self.filters:
            return True
        
        # apply logical operator to combine filter results
        if self.operator == 'AND':
            return all(f.matches(file_path) for f in self.filters)
        elif self.operator == 'OR':
            return any(f.matches(file_path) for f in self.filters)
        else:
            raise ValueError(f"Unsupported operator: {self.operator}")

# Core file search engine with directory traversal
class FileSearcher:
    def __init__(self, file_filter: FileFilter = None):
        self.file_filter = file_filter
    
    def search(self, root_path: str) -> List[str]:
        # recursively search directory tree and apply filters
        if not os.path.exists(root_path):
            raise FileNotFoundError(f"Path does not exist: {root_path}")
        
        results = []
        self._search_recursive(root_path, results)
        return results
    
    def _search_recursive(self, current_path: str, results: List[str]):
        # recursive directory traversal with filter application
        try:
            if os.path.isfile(current_path):
                # check if file matches filter criteria
                if self.file_filter is None or self.file_filter.matches(current_path):
                    results.append(current_path)
            elif os.path.isdir(current_path):
                # recursively search subdirectories
                for item in os.listdir(current_path):
                    item_path = os.path.join(current_path, item)
                    self._search_recursive(item_path, results)
        except (PermissionError, OSError):
            # handle permission errors gracefully by skipping
            pass

# Fluent API for programmatic usage
class FindBuilder:
    def __init__(self):
        self.filters = []
        self.operator = 'AND'
    
    def larger_than(self, size_mb: float):
        # add size filter to builder chain
        self.filters.append(SizeFilter(size_mb))
        return self
    
    def with_extension(self, *extensions):
        # add extension filter to builder chain
        self.filters.append(ExtensionFilter(set(extensions)))
        return self
    
    def using_operator(self, operator: str):
        # set logical operator for combining filters
        self.operator = operator
        return self
    
    def search(self, path: str) -> List[str]:
        # build final filter and execute search
        if self.filters:
            file_filter = CompositeFilter(self.filters, self.operator)
        else:
            file_filter = None
        
        searcher = FileSearcher(file_filter)
        return searcher.search(path)