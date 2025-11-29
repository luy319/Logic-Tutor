import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="Logical Reasoning Tutor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for user progress
def initialize_session_state():
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'quiz_progress' not in st.session_state:
        st.session_state.quiz_progress = {"beginner": 0, "intermediate": 0, "advanced": 0}
    if 'game_progress' not in st.session_state:
        st.session_state.game_progress = {"truth_table": 0, "puzzle": 0, "matching": 0}
    if 'current_quiz' not in st.session_state:
        st.session_state.current_quiz = {}
    if 'game_state' not in st.session_state:
        st.session_state.game_state = {}
    if 'error_tracking' not in st.session_state:
        st.session_state.error_tracking = {}
    if 'learning_path' not in st.session_state:
        st.session_state.learning_path = {
            "propositional_basics": False,
            "connectives": False,
            "truth_tables": False,
            "conditionals": False,
            "converse_inverse": False
        }

# ---------- LEARN SECTION ----------

def show_learn_section():
    st.header("Learn Propositional Logic")
    chapter = st.selectbox(
        "Choose a chapter to learn:",
        [
            "Basic Concepts & Definitions",
            "Logical Connectives",
            "Truth Tables",
            "Conditional Statements",
            "Converse, Inverse & Contrapositive",
            "Logical Equivalences"
        ]
    )

    if chapter == "Basic Concepts & Definitions":
        show_basic_concepts()
    elif chapter == "Logical Connectives":
        show_logical_connectives()
    elif chapter == "Truth Tables":
        show_truth_tables_learning()
        st.session_state.learning_path["truth_tables"] = True
    elif chapter == "Conditional Statements":
        show_conditionals()
        st.session_state.learning_path["conditionals"] = True
    elif chapter == "Converse, Inverse & Contrapositive":
        show_converse_inverse_contrapositive()
        st.session_state.learning_path["converse_inverse"] = True
    elif chapter == "Logical Equivalences":
        show_logical_equivalences()

def show_basic_concepts():
    st.subheader("Basic Concepts of Propositional Logic")
    st.markdown("""
    ### What is Propositional Logic?
    Propositional logic is the branch of logic that studies ways of joining and/or modifying 
    entire propositions, statements, or sentences to form more complicated propositions, 
    statements, or sentences.

    ### Key Definitions:

    **Proposition**: A declarative statement that is either true or false, but not both.

    **Atomic Proposition**: A simple statement that cannot be broken down into smaller statements.

    **Compound Proposition**: Formed by combining atomic propositions using logical connectives.

    **Truth Value**: The truth (T) or falsity (F) of a proposition.

    **Logical Connective**: Symbols used to combine or modify propositions (AND, OR, NOT, etc.)
    """)

    st.markdown("### Identify Propositions")
    st.markdown("Determine which of the following are valid propositions:")

    examples = [
        ("Paris is the capital of France", True, "This is a declarative statement with a clear truth value (True)"),
        ("What time is it?", False, "This is a question, not a declarative statement"),
        ("x + 5 = 10", False, "This depends on the value of x, so it's not a specific proposition"),
        ("This statement is false", False, "This creates a paradox and cannot have a consistent truth value"),
        ("Water boils at 100°C at sea level", True, "This is a factual declarative statement")
    ]

    for i, (example, is_proposition, explanation) in enumerate(examples):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{i+1}. {example}**")
        with col2:
            user_answer = st.selectbox(
                f"Is this a proposition?",
                ["Select", "Yes", "No"],
                key=f"prop_{i}"
            )
        with col3:
            if user_answer != "Select":
                if (user_answer == "Yes" and is_proposition) or (user_answer == "No" and not is_proposition):
                    st.success("✓ Correct")
                    if f"prop_correct_{i}" not in st.session_state:
                        st.session_state.score += 2
                        st.session_state[f"prop_correct_{i}"] = True
                        st.session_state.learning_path["propositional_basics"] = True
                else:
                    st.error("✗ Incorrect")
                    st.info(f"**Explanation:** {explanation}")

