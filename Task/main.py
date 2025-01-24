from graph import compile_graph
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
from datetime import datetime
import asyncio

date = "2025-01-24"
time = "18:08"
task = "tirar o lixo"

# Função criada para tratar o fluxo de forma assíncrona
async def main_async():
    """
    Função assíncrona principal que valida a data, compila e invoca o grafo de estados
    para executar a tarefa desejada, além de imprimir o resultado no console.

    Retorna:
        Nenhum valor de retorno. As saídas são exibidas no console.
    """
    app = compile_graph()
    print(f"Executando tarefa às {datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%H:%M:%S')}")
    
    # Enviando a mensagem no formato correto
    result = await asyncio.to_thread(
        app.invoke,
        {"message": task}
    )
    
    # Acessando a resposta corretamente
    print(result["message"])

if __name__ == "__main__":
    # VALIDAÇÃO DE DATA E HORA
    hour = time.split(":")[0]
    minute = time.split(":")[1]
    if date < datetime.now().strftime("%Y-%m-%d"):
        print("Não é possível executar a tarefa, a data é anterior à data atual")

    if time < datetime.now().strftime("%H:%M"):
        print("Não é possível executar a tarefa, o horário é anterior ao horário atual")

    # EXECUÇÃO DA TAREFA
    else:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        scheduler = AsyncIOScheduler(timezone=pytz.timezone('America/Sao_Paulo'), 
                                     event_loop=loop)
        scheduler.add_job(
            main_async,
            trigger="cron",
            hour=hour,
            minute=minute,
        )

        print(f"Agendando tarefa para {hour}:{minute}")
        scheduler.start()
        loop.run_forever()