import instructor
import openai
import os
from os.path import join, dirname, abspath
from dotenv import load_dotenv


# Load OpenAI API key from dotenv
dotenv_path = join(dirname(dirname(abspath(__file__))), '.env')
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI()
client = instructor.from_openai(client, mode=instructor.Mode.TOOLS)