def show_logical_connectives():
    st.subheader("Logical Connectives")
    connective = st.selectbox(
        "Choose a logical connective to learn:",
        ["AND (Conjunction ∧)", "OR (Disjunction ∨)", "NOT (Negation ¬)",
         "IMPLIES (Conditional →)", "IF AND ONLY IF (Biconditional ↔)", "XOR (Exclusive OR ⊕)"]
    )

    if "AND" in connective:
        show_and_connective()
    elif "OR" in connective and "XOR" not in connective:
        show_or_connective()
    elif "NOT" in connective:
        show_not_connective()
    elif "IMPLIES" in connective:
        show_implies_connective()
    elif "IF AND ONLY IF" in connective:
        show_iff_connective()
    elif "XOR" in connective:
        show_xor_connective()

    st.session_state.learning_path["connectives"] = True

def show_and_connective():
    st.markdown("""
    ### AND Connective (Conjunction) - Symbol: ∧
    """)
    and_table = pd.DataFrame({
        'p': [True, True, False, False],
        'q': [True, False, True, False],
        'p ∧ q': [True, False, False, False]
    })
    st.dataframe(and_table, hide_index=True)

    st.markdown("### Practice Exercise")
    practice_cases = [
        ("TRUE ∧ TRUE", True),
        ("TRUE ∧ FALSE", False),
        ("FALSE ∧ TRUE", False),
        ("FALSE ∧ FALSE", False)
    ]
    for expr, answer in practice_cases:
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.write(f"**{expr}**")
        with col2:
            user_ans = st.selectbox(
                f"Result for {expr}:",
                ["Select", "TRUE", "FALSE"],
                key=f"and_prac_{expr}"
            )
        with col3:
            if user_ans != "Select":
                correct = "TRUE" if answer else "FALSE"
                if user_ans == correct:
                    st.success("✓")
                else:
                    st.error(f"✗ Should be {correct}")

def show_or_connective():
    st.markdown("""
    ### OR Connective (Disjunction) - Symbol: ∨
    """)
    or_table = pd.DataFrame({
        'p': [True, True, False, False],
        'q': [True, False, True, False],
        'p ∨ q': [True, True, True, False]
    })
    st.dataframe(or_table, hide_index=True)

def show_not_connective():
    st.markdown("""
    ### NOT Connective (Negation) - Symbol: ¬
    """)
    not_table = pd.DataFrame({
        'p': [True, False],
        '¬p': [False, True]
    })
    st.dataframe(not_table, hide_index=True)

def show_implies_connective():
    st.markdown("""
    ### IMPLIES Connective (Conditional) - Symbol: →
    """)
    implies_table = pd.DataFrame({
        'p': [True, True, False, False],
        'q': [True, False, True, False],
        'p → q': [True, False, True, True]
    })
    st.dataframe(implies_table, hide_index=True)

def show_iff_connective():
    st.markdown("""
    ### IF AND ONLY IF Connective (Biconditional) - Symbol: ↔
    """)
    iff_table = pd.DataFrame({
        'p': [True, True, False, False],
        'q': [True, False, True, False],
        'p ↔ q': [True, False, False, True]
    })
    st.dataframe(iff_table, hide_index=True)

def show_xor_connective():
    st.markdown("""
    ### XOR Connective (Exclusive OR) - Symbol: ⊕
    """)
    xor_table = pd.DataFrame({
        'p': [True, True, False, False],
        'q': [True, False, True, False],
        'p ⊕ q': [False, True, True, False]
    })
    st.dataframe(xor_table, hide_index=True)

def show_truth_tables_learning():
    st.subheader("Understanding Truth Tables")
    st.markdown("### Interactive Truth Table Builder")
    num_vars = st.slider("Number of variables:", 1, 3, 2)
    variables = ['p', 'q', 'r'][:num_vars]

    combinations = []
    for i in range(2 ** num_vars):
        combo = []
        for j in range(num_vars):
            combo.append(bool((i >> (num_vars - 1 - j)) & 1))
        combinations.append(combo)

    table_data = []
    for combo in combinations:
        row = {}
        for i, var in enumerate(variables):
            row[var] = combo[i]
        table_data.append(row)

    df = pd.DataFrame(table_data)
    st.dataframe(df, hide_index=True)

