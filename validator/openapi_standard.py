import json
import re
import yaml
from jsonschema import validate, ValidationError

from .models import RequestModel, ReportSectionRule, ReportSection, Report, ResponseModel

# Function to validate API specs and return simplified error messages
def validate_api_spec(req:RequestModel) -> ResponseModel:
    # Section - Syntax Validation
    syntax_validation_rule = ReportSectionRule(
        rule="Check if the provided spec is valid JSON or YAML.",
        humanReview=False,
        recommendation=str.upper(req.format_type)
    )
    syntax_validation_section = ReportSection(
        id="1.0",
        name="Syntax validation",
        rules=[syntax_validation_rule]
    )

    # Section - Version Compatibility
    regex = re.compile(openapi_schema_version())
    if ('openapi' in req.api_spec) and (regex.match(req.api_spec['openapi'])):
        version_compatibility_message = f"Version compatibility check passed. (Version {req.api_spec['openapi']})"
    else:
        version_compatibility_message = "Version compatibility check failed."

    version_compatibility_rule = ReportSectionRule(
        rule="Verify the spec matches the declared OpenAPI version.",
        humanReview=False,
        recommendation=version_compatibility_message
    )
    version_compatibility_section = ReportSection(
        id="2.0",
        name="Version compatibility",
        rules=[version_compatibility_rule]
    )

    # Section - Schema Validation
    schema_validation_rule = ReportSectionRule(
        rule="Ensure the spec adheres to the OpenAPI schema structure.",
        humanReview=False,
        recommendation=validate_schema(req.api_spec)
    )
    schema_validation_section = ReportSection(
        id="3.0",
        name="Schema validation",
        rules=[schema_validation_rule]
    )

    # Report
    report = Report(
        name="OpenAPI Standard",
        sections=[syntax_validation_section, version_compatibility_section, schema_validation_section]
    )

    return ResponseModel(
        report=report,
        errors=[])

def validate_schema(api_spec) -> str:
    # Load OpenAPI standard schema from external JSON file
    with open("./validator/openapi_standard_schema.json", "r") as f:
        openapi_standard = json.load(f)

    try:
        validate(instance=api_spec, schema=openapi_standard)
        return "Complies to OpenAPI schema."
    except ValidationError as e:
        # Extract relevant error information
        error_path = " -> ".join([str(x) for x in list(e.path)]) if e.path else "Unknown path"
        error_message = f"Error at {error_path}: {e.message}"
        return error_message

def openapi_schema_version() -> str:
    with open("./validator/openapi_standard_schema.json", "r") as f:
        openapi_standard = json.load(f)

    return openapi_standard['properties']['openapi']['pattern']

def get_api_spec(file):
    try:
        api_spec = json.load(file)
        return api_spec, green("JSON")
    except ValueError:
        try:
            api_spec = yaml.safe_load(file)
            return api_spec, green("YAML")
        except yaml.YAMLError:
            return {}, red("Unknown")

def green(message) -> str:
    return ":green[" + message + "]"

def red(message) -> str:
    return ":red[" + message + "]"
