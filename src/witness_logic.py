import openai
import random
import re
from src.witness_profiles import WITNESS_PROFILES

class WitnessAI:
    def __init__(self, witness_name, api_key):
        openai.api_key = api_key
        
        if not openai.api_key:
            raise ValueError("OpenAI API key not provided")
        
        if witness_name not in WITNESS_PROFILES:
            raise ValueError(f"Witness '{witness_name}' not found")
        
        self.profile = WITNESS_PROFILES[witness_name]
        self.key_topics = self.profile["key_topics"]
        self.conversation_history = []
        self.used_phrases = []
        self.used_speech_patterns = []

    def generate_response(self, question):
        """Generate a natural, direct response that answers the question while maintaining personality."""
        topic = self._detect_topic(question)
        
        system_prompt = (
            f"You are roleplaying as {self.profile['identity']} during the O.J. Simpson trial cross-examination. "
            f"{self.profile['personality']} \n\n"
            f"FACTUAL KNOWLEDGE: {self.profile['knowledge']} \n\n"
            f"IMPORTANT INSTRUCTIONS:\n"
            f"1. ALWAYS DIRECTLY ANSWER THE SPECIFIC QUESTION ASKED.\n"
            f"2. Keep your personality consistent but vary your speech patterns.\n"
            f"3. For single-letter or gibberish inputs, express confusion naturally but stay in character.\n"
            f"4. Don't volunteer information beyond what was asked.\n"
            f"5. Don't try to steer the conversation toward specific topics.\n"
            f"6. Use your characteristic speech mannerisms naturally and varied.\n"
            f"7. If asked about where you were or what happened, provide specific details from your knowledge.\n"
        )
        
        try:
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": question})
            
            # Build message history
            messages = [{"role": "system", "content": system_prompt}]
            history = self._get_conversation_history(4)
            messages.extend(history)
            
            # Add current question
            messages.append({"role": "user", "content": question})
            
            # Generate response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.85,
                max_tokens=150,
            )
            
            raw_response = response.choices[0].message.content.strip()
            
            # Apply personality traits
            final_response = self._apply_personality(raw_response, len(question.strip()) <= 2)
            
            # Update conversation history
            self.conversation_history.append({"role": "assistant", "content": final_response})
            
            clue = self.profile["clues"].get(topic) if topic else None
            
            return final_response, topic, clue
            
        except Exception as e:
            return f"❌ Error generating response: {str(e)}", None, None

    def _get_conversation_history(self, max_exchanges):
        """Get recent conversation history."""
        if len(self.conversation_history) <= 1:
            return []
        return self.conversation_history[-(max_exchanges*2):-1]

    def _apply_personality(self, response, is_short_input):
        """Apply personality traits and ensure natural variation."""
        if is_short_input:
            confused_responses = [
                f"I'm not sure what you mean by that.",
                f"Could you clarify that question?",
                f"I don't quite understand what you're asking.",
                f"Can you rephrase that, please?",
                f"I'm not certain what you're referring to."
            ]
            return random.choice(confused_responses)
            
        if self.profile["identity"].startswith("Kato"):
            return self._apply_kato_style(response)
        else:
            return response

    def _apply_kato_style(self, response):
        """Apply Kato Kaelin's distinctive speech patterns."""
        fillers = ["like", "you know", "I mean", "I guess", "maybe"]
        qualifiers = ["I think", "probably", "sort of", "kind of"]
        
        # Insert filler at start (50% chance)
        if random.random() < 0.5:
            response = f"{random.choice(fillers)}, {response[0].lower() + response[1:]}"
        
        # Add qualifier at end (40% chance)
        if random.random() < 0.4:
            response += f" {random.choice(qualifiers)}"
            
        return response

    def _detect_topic(self, question):
        """Detects which key topic the question relates to."""
        question_lower = question.lower()
        for topic, keywords in self.key_topics.items():
            if any(keyword in question_lower for keyword in keywords):
                return topic
        return None

    def calculate_grade(self, topics_asked):
        """Calculate grade based on topics covered."""
        total_topics = len(self.key_topics)
        covered_topics = len(topics_asked)
        score = int((covered_topics / total_topics) * 100) if total_topics > 0 else 100
        
        feedback = [
            f"You explored {covered_topics} out of {total_topics} key topic areas.",
            "Topics covered:",
            *[f"- {topic}" for topic in topics_asked],
            "\nTopics missed:",
            *[f"- {topic}" for topic in set(self.key_topics.keys()) - topics_asked]
        ]
        
        return {"score": score, "feedback": feedback}
