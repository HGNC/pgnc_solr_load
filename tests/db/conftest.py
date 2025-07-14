"""
Pytest configuration specific for db tests
"""
import os
import sys

# Add the data-load path to sys.path so we can import the db modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
data_load_path = os.path.join(project_root, 'bin/data-load')
if data_load_path not in sys.path:
    sys.path.insert(0, data_load_path)

# Also add the db path directly
db_path = os.path.join(data_load_path, 'db')
if db_path not in sys.path:
    sys.path.insert(0, db_path)

# Clear any mock modules that might interfere with real imports
modules_to_clear = [
    'db', 'db.config', 'db.models', 'db.enum_types', 'db.insert',
    'db.models.base', 'db.models.gene', 'db.models.symbol', 'db.models.user',
    'db.models.location', 'db.models.name', 'db.models.gene_has_name',
    'db.models.gene_has_location', 'db.models.locus_type', 'db.models.gene_has_locus_type',
    'db.models.xref', 'db.models.gene_has_xref', 'db.models.gene_has_symbol',
    'db.models.assembly', 'db.models.assembly_has_location', 'db.models.external_resource',
    'db.models.gene_has_location', 'db.models.locus_group', 'db.models.role',
    'db.models.species', 'db.models.user_has_role',
    'db.insert.gene_symbol', 'db.insert.gene_name', 'db.insert.gene_location',
    'db.insert.gene_locus_type', 'db.insert.gene_xref',
    'db.enum_types.gene_status', 'db.enum_types.nomenclature', 'db.enum_types.basic_status'
]

for module in modules_to_clear:
    if module in sys.modules:
        del sys.modules[module]