def show_conditionals():
    st.subheader("Conditional Statements")
    st.markdown("### Practice: Translate Conditionals")

    translations = [
        {
            "expression": "You can drive if you have a license",
            "logical_form": "have_license → can_drive",
            "explanation": "'q if p' translates to p → q"
        },
        {
            "expression": "A number is prime only if it is greater than 1",
            "logical_form": "is_prime → greater_than_1",
            "explanation": "'p only if q' translates to p → q"
        },
        {
            "expression": "Studying hard is sufficient for passing the exam",
            "logical_form": "study_hard → pass_exam",
            "explanation": "'p is sufficient for q' translates to p → q"
        }
    ]

    for i, trans in enumerate(translations):
        st.markdown(f"**{i+1}. Natural Language:** {trans['expression']}")
        user_translation = st.text_input(
            f"Logical form for example {i+1}:",
            key=f"trans_{i}",
            placeholder="p → q format"
        )
        if user_translation:
            if user_translation.strip().lower() == trans['logical_form'].lower():
                st.success("✓ Correct translation!")
            else:
                st.error(f"Not quite. The logical form is: **{trans['logical_form']}**")
                st.info(f"**Explanation:** {trans['explanation']}")

def show_converse_inverse_contrapositive():
    st.subheader("Converse, Inverse, and Contrapositive")
    st.markdown("### Related Conditionals")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**Original**\np → q")
    with col2:
        st.markdown("**Converse**\nq → p")
    with col3:
        st.markdown("**Inverse**\n¬p → ¬q")
    with col4:
        st.markdown("**Contrapositive**\n¬q → ¬p")

def show_logical_equivalences():
    st.subheader("Logical Equivalences")
    st.markdown("### Important Logical Equivalences")

    equivalences = [
        ("Double Negation", "¬¬p ≡ p"),
        ("Identity Laws", "p ∧ T ≡ p\np ∨ F ≡ p"),
        ("Domination Laws", "p ∨ T ≡ T\np ∧ F ≡ F"),
        ("Idempotent Laws", "p ∨ p ≡ p\np ∧ p ≡ p"),
        ("Commutative Laws", "p ∨ q ≡ q ∨ p\np ∧ q ≡ q ∧ p"),
        ("Associative Laws", "(p ∨ q) ∨ r ≡ p ∨ (q ∨ r)\n(p ∧ q) ∧ r ≡ p ∧ (q ∧ r)"),
        ("Distributive Laws", "p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r)\np ∧ (q ∨ r) ≡ (p ∧ q) ∧ (p ∧ r)"),
        ("De Morgan's Laws", "¬(p ∧ q) ≡ ¬p ∨ ¬q\n¬(p ∨ q) ≡ ¬p ∧ ¬q"),
        ("Absorption Laws", "p ∨ (p ∧ q) ≡ p\np ∧ (p ∨ q) ≡ p"),
        ("Conditional Equivalences", "p → q ≡ ¬p ∨ q\np → q ≡ ¬q → ¬p"),
        ("Biconditional Equivalences", "p ↔ q ≡ (p → q) ∧ (q → p)\np ↔ q ≡ ¬p ↔ ¬q")
    ]

    for name, laws in equivalences:
        with st.expander(f"**{name}**"):
            st.code(laws)

    st.markdown("### Practice: Apply Logical Equivalences")

    practice_problems = [
        {
            "problem": "Simplify: ¬(p ∧ ¬q)",
            "steps": [
                "Apply De Morgan's Law: ¬(p ∧ ¬q) ≡ ¬p ∨ ¬¬q",
                "Apply Double Negation: ¬p ∨ ¬¬q ≡ ¬p ∨ q"
            ],
            "answer": "¬p ∨ q"
        },
        {
            "problem": "Rewrite p → q using only OR and NOT",
            "steps": [
                "Conditional equivalence: p → q ≡ ¬p ∨ q"
            ],
            "answer": "¬p ∨ q"
        }
    ]

    for i, prob in enumerate(practice_problems):
        st.markdown(f"**Problem {i+1}:** {prob['problem']}")
        user_solution = st.text_input("Your solution:", key=f"equiv_{i}")
        if user_solution:
            if user_solution.strip().replace(" ", "") == prob['answer'].replace(" ", ""):
                st.success("✓ Correct!")
            else:
                st.error("Not quite. Let's work through it:")
                for step in prob['steps']:
                    st.write(f"- {step}")
                st.info(f"**Final answer:** {prob['answer']}")

