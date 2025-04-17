from flask import Flask, jsonify
import requests
import redis
import json

app = Flask(__name__)

# Conectando ao Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

API_B_URL = "http://localhost:5001/weather/{}"
CACHE_TTL = 300  # 5 minutos

@app.route('/recommendation/<city>', methods=['GET'])
def get_recommendation(city):
    city_key = city.replace(" ", "").lower()

    # Verifica se existe cache no Redis
    cached_data = redis_client.get(city_key)
    if cached_data:
        data = json.loads(cached_data)
        print(f"[REDIS] Usando cache para {city_key}")
    else:
        try:
            # Consulta API B
            response = requests.get(API_B_URL.format(city))
            if response.status_code != 200:
                return jsonify({"error": "Não foi possível obter os dados de clima"}), 404
            data = response.json()

            # Salva no Redis com TTL
            redis_client.setex(city_key, CACHE_TTL, json.dumps(data))
            print(f"[API B] Dados salvos no cache Redis para {city_key}")
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    temp = data["temp"]

    if temp > 30:
        recommendation = "Está muito quente! Hidrate-se e use protetor solar."
    elif 15 < temp <= 30:
        recommendation = "O clima está agradável. Aproveite seu dia!"
    else:
        recommendation = "Está frio! Use um casaco."

    return jsonify({
        "city": data["city"],
        "temp": temp,
        "unit": data["unit"],
        "recommendation": recommendation
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
