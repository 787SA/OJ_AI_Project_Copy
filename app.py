import streamlit as st
from src.witness_logic import WitnessAI
from src.witness_profiles import WITNESS_PROFILES

def main():
    st.title("🎭 O.J. Trial Cross-Examination Simulator")

    # Initialize session state
    if "witness" not in st.session_state:
        st.session_state.witness = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "key_topics_asked" not in st.session_state:
        st.session_state.key_topics_asked = set()
    if "show_clues" not in st.session_state:
        st.session_state.show_clues = False

    # API Key Input
    api_key = st.text_input("Enter your OpenAI API key:", type="password", key="api_key_input")
    
    if not api_key:
        st.warning("🔑 Please enter your OpenAI API key to begin the cross-examination")
        st.stop()

    # Sidebar - Witness Selection
    with st.sidebar:
        st.header("Witness Selection")
        witness_choice = st.selectbox(
            "Choose a witness:",
            ["Kato Kaelin", "Mark Fuhrman", "Nicole Brown Neighbor"]
        )

        # Initialize/update witness (CRITICAL FIX)
        witness_name = witness_choice.replace(" ", "_")
        if st.session_state.witness is None or not hasattr(st.session_state.witness, 'profile') or st.session_state.witness.profile != WITNESS_PROFILES[witness_name]:
            try:
                st.session_state.witness = WitnessAI(witness_name, api_key)
                st.session_state.messages = []
                st.session_state.key_topics_asked = set()
                st.session_state.show_clues = False
                st.rerun()
            except Exception as e:
                st.error(f"Failed to initialize witness: {str(e)}")
                return

        # Toggle clues button
        if st.button("💡 Toggle Clues"):
            st.session_state.show_clues = not st.session_state.show_clues

        # End session button
        if st.button("⏹️ End Session"):
            if st.session_state.witness:
                grade_results = st.session_state.witness.calculate_grade(st.session_state.key_topics_asked)
                with st.container():
                    st.write("## Cross-Examination Results")
                    st.write(f"**Score:** {grade_results['score']}%")
                    for item in grade_results['feedback']:
                        st.write(f"- {item}")
            else:
                st.warning("No active session to grade")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg["role"] == "assistant" and "clue" in msg and msg["clue"] and st.session_state.show_clues:
                st.caption(f"🧠 Strategic Insight: {msg['clue']}")

    # User input
    if prompt := st.chat_input("Ask your question..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        try:
            # Generate response from AI
            response, topic, clue = st.session_state.witness.generate_response(prompt)
            
            # Track topics for grading
            if topic:
                st.session_state.key_topics_asked.add(topic)
            
            # Add AI response to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "clue": clue
            })
            
            st.rerun()
        
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")

if __name__ == "__main__":
    main()
