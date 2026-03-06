#!/bin/bash

echo "🚀 Iniciando Consultor RH..."
echo ""

# Start backend
echo "📦 Iniciando backend na porta 3001..."
cd backend
node server.js &
BACKEND_PID=$!

# Wait for backend
sleep 2

echo ""
echo "✅ Sistema iniciado!"
echo ""
echo "📊 Frontend: http://localhost:5173"
echo "🔧 Backend: http://localhost:3001"
echo ""
echo "Pressione Ctrl+C para parar"

# Wait for Ctrl+C
trap "kill $BACKEND_PID; exit" INT
wait
