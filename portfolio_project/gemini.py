import os
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

GOOGLE_API_KEY = 'AIzaSyCTnxP9mxqhaoVReOosmh5Y4O8ezd9d-cY'
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.1)


def sentiment(sentence):
    analyze_prompt = PromptTemplate(
        input_variables=["feedback"],
        template="Analyze the following customer feedback:\n{feedback}\n\nClassify the statement as negative , positive or neutral feedback. Only give the answer."
    )
    analyze_chain = LLMChain(llm=llm, prompt=analyze_prompt)
    result = analyze_chain.run(feedback=sentence)
    return result