from typing import Any


class RequestModel:
    def __init__(self, format_type: str, api_spec: Any):
        self.format_type = format_type
        self.api_spec = api_spec

class ReportSectionRule:
    def __init__(self, rule: str, humanReview: bool, recommendation: str):
        self.rule = rule
        self.humanReview = humanReview
        self.recommendation = recommendation

class ReportSection:
    def __init__(self, id, name: str, rules: list[ReportSectionRule]):
        self.id = id
        self.name = name
        self.rules = rules

class Report:
    def __init__(self, name: str, sections: list[ReportSection]):
        self.name = name
        self.sections = sections

class ResponseModel:
    def __init__(self, report: Report, errors: list[str]):
        self.report = report
        self.errors = errors