# Add src folder to Python's search path
import sys
sys.path.append('./src')

# Load environment variables FIRST
import os
from dotenv import load_dotenv
load_dotenv()

# Import functions and classes from src folder AFTER loading .env
from ethics_check import validate_question
from witness_logic import WitnessAI

# Allow user to select a witness
print("Available witnesses:")
print("1. Mark Fuhrman")
print("2. Kato Kaelin")
print("3. Nicole Brown's Neighbor")
witness_choice = input("Select a witness by entering their number (1, 2, or 3): ")

if witness_choice == "1":
    witness_name = "Mark_Fuhrman"
elif witness_choice == "2":
    witness_name = "Kato_Kaelin"
elif witness_choice == "3":
    witness_name = "Nicole_Brown_Neighbor"
else:
    print("Invalid choice. Defaulting to Mark Fuhrman.")
    witness_name = "Mark_Fuhrman"

# Initialize the selected witness
witness = WitnessAI(witness_name)

# Allow user to ask a question
user_question = input(f"Enter your question for {witness_name.replace('_', ' ')}: ")
response = witness.generate_response(user_question)
print(f"Witness Response: {response}")

# Test environment variable loading
api_key = os.getenv("OPENAI_API_KEY")
print("Hello UA92 Project!")
print("Your OpenAI key starts with:", api_key[:10] if api_key else "No key found.")
