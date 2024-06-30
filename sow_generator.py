import streamlit as st
from docx import Document
import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
system = "You are presale engineer with 15 years of experience, working at system integrator company called TeraSky. Your job is to generate Scope of work document that is presented to TeraSky customers. Use professional  and clear language."

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system,
        ),
        ("human", "{input}"),
    ]
)
executive_summary_descirption = "The executive summary includes the following: a high-level overview of the project; business and technical drivers for doing the project; and brief description of the customer's business and technical objectives. In addition, we briefly summarize TeraSky professional services to be delivered to meet the customer’s objectives."
current_challanges_description = "In this part we will describe what is the status on the customer side – system in use, challenges, what is not working well, what we want to improve or allow the customer to achieve."
proposed_soltion_description = "Describe our proposed solution from a technical architecture perspective.A description of the proposed high-level technical architecture should be included in the Statement of Work. It should address common architectural aspects such as: network infrastructure; data/process flows; software services/components; integration/messaging/middleware; security; deployment models; operations/support models. (As appropriate, based on the type of project)."
llmchain = LLMChain(llm=llm, prompt=prompt)


def improve_through_agent(current_text, current_context, section_description):
    improvement = llmchain.run({"input": "You are generating the section of the document called " + current_context + ". This is section description: " + section_description + ". This is the current text that was provided: " + current_text + ". Fix spelling mistakes and rephrase if needed."})
    return improvement


def replace_text(placeholder, content, run_text, count, doc):
    replace = re.sub(placeholder, content, run_text, count)
    if replace != run_text:
        run_text = replace


def generate_scope_of_work(project_name, customer_name, executive_summary, current_challanges, proposed_solution):
    doc = Document("sow_template.docx")
    for para in doc.paragraphs:
        for run in para.runs:
            if run.text:
                replace_title = re.sub("< Project Name >", project_name, run.text, 999)
                if replace_title != run.text:
                    run.text = replace_title
                replace_executive_summary = re.sub("<Executive Summary>", executive_summary, run.text, 999)
                if replace_executive_summary != run.text:
                    improved_summary = improve_through_agent(executive_summary, "Executive Summary", executive_summary_descirption)
                    run.text = improved_summary
                replace_current_challanges = re.sub("<current challenges>", current_challanges, run.text, 999)
                if replace_current_challanges != run.text:
                    improved_challanges = improve_through_agent(executive_summary, "Current Challenges", current_challanges_description)
                    run.text = improved_challanges
                    "<current challenges>"
                replace_proposed_solution = re.sub("<proposed solution>", proposed_solution, run.text, 999)
                if replace_proposed_solution != run.text:
                    improved_executive_summary = improve_through_agent(executive_summary, "Proposed Solution", proposed_soltion_description)
                    run.text = improved_executive_summary
    # Save the document
    new_file_path = customer_name+".docx"
    doc.save(new_file_path)
    return "created file: " + new_file_path


st.header('Scope of Work Generator')
project_name = st.text_input('Enter Project Name')
customer_name = st.text_input('Enter the Customer Name')
executive_summary = st.text_area('Enter the Project Description')
current_challanges = st.text_area('Enter Current Challenges')
proposed_solution = st.text_area('Enter Proposed Solution')

if st.button('Generate Scope of Work'):
    scope_of_work = generate_scope_of_work(project_name, customer_name, executive_summary, current_challanges, proposed_solution)
    st.write(scope_of_work)
