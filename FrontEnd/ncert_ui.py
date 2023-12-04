import requests
import streamlit as st
import json

def ask_llm(query):
    LLM_url = r"http://ec2-13-233-104-187.ap-south-1.compute.amazonaws.com:60001/inference_vicuna"
    llm_request_dict = {"queries":str(query)}
    llm_response = requests.post(LLM_url, json = llm_request_dict)
    return llm_response.json()


def call_LLM(query):
    LLM_url = r"http://ec2-13-233-104-187.ap-south-1.compute.amazonaws.com:60001/inference_colbert_vicuna"
    llm_request_dict = {"queries":str(query)}
    llm_response = requests.post(LLM_url, json = llm_request_dict)
    return llm_response.json()

def ask_query(up_llm):
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # response = f"Echo: {prompt}"
        if up_llm == "Ask a query":
            llm_response = call_LLM(prompt)
            response = llm_response['response']
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
                st.markdown("\nSources:\n")
                for idx, (pid,passage,source) in enumerate(zip(llm_response['pids'], llm_response['Passages'], llm_response['Sources'])):
                    with st.expander(f"Source Number: {idx+1}"):
                        st.write(f"PID ==> {pid}")
                        st.write(f"Chapter  ==>  {source['Chapter']}")
                        st.write(f"Page Number  ==>  {source['Page_number']}")
                        st.write(f"Topic  ==>  {source['Topic']}")
                        st.write(f"{passage}")

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        elif up_llm == "Leave planner":
            plan_leave(prompt)
        else:
            ask_llm(prompt)

def plan_leave(prompt):
    print(f"I am leave planner : {prompt}")
    prompt_template = """
        classify the user query in two classes : Apply Leave and Show Leave Plan
        Below are some examples:
        query : Can you apply leave for me?
        class : Apply Leave
        query : Show me how many leaves I have taken so far.
        class : Show Leave Plan
        query : Apply leave for tomorrow.
        class : Apply Leave
        query : Have I taken leave on monday?
        class : Show Leave Plan
        query : {prompt}
        class :
    """

    prompt_template = prompt_template.replace("{prompt}",prompt)
    response = ask_llm(prompt_template)

    st.markdown(response)


st.title("NCERT Bio Bot")

with st.sidebar:
    st.header("I am sidebar")
    add_radio = st.radio(
        "Choose a method",
        ("Ask a query", "Leave planner","Chat with LLM")
    )
    if add_radio == "Ask a query":
        up_llm = "Ask a query"
    elif add_radio == "Leave planner":
        up_llm = "Leave planner"
    else:
        up_llm = "Chat with LLM"

ask_query(up_llm)
