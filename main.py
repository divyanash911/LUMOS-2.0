import os
import json
import jsonschema

from utils import export_schema_to_mermaid, LDLSchema


schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'LDLSchema.json')
example_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs', 'example_system.json')

with open(schema_path, 'r') as schema_file:
    schema = LDLSchema(schema_path)

with open(example_path, 'r') as example_file:
    example_system = json.load(example_file)


mermaid_code = export_schema_to_mermaid(schema.get_schema(), "yes")

with open("code.mmt", "w+") as f:
    f.write(mermaid_code)