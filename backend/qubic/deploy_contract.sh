#!/bin/bash
# deploy_contract.sh
# Simulated contract deployment to Qubic testnet

CONTRACT_FILE=$1

if [ -z "$CONTRACT_FILE" ]; then
    echo "Usage: ./deploy_contract.sh contract.cpp"
    exit 1
fi

echo "🚀 Simulating deployment of $CONTRACT_FILE to Qubic Testnet..."
sleep 1
echo "✅ Contract deployed (simulated)!"