# ---------- QUIZZES ----------

def show_quizzes():
    st.header("Practice Quizzes")
    st.markdown(f"### Current Score: {st.session_state.score}")
    quiz_level = st.radio(
        "Select Quiz Level:",
        ["Beginner", "Intermediate", "Advanced"],
        horizontal=True
    )

    if quiz_level == "Beginner":
        run_beginner_quiz()
    elif quiz_level == "Intermediate":
        run_intermediate_quiz()
    else:
        run_advanced_quiz()

def run_beginner_quiz():
    st.subheader("Beginner Level Quiz")
    questions = [
        {
            "question": "What is the result of TRUE AND FALSE?",
            "options": ["TRUE", "FALSE", "Cannot determine", "Both TRUE and FALSE"],
            "correct": 1,
            "hint": "AND is only true when both operands are true.",
            "explanation": "The AND connective requires both propositions to be true for the result to be true. Since FALSE is one operand, the result is FALSE.",
            "points": 10,
            "error_feedback": {
                "TRUE": "Remember: AND requires BOTH to be true",
                "Cannot determine": "With specific truth values, we can always determine the result",
                "Both TRUE and FALSE": "A proposition cannot be both true and false simultaneously"
            }
        },
        {
            "question": "Which connective represents logical OR?",
            "options": ["∧", "∨", "¬", "→"],
            "correct": 1,
            "hint": "OR is represented by the ∨ symbol.",
            "explanation": "∨ is the symbol for logical OR (disjunction). ∧ is AND, ¬ is NOT, and → is IMPLIES.",
            "points": 10,
            "error_feedback": {
                "∧": "That's the symbol for AND, not OR",
                "¬": "That's the symbol for NOT (negation)",
                "→": "That's the symbol for IMPLIES (conditional)"
            }
        }
    ]
    display_enhanced_quiz(questions, "beginner")

def run_intermediate_quiz():
    st.subheader("Intermediate Level Quiz")
    questions = [
        {
            "question": "If p → q is FALSE, what must be true?",
            "options": ["p is FALSE, q is TRUE", "p is TRUE, q is FALSE", "Both are FALSE", "Both are TRUE"],
            "correct": 1,
            "hint": "IMPLIES is false only in one specific case.",
            "explanation": "The conditional p → q is false ONLY when p is true and q is false. In all other cases, it's true.",
            "points": 20,
            "error_feedback": {
                "p is FALSE, q is TRUE": "When p is false, p → q is true regardless of q",
                "Both are FALSE": "When both are false, p → q is true",
                "Both are TRUE": "When both are true, p → q is true"
            }
        },
        {
            "question": "What is the contrapositive of 'If it rains, then I bring an umbrella'?",
            "options": [
                "If I bring an umbrella, then it rains",
                "If it does not rain, then I do not bring an umbrella",
                "If I do not bring an umbrella, then it does not rain",
                "It rains if and only if I bring an umbrella"
            ],
            "correct": 2,
            "hint": "Contrapositive: negate both parts and reverse them.",
            "explanation": "Original: p → q where p='it rains', q='I bring umbrella'. Contrapositive: ¬q → ¬p = 'If I do not bring an umbrella, then it does not rain'.",
            "points": 25,
            "error_feedback": {
                "If I bring an umbrella, then it rains": "That's the converse, not the contrapositive",
                "If it does not rain, then I do not bring an umbrella": "That's the inverse, not the contrapositive",
                "It rains if and only if I bring an umbrella": "That's the biconditional, not the contrapositive"
            }
        }
    ]
    display_enhanced_quiz(questions, "intermediate")

