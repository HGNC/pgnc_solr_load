"""
Pytest configuration specific for model tests
"""
import os
import sys

# Add the data-load path to sys.path so we can import the models
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
data_load_path = os.path.join(project_root, 'bin/data-load')
if data_load_path not in sys.path:
    sys.path.insert(0, data_load_path)

# Also add the models path directly
models_path = os.path.join(data_load_path, 'db', 'models')
if models_path not in sys.path:
    sys.path.insert(0, models_path)

# Clear any mock modules that might interfere with real imports
modules_to_clear = [
    'db', 'db.models', 'db.models.base', 'db.models.gene', 'db.models.symbol',
    'db.models.user', 'db.models.location', 'db.models.gene_has_symbol'
]

for module in modules_to_clear:
    if module in sys.modules and hasattr(sys.modules[module], '_mock_name'):
        del sys.modules[module]
