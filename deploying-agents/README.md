curl -N -X POST "http://127.0.0.1:8000/conversations/{conversation_id}/message-stream" \
-H "Content-Type: application/json" \
-d '{"question":"What is the size of the great wall of china?"}'

curl -N -X POST "http://127.0.0.1:8000/conversations/{conversation_id}/message-stream-all" \
-H "Content-Type: application/json" \
-d '{"question":"한국의 수도는 어디고 인천은 어디에 있어"}'

# Deploy

railway login
railway init
railway up
