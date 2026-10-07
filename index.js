const express = require('express');
const puppeteer = require('puppeteer');

const app = express();
app.use(express.json());

// Endpoint que llamará Google Apps Script
app.get('/consultar-corridas', async (req, res) => {
  try {
    const { origen, destino, fecha, linea } = req.query;

    if (!origen || !destino || !fecha || !linea) {
      return res.status(400).json({ 
        error: 'Faltan parámetros requeridos: origen, destino, fecha y linea.' 
      });
    }

    console.log(`Buscando corridas para: ${linea} | ${origen} -> ${destino} el ${fecha}`);

    // AQUÍ VA TU LÓGICA DE SCRAPING CON PUPPETEER
    // Por ahora enviamos una estructura de prueba compatible:
    const resultadosScraping = [
      { horario: "08:00 AM", precioProveedor: 850.00 },
      { horario: "12:30 PM", precioProveedor: 850.00 },
      { horario: "05:00 PM", precioProveedor: 920.00 }
    ];

    res.json({ corridas: resultadosScraping });

  } catch (error) {
    console.error("Error en el proceso:", error);
    res.status(500).json({ error: "Ocurrió un error al consultar las corridas." });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor activo en el puerto ${PORT}`);
});
