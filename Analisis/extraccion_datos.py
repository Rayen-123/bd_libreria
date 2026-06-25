import schedule
import time
from etl_libreria import ejecutar_etl # Tu función que hace los SELECT e INSERT

def job():
    print("Ejecutando ETL programado...")
    ejecutar_etl()

# Programamos la extracción para las 3:00 todos los días
schedule.every().day.at("3:00").do(job)

# Bucle infinito para mantener el programa vivo
while True:
    schedule.run_pending()
    time.sleep(1)