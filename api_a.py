from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_B_URL = "http://localhost:5001/weather/{}"

@app.route('/recommendation/<city>', methods=['GET'])
def get_recommendation(city):
    try:
        response = requests.get(API_B_URL.format(city))
        if response.status_code != 200:
            return jsonify({"error": "Não foi possível obter os dados de clima"}), 404

        data = response.json()
        temp = data['temp']

        if temp > 30:
            recommendation = "Está muito quente! Hidrate-se e use protetor solar."
        elif 15 < temp <= 30:
            recommendation = "O clima está agradável. Aproveite seu dia!"
        else:
            recommendation = "Está frio! Recomenda-se usar um casaco."

        return jsonify({
            "city": data["city"],
            "temp": temp,
            "unit": data["unit"],
            "recommendation": recommendation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)