# Trading Integrated API

## Dependencias
- python 3.11.9
- MetaTrader5
- pandas==2.2.2
- numpy==1.26.4
- plyer==2.1.0
- uvicorn[standard]==0.29.0
- fastapi==0.110.0
- requests
- python-dotenv

## Inicializar
- crear entorno virtual
- python -m venv .venv
- pip install -r requirements.txt

## Tests
- abrir metatrader e iniciar sesion
- ejecutar todos los .py en carpeta tests para verificar que funcione la conexion
- python -m tests.test_data ...

## Notificacion
- crear bot en telegram (instrucciones en la web)
- guardar TOKEN y chat_id del bot en .env.local

# Servidor
- tener abierto metatrader siempre
- python -m uvicorn main:app --reload
- :8000

## Comparar en TradingView
- abrir pine editor en TV y crear nuevo script con este codigo

//@version=5
indicator("Cruce rsi smas", overlay=true)

// --- SMAs ---
ma9 = ta.sma(close, 20)
ma21 = ta.sma(close, 40)
ma20 = ta.sma(close, 100)
ma40 = ta.sma(close, 200)

// SMAs en grafico
plot(ma9, color=color.new(color.orange, 0), title="SMA 20", linewidth=1)
plot(ma21, color=color.new(color.green, 0), title="SMA 40", linewidth=1)
plot(ma20, color=color.new(color.blue, 0), title="SMA 100", linewidth=1)
plot(ma40, color=color.new(color.purple, 0), title="SMA 200", linewidth=1)

// --- RSI ---
rsiLen = 14
rsiVal = ta.rsi(close, rsiLen)
rsiMA  = ta.sma(rsiVal, 14) // SMA del RSI para el cruce

// logica de cruces para señales
bullishCross = ta.crossover(rsiVal, rsiMA)
bearishCross = ta.crossunder(rsiVal, rsiMA)

// señales de BUY/SELL en las velas
plotshape(bullishCross, title="Señal BUY", style=shape.triangleup, location=location.belowbar, color=color.green, size=size.small, text="BUY")
plotshape(bearishCross, title="Señal SELL", style=shape.triangledown, location=location.abovebar, color=color.red, size=size.small, text="SELL")

- guardar script y agregarlo al grafico
- poner la temporalidad en TV igual que el "Trend" de la UI
- cuando se mande la notificacion, checar si coincide la señal con TV, considerar los 15 minutos de retraso de MT5