def run_advanced_quiz():
    st.subheader("Advanced Level Quiz")
    questions = [
        {
            "question": "Which expression is logically equivalent to ¬(p ∨ q)?",
            "options": ["¬p ∧ ¬q", "¬p ∨ ¬q", "p ∧ q", "p ∨ q"],
            "correct": 0,
            "hint": "This is one of De Morgan's Laws.",
            "explanation": "De Morgan's Law states that ¬(p ∨ q) ≡ ¬p ∧ ¬q. The negation distributes and flips OR to AND.",
            "points": 30,
            "error_feedback": {
                "¬p ∨ ¬q": "That would be equivalent to ¬(p ∧ q) by De Morgan's Law",
                "p ∧ q": "That's the opposite of what we want",
                "p ∨ q": "That's the original expression without negation"
            }
        },
        {
            "question": "If 'All humans are mortal' is true, which of these must also be true?",
            "options": [
                "All mortals are humans",
                "If something is not mortal, then it is not human",
                "If something is human, then it is not mortal",
                "Some humans are not mortal"
            ],
            "correct": 1,
            "hint": "Think about the contrapositive.",
            "explanation": "Let p='is human', q='is mortal'. Original: p → q. The contrapositive ¬q → ¬p must also be true: 'If something is not mortal, then it is not human'.",
            "points": 35,
            "error_feedback": {
                "All mortals are humans": "That's the converse, which may not be true",
                "If something is human, then it is not mortal": "That contradicts the original statement",
                "Some humans are not mortal": "That also contradicts the original statement"
            }
        }
    ]
    display_enhanced_quiz(questions, "advanced")

def display_enhanced_quiz(questions, level):
    st.markdown(f"**Progress: {st.session_state.quiz_progress[level]}/{len(questions)} questions completed**")
    for i, q in enumerate(questions):
        st.markdown("---")
        st.markdown(f"**Question {i+1}:** {q['question']}")
        st.markdown(f"*Points: {q['points']}*")

        hint_key = f"hint_{level}_{i}"
        if hint_key not in st.session_state:
            st.session_state[hint_key] = False

        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("💡 Hint", key=f"hint_btn_{level}_{i}"):
                st.session_state[hint_key] = True

        if st.session_state[hint_key]:
            st.info(f"**Hint:** {q['hint']}")

        user_answer = st.radio(
            "Select your answer:",
            q['options'],
            key=f"quiz_{level}_{i}"
        )

        if st.button(f"Check Answer {i+1}", key=f"check_btn_{level}_{i}"):
            if user_answer == q['options'][q['correct']]:
                st.success(f"✅ Correct! +{q['points']} points")
                st.session_state.score += q['points']
                st.session_state.quiz_progress[level] += 1

                if level == "beginner" and i == 0:
                    st.session_state.learning_path["propositional_basics"] = True
                elif level == "intermediate" and i == 1:
                    st.session_state.learning_path["converse_inverse"] = True
            else:
                st.error("❌ Incorrect.")
                if 'error_feedback' in q and user_answer in q['error_feedback']:
                    st.warning(f"**Common misunderstanding:** {q['error_feedback'][user_answer]}")

                error_key = f"error_{level}_{q['question'][:20]}"
                if error_key in st.session_state.error_tracking:
                    st.session_state.error_tracking[error_key] += 1
                else:
                    st.session_state.error_tracking[error_key] = 1

            with st.expander("View Detailed Explanation"):
                st.markdown(f"**Question:** {q['question']}")
                st.markdown(f"**Correct Answer:** {q['options'][q['correct']]}")
                st.markdown(f"**Explanation:** {q['explanation']}")
                if user_answer != q['options'][q['correct']]:
                    error_count = st.session_state.error_tracking.get(
                        f"error_{level}_{q['question'][:20]}", 0
                    )
                    if error_count > 1:
                        st.warning(
                            f"🤔 You've made this error {error_count} times. "
                            "Consider reviewing the related learning materials."
                        )

