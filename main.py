import streamlit as st
import os
# This code still depends on Langflow for other modules and requires googleai
# To remove, please refactor with a different implementation.
from profiles import create_profile, get_notes, get_profile
from form_submit import update_personal_info, add_note, delete_note
from ask_ai_module import ask_ai #This is what is replacing
from ai import get_macros
from dotenv import load_dotenv
load_dotenv()

# Make sure to put you api key in the code
os.environ['GROQ_API_KEY'] = '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'

st.title("Personal Fitness Tool")

@st.fragment()
def personal_data_form():
    with st.form("personal_data"):
        st.header("Personal Data")

        profile = st.session_state.profile

        name = st.text_input("Name", value=profile["general"]["name"])
        age = st.number_input(
            "Age", min_value=1, max_value=120, step=1, value=profile["general"]["age"]
        )
        weight = st.number_input(
            "Weight (kg)",
            min_value=0.0,
            max_value=300.0,
            step=0.1,
            value=float(profile["general"]["weight"]),
        )
        height = st.number_input(
            "Height (cm)",
            min_value=0.0,
            max_value=250.0,
            step=0.1,
            value=float(profile["general"]["height"]),
        )
        genders = ["Male", "Female", "Other"]
        gender = st.radio(
            "Gender", genders, genders.index(profile["general"].get("gender", "Male"))
        )
        activities = (
            "Sedentary",
            "Lightly Active",
            "Moderately Active",
            "Very Active",
            "Super Active",
        )
        activity_level = st.selectbox(
            "Activity Level",
            activities,
            index=activities.index(
                profile["general"].get("activity_level", "Sedentary")
            ),
        )

        personal_data_submit = st.form_submit_button("Save")
        if personal_data_submit:
            if all([name, age, weight, height, gender, activity_level]):
                with st.spinner():
                    st.session_state.profile = update_personal_info(
                        profile,
                        "general",
                        name=name,
                        weight=weight,
                        height=height,
                        gender=gender,
                        age=age,
                        activity_level=activity_level,
                    )
                    st.success("Information saved.")
            else:
                st.warning("Please fill in all of the data!")


@st.fragment()
def goals_form():
    profile = st.session_state.profile
    with st.form("goals_form"):
        st.header("Goals")
        goals = st.multiselect(
            "Select your Goals",
            ["Muscle Gain", "Fat Loss", "Stay Active"],
            default=profile.get("goals", ["Muscle Gain"]),
        )

        goals_submit = st.form_submit_button("Save")
        if goals_submit:
            if goals:
                with st.spinner():
                    st.session_state.profile = update_personal_info(
                        profile, "goals", goals=goals
                    )
                    st.success("Goals updated")
            else:
                st.warning("Please select at least one goal.")


@st.fragment()
def macros():
    profile = st.session_state.profile
    nutrition = st.container(border=True)
    nutrition.header("Macros")
    if nutrition.button("Generate with AI"):
         result = get_macros(profile.get("general"), profile.get("goals"))
         profile["nutrition"] = result
         nutrition.success("AI has generated the results.")

    with nutrition.form("nutrition_form", border=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            calories = st.number_input(
                "Calories",
                min_value=0,
                step=1,
                value=profile["nutrition"].get("calories", 0),
            )
        with col2:
            protein = st.number_input(
                "Protein",
                min_value=0,
                step=1,
                value=profile["nutrition"].get("protein", 0),
            )
        with col3:
            fat = st.number_input(
                "Fat",
                min_value=0,
                step=1,
                value=profile["nutrition"].get("fat", 0),
            )
        with col4:
            carbs = st.number_input(
                "Carbs",
                min_value=0,
                step=1,
                value=profile["nutrition"].get("carbs", 0),
            )

        if st.form_submit_button("Save"):
            with st.spinner():
                st.session_state.profile = update_personal_info(
                    profile,
                    "nutrition",
                    protein=protein,
                    calories=calories,
                    fat=fat,
                    carbs=carbs,
                )
                st.success("Information saved")

@st.fragment()
def notes():
    st.subheader("Notes: ")
    for i, note in enumerate(st.session_state.notes):
        cols = st.columns([5, 1])
        with cols[0]:
            st.text(note.get("text"))
        with cols[1]:
            if st.button("Delete", key=i):
                delete_note(note.get("_id"))
                st.session_state.notes.pop(i)
                st.rerun()
    
    new_note = st.text_input("Add a new note: ")
    if st.button("Add Note"):
        if new_note:
            note = add_note(new_note, st.session_state.profile_id)
            st.session_state.notes.append(note)
            st.rerun()

@st.fragment()
def ask_ai_func():
    st.subheader('Ask AI')
    with st.form("ask_ai_form"):
        user_question = st.text_input("Ask AI a question:")
        ask_ai_button = st.form_submit_button("Ask AI")

        # Check if "Ask AI" button is clicked AND there's a question
        if ask_ai_button and user_question:
            with st.spinner():
                # Combine profile, question, and notes
                combined_input = f"Profile: {st.session_state.profile}\nQuestion: {user_question}\nNotes: {st.session_state.notes}"
                # Use the ask_ai function from ask_ai_module
                fitness_advice = ask_ai(combined_input)
                st.write(fitness_advice)

def forms():
    if "profile" not in st.session_state:
        profile_id = 1
        profile = get_profile(profile_id)
        if not profile:
            profile_id, profile = create_profile(profile_id)

        st.session_state.profile = profile
        st.session_state.profile_id = profile_id

    if "notes" not in st.session_state:
        st.session_state.notes = get_notes(st.session_state.profile_id)

    personal_data_form()
    goals_form()
    macros()
    notes()
    ask_ai_func()


if __name__ == "__main__":
    forms()
