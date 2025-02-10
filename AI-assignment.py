import streamlit as st
import pandas as pd

# Load quiz data
quiz_data = pd.read_csv('C:\\Users\\induu\\Downloads\\Cleaned_Quiz_Data.csv')

# Initialize session state if not already
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'attempts' not in st.session_state:
    st.session_state.attempts = []

st.title("Quiz Performance & Recommendations")

# Display questions and collect user responses
st.header("Take the Quiz")
user_answers = {}

for index, row in quiz_data.iterrows():
    st.subheader(f"Q{index + 1}: {row['Description']}")
    options = row['Options'].split(', ')
    user_answers[row['Question ID']] = st.radio("Choose your answer:", options, key=f"q{index}")

# Submit button
if st.button("Submit Quiz"):
    score = 0
    total_questions = len(quiz_data)
    incorrect_questions = []

    for index, row in quiz_data.iterrows():
        if user_answers[row['Question ID']] == row['Correct Answer']:
            score += 1
        else:
            incorrect_questions.append(row['Description'])

    accuracy = (score / total_questions) * 100
    
    # Store attempt in session state
    st.session_state.submitted = True
    st.session_state.score = score
    st.session_state.attempts.append(accuracy)

# Display results and recommendations
if st.session_state.submitted:
    st.success(f"You scored {st.session_state.score} out of {len(quiz_data)}.")
    st.info(f"Accuracy: {st.session_state.attempts[-1]:.2f}%")

    if len(st.session_state.attempts) > 1:
        prev_accuracy = st.session_state.attempts[-2]
        improvement = st.session_state.attempts[-1] - prev_accuracy
        if improvement > 0:
            st.success(f"Great job! You've improved by {improvement:.2f}% compared to your last attempt.")
        elif improvement < 0:
            st.warning(f"Your score decreased by {abs(improvement):.2f}%. Review the incorrect questions.")
        else:
            st.info("Your performance remained the same as the last attempt.")

    if incorrect_questions:
        st.subheader("Questions to Review")
        for question in incorrect_questions:
            st.write(f"- {question}")

    st.subheader("Recommendations")
    if accuracy < 50:
        st.write("Focus on understanding the key concepts and reviewing the study material thoroughly.")
    elif accuracy < 80:
        st.write("Good job! But there's room for improvement. Try revisiting the topics you're struggling with.")
    else:
        st.write("Excellent performance! Keep practicing to maintain your high score.")
