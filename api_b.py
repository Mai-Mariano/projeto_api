from flask import Flask, jsonify

app = Flask(__name__)

# Simula dados de temperatura por cidade
weather_data = {
    "SãoPaulo": 25,
    "RioDeJaneiro": 33,
    "Curitiba": 14,
    "PortoAlegre": 18
}

@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    city_key = city.replace(" ", "")
    temp = weather_data.get(city_key)

    if temp is None:
        return jsonify({"error": "Cidade não encontrada"}), 404

    return jsonify({
        "city": city.replace("_", " "),
        "temp": temp,
        "unit": "Celsius"
    })

if __name__ == '__main__':
    app.run(port=5001, debug=True)