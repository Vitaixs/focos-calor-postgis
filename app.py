from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, text

app = Flask(__name__)

engine = create_engine("postgresql://postgres:123@localhost:5432/focosdb")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contar", methods=["POST"])
def contar():
    dados = request.json
    coordenadas = dados["coordinates"]

    coords_text = ", ".join([f"{lon} {lat}" for lon, lat in coordenadas])
    coords_text += f", {coordenadas[0][0]} {coordenadas[0][1]}"

    wkt = f"POLYGON(({coords_text}))"

    query = text(f"""
        SELECT COUNT(*)
        FROM focos
        WHERE ST_Contains(
            ST_GeomFromText(:wkt, 4326),
            geom
        );
    """)

    with engine.connect() as conn:
        resultado = conn.execute(query, {"wkt": wkt}).scalar()

    return jsonify({"quantidade": resultado})

if __name__ == "__main__":
    app.run(debug=True)
