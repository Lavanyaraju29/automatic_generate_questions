import streamlit as st
import cohere

# Initialize Cohere API client
co = cohere.Client("vmLXR4aO7MT5CAS2ZL1EC5PInWzx9ciYReKv90X5")  # Replace with your actual Cohere API key

# Define subjects
subjects = {
    "Mathematics": "mathematics",
    "Science": "science",
    "History": "history",
    "Geography": "geography",
    "Literature": "literature",
    "Microprocessor": "microprocessor",
    "Computer Networks": "computer networks",
    "AI": "artificial intelligence",
    "Data Warehouse": "data warehouse",
    "Business Intelligence": "business intelligence"
}

# Streamlit App Layout
st.title("AI Quiz Generator")
st.write("Select a subject to generate multiple-choice questions.")

# Dropdown menu to select the subject
selected_subject = st.selectbox("Choose a subject", list(subjects.keys()))

# Display start button only after a subject is selected
if selected_subject:
    if st.button("Generate Quiz"):
        with st.spinner("Generating quiz..."):
            try:
                # Define the prompt to send to Cohere API
                prompt = (
                    f"Generate 5 multiple-choice questions on the subject: {subjects[selected_subject]}.\n"
                    "Each question should have:\n"
                    "- A clear question text\n"
                    "- Four options labeled A, B, C, and D\n"
                    "Ensure the output is formatted as follows:\n"
                    "Question: <Question Text>\n"
                    "Options:\n"
                    "A. <Option 1>\n"
                    "B. <Option 2>\n"
                    "C. <Option 3>\n"
                    "D. <Option 4>"
                )

                # Call Cohere API to generate questions
                response = co.generate(
                    model='command-xlarge',
                    prompt=prompt,
                    max_tokens=500,
                    temperature=0.7,
                    k=0,
                    stop_sequences=["--"],
                    return_likelihoods='NONE'
                )

                # Debugging raw response
                raw_text = response.generations[0].text.strip()

                # Clean and split the text into individual questions
                questions = raw_text.split("Question:")[1:]  # Split into questions by "Question:"
                
                if not questions:
                    st.error("No questions were generated. Please try again.")
                else:
                    # Display the questions and their options
                    for i, question_block in enumerate(questions, 1):
                        try:
                            # Extract question text, options
                            lines = question_block.strip().split("\n")
                            question = lines[0].strip()
                            options = [line.strip() for line in lines if line.startswith(("A.", "B.", "C.", "D."))]
                            
                            # Display question and options
                            st.write(f"Question {i}: {question}")
                            for option in options:
                                st.write(option)

                        except Exception as e:
                            st.warning(f"Error processing question {i}: {e}")

            except Exception as e:
                st.error(f"An error occurred: {e}")