# ---------- GAMES ----------

def truth_table_game():
    st.subheader("Truth Table Challenge")
    st.markdown("Fill in the missing outputs for the given logical expression.")
    expressions = [
        {"expr": "p ∧ q", "func": lambda p, q: p and q},
        {"expr": "p ∨ q", "func": lambda p, q: p or q},
        {"expr": "p → q", "func": lambda p, q: (not p) or q},
    ]
    if "truth_table_state" not in st.session_state:
        st.session_state.truth_table_state = {"current": 0, "score": 0}

    state = st.session_state.truth_table_state
    current = expressions[state["current"]]
    st.markdown(f"### Expression: **{current['expr']}**")

    rows = [(True, True), (True, False), (False, True), (False, False)]
    correct_outputs = [current["func"](p, q) for p, q in rows]

    user_outputs = []
    for idx, (p, q) in enumerate(rows):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"p = {p}, q = {q}")
        with col2:
            ans = st.selectbox(
                f"Result row {idx+1}",
                ["Select", "True", "False"],
                key=f"tt_ans_{state['current']}_{idx}"
            )
        user_outputs.append(ans)

    if st.button("✅ Check Truth Table"):
        all_correct = True
        for idx, ans in enumerate(user_outputs):
            expected = "True" if correct_outputs[idx] else "False"
            if ans == expected:
                st.success(f"Row {idx+1}: Correct")
            else:
                all_correct = False
                st.error(f"Row {idx+1}: Should be {expected}")

        if all_correct:
            st.success("All rows correct! +20 points")
            st.session_state.score += 20
            state["score"] += 20
            st.session_state.game_progress["truth_table"] += 1
            st.session_state.learning_path["truth_tables"] = True
            state["current"] = (state["current"] + 1) % len(expressions)

    st.markdown(f"Game score (truth tables): {state['score']}")

def logic_puzzle_game():
    st.subheader("Logic Puzzle")
    st.markdown("Solve a small reasoning puzzle about propositions.")
    if "puzzle_done" not in st.session_state:
        st.session_state.puzzle_done = False

    st.markdown(
        "Suppose the statement 'If it is Sunday, then I rest' is true. "
        "Today I am not resting. What can be concluded?"
    )
    options = [
        "It is Sunday",
        "It is not Sunday",
        "I always rest",
        "Nothing can be concluded"
    ]
    ans = st.radio("Choose the best conclusion:", options, key="puzzle_ans")
    if st.button("Check Puzzle Answer"):
        if ans == "It is not Sunday":
            st.success("Correct! This is the contrapositive reasoning. +10 points")
            st.session_state.score += 10
            st.session_state.game_progress["puzzle"] += 1
            st.session_state.puzzle_done = True
        else:
            st.error("Not quite. Think about the contrapositive: if not q, then not p.")

def connective_match_game():
    st.subheader("Connective Match")
    st.markdown("Match natural language sentences to the correct connective.")
    if "match_score" not in st.session_state:
        st.session_state.match_score = 0

    items = [
        ("I will go to the party only if I finish my work", "→"),
        ("I will have coffee or tea (or both)", "∨"),
        ("I will not go outside", "¬"),
    ]
    score_gain = 0
    for idx, (text, symbol) in enumerate(items):
        st.markdown(f"**{idx+1}.** {text}")
        choice = st.selectbox(
            "Choose connective:",
            ["Select", "∧", "∨", "¬", "→", "↔"],
            key=f"match_{idx}"
        )
        if st.button(f"Check {idx+1}", key=f"btn_match_{idx}"):
            if choice == symbol:
                st.success("Correct! +5 points")
                score_gain += 5
            else:
                st.error(f"Incorrect. The right symbol is {symbol}")

    if score_gain > 0:
        st.session_state.score += score_gain
        st.session_state.match_score += score_gain
        st.session_state.game_progress["matching"] += 1

    st.markdown(f"Connective match game score: {st.session_state.match_score}")

