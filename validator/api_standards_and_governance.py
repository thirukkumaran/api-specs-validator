import os
import yaml

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

from .models import RequestModel, ReportSectionRule, ReportSection, Report, ResponseModel

load_dotenv()

class ASGSectionRule:
    def __init__(self, id, rule: str, humanReview: bool):
        self.rule = rule
        self.humanReview = humanReview

class ASGSection:
    def __init__(self, id, name: str, rules: list[ASGSectionRule]):
        self.id = id
        self.name = name
        self.rules = rules

class ASG:
    def __init__(self, **entries):
        self.__dict__.update(entries)
    def __init__(self, name: str, sections: list[ASGSection]):
        self.name = name
        self.sections = sections

def validate_api_spec(req:RequestModel) -> ResponseModel:
    with open('./validator/api_standards_and_governance.yaml', 'r') as f:
        # data = yaml.load(f, Loader=yaml.SafeLoader)
        data = yaml.safe_load(f)
        asg = ASG(**data)

    print("1")
    llm = ChatOpenAI(
        # api_key=os.getenv("API_KEY"),
        api_key="sk-vx_6rphVLikmvPDp4J60qw",
        openai_api_base="https://litellm.govtext.gov.sg",
        model="gpt-4o-prd-gcc2-lb",
        temperature=0.1,
        default_headers={"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0"},
    )
    print("2")

    prompt_template: str = '''
    Given the following OpenAPI specification:

    {api_spec}

    Please analyse this specification against the following API standard "{standard_name}":
    {standard_rule}

    Provide specific recommendations for addressing the gaps found, cite all the relevant information in the gap and be concise.
    - Don't include a title.
    - Don't include an overview
    - Don't include a conclusion
    - Don't include a recommendation if it is already compliant, think carefully and step-by-step

    Output in HTML format and remove the enclosing ```html and ```
    '''

    prompt = PromptTemplate.from_template(template=prompt_template)

    reportSections: list[ReportSection] = []
    for section in asg.sections:
        reportSectionRules: list[ReportSectionRule] = []
        for rule in section['rules']:
            if rule['humanReview']:
                reportSectionRules.append(ReportSectionRule(
                    rule=rule['rule'],
                    humanReview=rule['humanReview'],
                    recommendation="This guideline requires human review and cannot be validated by software."
                ))
            else:
                # content += f"Evaluate via LLM.\n"
                prompt_formatted: str = prompt.format(
                    api_spec=req.api_spec,
                    standard_name=section['name'],
                    standard_rule=rule['rule'],
                )

                res = llm.invoke(input=prompt_formatted)
                reportSectionRules.append(ReportSectionRule(
                    rule=rule['rule'],
                    humanReview=rule['humanReview'],
                    recommendation=res.content
                ))
        reportSections.append(ReportSection(section['id'], section['name'], reportSectionRules))

    return ResponseModel(Report(asg.name, reportSections), [])
