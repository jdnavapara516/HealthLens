from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

from app.core.config import settings


class GroqReportService:
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.groq_model or 'openai/gpt-oss-120b',
            temperature=0.2,
            api_key=settings.groq_api_key,
        )

    def generate_report(self, extracted_text: str) -> str:
        response = self.llm.invoke([HumanMessage(content=(
            'Analyze this medical report. Summarize reported facts, abnormal '
            'and normal values, and possible clinical significance without '
            'inventing information or giving a definitive diagnosis. Return '
            'the result as readable plain text or simple Markdown with short '
            'headings, paragraphs, and bullet points. Do not use tables, '
            'table syntax, columns, or dense data grids.\n\n'
            f'{extracted_text}'
        ))])
        return str(response.content).strip()

    def answer_question(self, prompt: str) -> str:
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return str(response.content).strip()