def conditional_transformation_game():
    st.subheader("Conditional Transformation Game")
    st.markdown("Transform the given conditional into its converse, inverse, or contrapositive!")
    transformations = [
        {
            "original": "If a number is even, then it is divisible by 2",
            "type": "contrapositive",
            "target": "If a number is not divisible by 2, then it is not even",
            "hint": "Negate both parts and reverse them"
        },
        {
            "original": "If it is summer, then it is hot",
            "type": "converse",
            "target": "If it is hot, then it is summer",
            "hint": "Simply reverse the order without negating"
        },
        {
            "original": "If you study, then you will pass",
            "type": "inverse",
            "target": "If you do not study, then you will not pass",
            "hint": "Negate both parts but keep the same order"
        }
    ]

    if 'transform_game' not in st.session_state:
        st.session_state.transform_game = {
            'current_round': 0,
            'score': 0,
            'hints_used': 0
        }

    state = st.session_state.transform_game

    if state['current_round'] < len(transformations):
        current = transformations[state['current_round']]
        st.markdown(f"### Round {state['current_round'] + 1}")
        st.markdown(f"**Original:** {current['original']}")
        st.markdown(f"**Transform to:** {current['type'].title()}")
        user_answer = st.text_area("Your answer:", key=f"transform_{state['current_round']}")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💡 Get Hint"):
                st.info(f"**Hint:** {current['hint']}")
                state['hints_used'] += 1
        with col2:
            if st.button("✅ Check Answer"):
                if user_answer.strip().lower() == current['target'].lower():
                    st.success("Correct! +15 points")
                    state['score'] += 15
                    st.session_state.score += 15
                    state['current_round'] += 1
                    st.session_state.learning_path["converse_inverse"] = True
                    st.session_state.game_progress["puzzle"] += 1
                else:
                    st.error("Not quite right. Try again!")
                    st.info(f"**Expected:** {current['target']}")
        with col3:
            if st.button("⏭️ Skip"):
                state['current_round'] += 1
                st.rerun()
    else:
        st.success(f"Game Complete! Final Score: {state['score']}")
        st.markdown(f"Hints used: {state['hints_used']}")
        if st.button("🔄 Play Again"):
            st.session_state.transform_game = {
                'current_round': 0,
                'score': 0,
                'hints_used': 0
            }
            st.rerun()

def show_games():
    st.header("Logic Games & Exercises")
    st.markdown(f"### Current Game Score: {st.session_state.score}")
    game_choice = st.selectbox(
        "Choose a game:",
        ["Truth Table Challenge", "Logic Puzzle", "Connective Match", "Conditional Transformation"]
    )

    if game_choice == "Truth Table Challenge":
        truth_table_game()
    elif game_choice == "Logic Puzzle":
        logic_puzzle_game()
    elif game_choice == "Connective Match":
        connective_match_game()
    else:
        conditional_transformation_game()

# ---------- PROGRESS DASHBOARD ----------

def show_progress():
    st.header("Learning Progress Dashboard")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Score", st.session_state.score)
    with col2:
        quiz_completion = sum(st.session_state.quiz_progress.values()) / 15 * 100
        st.metric("Quiz Completion", f"{quiz_completion:.1f}%")
    with col3:
        game_completion = sum(st.session_state.game_progress.values()) / 9 * 100
        st.metric("Game Completion", f"{game_completion:.1f}%")

    st.subheader("Learning Path Progress")
    learning_objectives = [
        ("Basic Concepts & Definitions", "propositional_basics"),
        ("Logical Connectives", "connectives"),
        ("Truth Tables", "truth_tables"),
        ("Conditional Statements", "conditionals"),
        ("Converse, Inverse & Contrapositive", "converse_inverse")
    ]
    for objective, key in learning_objectives:
        status = "✅ Completed" if st.session_state.learning_path[key] else "📚 In Progress"
        st.markdown(f"- {objective}: {status}")

    st.subheader("Common Error Patterns")
    if st.session_state.error_tracking:
        st.markdown("Areas where you've made repeated errors:")
        for error, count in list(st.session_state.error_tracking.items())[:5]:
            if count > 1:
                st.warning(f"❌ {error.replace('error_', '')}: {count} errors")
    else:
        st.info("No repeated errors detected! Keep up the good work!")

    st.subheader("Learning Recommendations")
    recommendations = []
    if not st.session_state.learning_path["converse_inverse"]:
        recommendations.append("Practice converting between conditionals and their related forms")
    if st.session_state.quiz_progress["beginner"] < 3:
        recommendations.append("Complete more beginner quizzes to strengthen fundamentals")
    if not st.session_state.learning_path["truth_tables"]:
        recommendations.append("Work on truth table exercises for better logical intuition")
    if recommendations:
        for rec in recommendations:
            st.markdown(f"📋 {rec}")
    else:
        st.success("🎉 You're making great progress across all areas!")

