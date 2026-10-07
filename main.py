import os
import asyncio
from fastapi import FastAPI, Query
from playwright.async_api import async_playwright

app = FastAPI()

@app.get("/")
def home():
    return {"status": "OK", "mensaje": "API de Scraping MK Travels Activa"}

@app.get("/consultar-corridas")
async def consultar_corridas(origen: str, destino: str, fecha: str, linea: str):
    corridas = []
    
    async with async_playwright() as p:
        # Lanza el navegador invisible (Chromium)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            linea_clean = linea.upper().strip()
            
            if "ETN" in linea_clean:
                url = f"https://etn.com.mx/compra?origen={origen}&destino={destino}&fecha={fecha}"
                await page.goto(url, timeout=35000)
                await page.wait_for_selector(".corrida-item", timeout=12000)
                
                elementos = await page.query_selector_all(".corrida-item")
                for elem in elementos:
                    hora = await elem.query_selector(".hora-salida")
                    precio = await elem.query_selector(".precio-base")
                    if hora and precio:
                        h_txt = (await hora.inner_text()).strip()
                        p_txt = (await precio.inner_text()).replace("$", "").replace(",", "").strip()
                        corridas.append({
                            "horario": h_txt,
                            "precioProveedor": float(p_txt)
                        })
                        
            elif "PRIMERA" in linea_clean:
                url = f"https://www.primeraplus.com.mx/viajes?origen={origen}&destino={destino}&fecha={fecha}"
                await page.goto(url, timeout=35000)
                await page.wait_for_selector(".corrida-card", timeout=12000)
                
                elementos = await page.query_selector_all(".corrida-card")
                for elem in elementos:
                    hora = await elem.query_selector(".time")
                    precio = await elem.query_selector(".price")
                    if hora and precio:
                        h_txt = (await hora.inner_text()).strip()
                        p_txt = (await precio.inner_text()).replace("$", "").replace(",", "").strip()
                        corridas.append({
                            "horario": h_txt,
                            "precioProveedor": float(p_txt)
                        })
                        
        except Exception as e:
            print(f"Error durante el scraping de {linea}: {str(e)}")
        finally:
            await browser.close()
            
    return {"linea": linea, "corridas": corridas}
