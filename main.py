from fastapi import FastAPI, Query
import requests
import pandas as pd
from io import StringIO

app = FastAPI(title="API Sindicatos CFCRL")

CSV_URL = "https://repodatos.atdt.gob.mx/api_update/cfcrl/resoluciones_positivas_tramites_registrales/05_resoluciones_positivas_cgra_2024-2025.csv"

def obtener_datos():
    respuesta = requests.get(CSV_URL, timeout=10)
    respuesta.encoding = "utf-8"
    return pd.read_csv(StringIO(respuesta.text))

@app.get("/")
def inicio():
    return {"mensaje": "API Sindicatos funcionando ✅"}

@app.get("/sindicatos")
def todos():
    df = obtener_datos()
    return {"total": len(df), "datos": df.fillna("").to_dict(orient="records")}

@app.get("/sindicatos/altas")
def altas():
    df = obtener_datos()
    resultado = df[df["tramite"] == "Registro de asociaciones"]
    return {"total": int(resultado["total"].sum()), "datos": resultado.fillna("").to_dict(orient="records")}

@app.get("/sindicatos/federaciones")
def federaciones():
    df = obtener_datos()
    resultado = df[df["tramite"] == "Registro de Federacion y Confed"]
    return {"total": int(resultado["total"].sum()), "datos": resultado.fillna("").to_dict(orient="records")}

@app.get("/sindicatos/modificaciones")
def modificaciones():
    df = obtener_datos()
    resultado = df[df["tramite"].str.contains("Modificacion", na=False)]
    return {"total": int(resultado["total"].sum()), "datos": resultado.fillna("").to_dict(orient="records")}

@app.get("/sindicatos/tramites")
def tramites():
    df = obtener_datos()
    return {"tramites_disponibles": df["tramite"].unique().tolist()}