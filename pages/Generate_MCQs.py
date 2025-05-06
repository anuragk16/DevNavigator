import streamlit as st
import json
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate


def gen_mcq():
    # Initialize LLM
    llm = OllamaLLM(model="llama3.2")

    # Prompt template for single-answer MCQs
    mcq_prompt_template = PromptTemplate.from_template("""
    Generate {num_questions} multiple-choice questions (MCQs) about "{topic}".
    Each question must have only one correct answer.

    Format your response as a valid JSON array:
    [
    {{
        "question": "What is ...?",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "answer": "Correct Option"
    }},
    ...
    ]

    Only return valid JSON. No extra explanation or text.
    """)

    # Page setup
    st.title("🧠 MCQ Quiz App (LLaMA 3.2)")

    # Session storage
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "show_result" not in st.session_state:
        st.session_state.show_result = False

    # Input form
    with st.form("mcq_form"):
        topic = st.text_input("Enter Topic", placeholder="e.g. Machine Learning")
        num_questions = st.radio("Select Number of Questions", [5, 10, 20], horizontal=True)
        generate = st.form_submit_button("🚀 Generate Quiz")

    # Generate quiz
    if generate:
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating MCQs..."):
                try:
                    prompt = mcq_prompt_template.format(topic=topic, num_questions=num_questions)
                    response = llm.invoke(prompt)
                    questions = json.loads(response)

                    st.session_state.questions = questions
                    st.session_state.user_answers = {}
                    st.session_state.show_result = False

                    st.success(f"{len(questions)} MCQs generated for topic: {topic}")
                except Exception as e:
                    st.error(f"Server error : Try Again")

    # Display MCQs
    if st.session_state.questions:
        st.subheader("📋 Your Quiz")
        for i, q in enumerate(st.session_state.questions):
            st.markdown(f"**Q{i+1}. {q['question']}**")
            options_with_placeholder = ["-- Select an Option --"] + q["options"]
            selected_option = st.radio(
                label=f"Question {i+1}",
                options=options_with_placeholder,
                key=f"q{i}",
                label_visibility="collapsed"
            )

            # Save only if user selected a real option
            if selected_option != "-- Select an Option --":
                st.session_state.user_answers[i] = selected_option
            else:
                st.session_state.user_answers[i] = None


        # Submit/check button
        if st.button("✅ Submit & Check"):
            st.session_state.show_result = True

    # Results
    if st.session_state.show_result:
        correct = 0
        total = len(st.session_state.questions)

        st.subheader("📝 Results")
        for i, q in enumerate(st.session_state.questions):
            user_ans = st.session_state.user_answers.get(i)
            correct_ans = q["answer"]
            is_correct = user_ans == correct_ans

            st.markdown(f"**Q{i+1}. {q['question']}**")
            for opt in q["options"]:
                if opt == correct_ans:
                    if opt == user_ans:
                        st.markdown(f"- ✅ **{opt}** (Your Answer, Correct)")
                    else:
                        st.markdown(f"- ✅ **{opt}** (Correct)")
                else:
                    if opt == user_ans:
                        st.markdown(f"- ❌ **{opt}** (Your Answer, Wrong)")
                    else:
                        st.markdown(f"- {opt}")

            st.markdown("---")

            if is_correct:
                correct += 1

        st.success(f"🎉 You got {correct} out of {total} correct!")
        st.info(f"✅ Correct: {correct} | ❌ Wrong: {total - correct}")