# ---------- HOME PAGE ----------

def show_home():
    st.header("Welcome to the Logical Reasoning Tutor! 🧠")
    st.markdown("""
    ### Your Comprehensive Guide to Propositional Logic
    """)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🎓 Start Learning", use_container_width=True):
            st.session_state.page = "Learn Propositional Logic"
            st.rerun()
    with col2:
        if st.button("📝 Take Placement Quiz", use_container_width=True):
            st.session_state.page = "Practice Quizzes"
            st.rerun()
    with col3:
        if st.button("🎮 Play Logic Games", use_container_width=True):
            st.session_state.page = "Logic Games & Exercises"
            st.rerun()
    with col4:
        if st.button("📊 View Progress", use_container_width=True):
            st.session_state.page = "Learning Progress Dashboard"
            st.rerun()

    st.markdown("### 📚 Additional Resources")
    resources = [
        ("Stanford Introduction to Logic", "https://online.stanford.edu/courses/soe-y0001-logic-introduction-logic"),
        ("Khan Academy Logic Courses", "https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:logic"),
        ("Internet Encyclopedia of Philosophy - Logic", "https://iep.utm.edu/logic/"),
        ("Wikipedia - Propositional Calculus", "https://en.wikipedia.org/wiki/Propositional_calculus")
    ]
    for name, url in resources:
        st.markdown(f"- [{name}]({url})")

# ---------- MAIN APP ----------

def main():
    initialize_session_state()
    st.title("🧠 Logical Reasoning Tutor")
    st.markdown("---")

    st.sidebar.title("Navigation")
    if 'page' not in st.session_state:
        st.session_state.page = "Home"

    page = st.sidebar.radio(
        "Go to",
        [
            "Home",
            "Learn Propositional Logic",
            "Practice Quizzes",
            "Logic Games & Exercises",
            "Learning Progress Dashboard"
        ],
        key="nav_radio"
    )
    st.session_state.page = page

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### Current Score: {st.session_state.score}")
    st.sidebar.markdown("#### Learning Progress")
    completed = sum(1 for status in st.session_state.learning_path.values() if status)
    total = len(st.session_state.learning_path)
    st.sidebar.progress(completed / total if total else 0)
    st.sidebar.markdown(f"**{completed}/{total} topics mastered**")

    if completed < total:
        next_topic = next(
            (topic for topic, status in st.session_state.learning_path.items() if not status),
            None
        )
        if next_topic:
            st.sidebar.info(f"**Next:** {next_topic.replace('_', ' ').title()}")

    if st.session_state.page == "Home":
        show_home()
    elif st.session_state.page == "Learn Propositional Logic":
        show_learn_section()
    elif st.session_state.page == "Practice Quizzes":
        show_quizzes()
    elif st.session_state.page == "Logic Games & Exercises":
        show_games()
    elif st.session_state.page == "Learning Progress Dashboard":
        show_progress()

    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            "<div style='text-align: center; color: gray;'>"
            "Logical Reasoning Tutor © 2024 | Built with Streamlit | "
            "<a href='#'>Need Help?</a>"
            "</div>",
            unsafe_allow_html=True
        )
    with col2:
        if st.button("🔄 Reset Progress"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()

