#!/usr/bin/bash
n=$1

if [ $# -ne 1 ]; then
  echo "Введите одно(!) число"
  exit 1
fi

if [[ ! $1 =~ ^[0-9]+$ ]]; then
  echo "n должен быть числом"
  exit 1
fi

if [ $n -gt 100 ]; then
  echo "n не должен превышать 100!"
  exit 1
fi

response=$(curl -s -X POST -H "Content-Type: application/json" \
-d '{
  "jsonrpc": "2.0",
  "method": "generateIntegers",
  "params": {
    "apiKey": "73118e27-e560-448f-83c2-2703d02bd5f4",
    "n": '"$n"',
    "min": 1,
    "max": 1000000000
  },
  "id": 1
}' https://api.random.org/json-rpc/4/invoke) 


echo $response | jq -r '.result.random.data | join("\n")' || echo "Произошла какая-то внешняя ошибка!"

