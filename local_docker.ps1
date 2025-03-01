docker build --rm -t "local-disaster-assistant" .
docker run -e OPENAI_API_KEY=$env:OPENAI_API_KEY -p 80:80 local-disaster-assistant