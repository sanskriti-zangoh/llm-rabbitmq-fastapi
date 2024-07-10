#!/bin/sh

# Start the Ollama server
ollama serve &

# Wait for the server to start
sleep 10

# Pull the llama3 model
ollama pull llama3

# Keep the container running
tail -f /dev/null