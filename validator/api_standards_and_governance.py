import asyncio
import os
import yaml

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

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
        data = yaml.safe_load(f)
        asg = ASG(**data)

    # Define the prompt
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

    # Define the large language model
    llm = ChatOpenAI(
        api_key=os.getenv("API_KEY"),
        openai_api_base="https://litellm.govtext.gov.sg",
        model="gpt-4o-prd-gcc2-lb",
        temperature=0.1,
        default_headers={"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0"},
    )

    # Define the output parser
    output_parser = StrOutputParser()

    # Define the chain
    chain = prompt | llm | output_parser

    async def process_single_query(query: dict) -> str:
        if query['human_review']:
            return "This guideline requires human review and cannot be validated by software."
        else:
            result = await chain.ainvoke(query)
            return result

    async def process_multiple_queries(queries: list[dict]) -> list[str]:
        tasks = [process_single_query(query) for query in queries]
        results = await asyncio.gather(*tasks)
        return results

    queries = []
    reportSections: list[ReportSection] = []
    for section in asg.sections:
        reportSectionRules: list[ReportSectionRule] = []
        for rule in section['rules']:
            queries.append({
                'api_spec': req.api_spec,
                'standard_id': section['id'],
                'standard_name': section['name'],
                'standard_rule': rule['rule'],
                'human_review': rule['humanReview']
            })

            reportSectionRules.append(ReportSectionRule(
                rule=rule['rule'],
                humanReview=rule['humanReview'],
                recommendation=""
            ))

        reportSections.append(ReportSection(section['id'], section['name'], reportSectionRules))

    results = asyncio.run(process_multiple_queries(queries))

    i = 0
    for s in reportSections:
        for r in s.rules:
            r.recommendation = results[i]
            i += 1

    return ResponseModel(Report(asg.name, reportSections), [])
