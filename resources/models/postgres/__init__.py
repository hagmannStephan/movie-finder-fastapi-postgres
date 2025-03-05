import pkgutil
import importlib

__all__ = []

# Dynamically import all modules in the current package
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    module = importlib.import_module(f".{module_name}", package=__name__)
    # Get all public attributes (not starting with '_')
    public_attrs = [attr for attr in dir(module) if not attr.startswith("_")]
    __all__.extend(public_attrs)
    globals().update({attr: getattr(module, attr) for attr in public_attrs})
