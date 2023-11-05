import os
from decouple import config
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains.llm import LLMChain


# Initialize environment keys
os.environ["OPENAI_API_KEY"] = config('OPENAI_API_KEY')
os.environ["APIFY_API_TOKEN"] = config('APIFY_API_TOKEN')


def understand_prescription(prescription: str):
    prompt_template = f"""
    You will be given a prescription information, in unstructured text. 
    I want you to extract the following information and return it to me in
    this format.
    
    Patient Information:
    Name: Mary Smith
    Patient ID: Jan 9, 20yy
    Address: 123 Broad Street
    Prescription Details:

    Medication: Lipitor 10 mg
    Tablets Quantity: 30
    Dosage: Take 1 tablet every day.
    Refills: 5 times
    Labet (Generic): Yes
    Physician Information:

    Doctor's Name: Dr. Brown, M.D.
    DEA No.: 1234563
    State License No.: 65432
    
    If an information is missing just use NA
    """
    prompt = PromptTemplate.from_template(prompt_template)
        
    # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    
    print(llm_chain.predict(prescription))
    
def verify_prescription(prescription: str):
    prompt_template = f"""
        You will be given a prescription information, in unstructured text. 
        I want you to check the prescription there and let me know what you think 
        The prescription is going to solve, then ask any 
        
        Patient Information:
        Name: Mary Smith
        Patient ID: Jan 9, 20yy
        Address: 123 Broad Street
        Prescription Details:

        Medication: Lipitor 10 mg
        Tablets Quantity: 30
        Dosage: Take 1 tablet every day.
        Refills: 5 times
        Labet (Generic): Yes
        Physician Information:

        Doctor's Name: Dr. Brown, M.D.
        DEA No.: 1234563
        State License No.: 65432
        
        If an information is missing just use NA
    """
    prompt = PromptTemplate.from_template(prompt_template)
        
    # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    
    print(llm_chain.predict(prescription))