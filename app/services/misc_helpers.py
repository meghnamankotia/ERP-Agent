from schemas.tables import table_schemas
from schemas.dependencies import dependency_dict

def fetch_schema(table_name:str)->str:
    """An MCP tool to fetch the schema of any requested tables, if it exists."""
    if table_name in table_schemas:
        return table_schemas[table_name]
    return 'Table does not exist'

def check_dependencies(table_name:str)->list:
    """An MCP tool to check which tables are dependent on the given table."""
    if table_name in dependency_dict:
        return dependency_dict[table_name]
    return 'Table does not exist'
    