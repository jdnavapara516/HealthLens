from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.graph.state import ChatGraphState
from app.llm.service import GroqReportService


SYSTEM_INSTRUCTIONS = (
    '''You are a careful medical-report assistant. Answer only from the supplied medical report context and relevant conversation history for follow-up questions. Never invent values, diagnoses, symptoms, medical history, or other medical information.

If the requested information is not present in the supplied report context, clearly state that the information is not available in the report.

Explain medical values and findings in simple, clear language. Clearly distinguish information directly stated in the report from general medical interpretation. Do not make definitive diagnoses or provide dangerous, misleading, or overconfident medical advice.

For potentially serious or concerning findings, advise the user to consult a qualified healthcare professional.

Return responses as plain text only. Do not use Markdown formatting. Do not use headings, bullet points, numbered lists, tables, table syntax, columns, bold text, italic text, code blocks, or special formatting. Write responses as short, clear paragraphs that are easy to read on a small screen.
'''
)


def generate_answer(state: ChatGraphState, *, groq_service: GroqReportService) -> ChatGraphState:
    context = "\n\n".join(
        f"[Chunk {chunk.id}, page {chunk.page or 'unknown'}]\n{chunk.content}"
        for chunk, _distance in state.get("matches", [])
    ) or "No relevant report context was found."

    messages = [SystemMessage(content=SYSTEM_INSTRUCTIONS)]
    for item in state.get("history", [])[-20:]:
        role = item.get("role", "").upper()
        content = item.get("content", "").strip()
        if not content:
            continue
        messages.append(
            HumanMessage(content=content)
            if role == "USER"
            else AIMessage(content=content)
        )

    messages.append(HumanMessage(content=(
        f"REPORT CONTEXT\n{context}\n\n"
        f"CURRENT USER QUESTION\n{state['message']}"
    )))
    answer = groq_service.llm.invoke(messages).content
    answer = str(answer).strip()
    if not answer:
        raise ValueError("Groq returned an empty answer.")
    return {"answer": answer}