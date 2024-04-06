import re
import streamlit as st
import openai

# Set up OpenAI API key
openai.api_key = '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'

# Function to scan for potential bugs in an app description


def super_sleuth_scanner(app_description):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"Analyze the following app description and provide potential areas in the code where bugs might occur:\n\n{app_description}\n\n",
        max_tokens=150
    )
    potential_bugs = response.choices[0].text.strip()
    return potential_bugs

# Function to generate bug-catching tests based on potential bug areas


def generate_bug_tests(potential_bugs):
    bug_areas = re.findall(r'\d+\. (.*?)\n', potential_bugs)
    return bug_areas

# Function to generate test cases for a specific area of the app using an LLM


def generate_test_cases(area_description, app_description):
    area, description = area_description.split(': ', 1)
    response = openai.Completion.create(
        prompt=f"Generate detailed test cases for the {area.lower()} of an app where: {description} The app is described as: {app_description}",
        engine="gpt-3.5-turbo-instruct",
        max_tokens=150
    )
    test_cases = response.choices[0].text.strip()
    return test_cases

# Function to debug code snippet and problem description


def debug_code(code_snippet, problem_description):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"### Problem Description:\n{problem_description}\n### Code Snippet:\n{code_snippet}\n### Suggestions:",
        temperature=0.5,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["###"]
    )
    return response.choices[0].text.strip()

# Streamlit UI


def main():
    st.title('App Bug Analyzer')

    # Input area for app description
    app_description = st.text_area("Enter app description:", "")

    # Button to trigger analysis
    if st.button('Analyze'):
        if app_description:
            # Analyze app description for potential bugs
            potential_bugs = super_sleuth_scanner(app_description)

            # Generate bug-catching tests
            bug_tests = generate_bug_tests(potential_bugs)

            # Display bug areas
            st.subheader("Potential Bug Areas:")
            for bug_area in bug_tests:
                st.write(bug_area)

            # Input area for app code snippet
            app_code = st.text_area("Enter app code snippet:", "")

            # Submit button to trigger final report generation
            if st.button('Submit'):
                if app_code:
                    st.subheader("Final Report:")

                    # Debug code for the last bug area
                    if bug_tests:
                        last_bug_area = bug_tests[-1]
                        suggestions = debug_code(app_code, last_bug_area)
                        st.write(suggestions)


if __name__ == "__main__":
    main()
