import dotenv
dotenv.load_dotenv()

import os
import vertexai
from vertexai import agent_engines

PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")
BUCKET = os.getenv("BUCKET")

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=BUCKET,
)

DEPLOYMENT_ID = os.getenv("DEPLOYMENT_ID")
SESSION_ID = os.getenv("SESSION_ID")


remote_app = agent_engines.get(DEPLOYMENT_ID)

# 반드시 실행
remote_app.delete(force=True)

#remote_session = remote_app.create_session(user_id="u_123")

#print(remote_session['id'])

# for event in remote_app.stream_query(
#     user_id="u_123",
#     session_id=SESSION_ID,
#     message="I'm going to Laos, any tips?",
# ):
#     print(event, "\n", "=" *50)

