from langchain_core.tools import tool
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from dotenv import load_dotenv
import os
import time

load_dotenv()

API_KEY = os.getenv("PAPER_APCA_API_KEY")
SECRET_KEY = os.getenv("PAPER_APCA_API_SECRET")

# Inicializar clientes
trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)
stock_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

@tool
def get_stock_price(ticker: str) -> str:
    """Busca o preço atual de uma ação usando uma API de mercado financeiro."""
    request_params = StockLatestQuoteRequest(symbol_or_symbols=ticker)

    quote = stock_client.get_stock_latest_quote(request_params)
    preco_atual = quote[ticker].ask_price
    print(f"O preço atual de {ticker} é $ {preco_atual:.2f}")
    return preco_atual

# Função para verificar se o mercado está aberto
def mercado_aberto():
    clock = trading_client.get_clock()
    return clock.is_open

def aguardar_execucao_ordem(order_id, max_tentativas=10):
    """Aguarda a execução da ordem e retorna seu status final"""
    tentativas = 0

    while tentativas < max_tentativas:
        status = trading_client.get_order_by_id(order_id)
        if status.status in ['filled', 'canceled', 'expired', 'rejected']:
            return status
        time.sleep(3)  
        tentativas += 1
    
    return status

@tool
def comprar_acoes(ticker, qty):
    if mercado_aberto():
        ordem_compra = MarketOrderRequest(
            symbol=ticker,
            qty=qty,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY  
        )
        ordem_enviada = trading_client.submit_order(ordem_compra)
        print(f"Ordem de COMPRA enviada! ID: {ordem_enviada.id}")
        status_final = aguardar_execucao_ordem(ordem_enviada.id)
        print(f"Status Final: {status_final.status} | Preço de execução: {status_final.filled_avg_price}")
        return ordem_enviada.id, status_final.filled_avg_price
    else:
        print("Mercado fechado. Não é possível comprar/vender.")
        return "Mercado fechado."

@tool
def vender_acoes(ticker, qty, limit_price):
    if mercado_aberto():
        ordem_venda = LimitOrderRequest(
            symbol=ticker,
            qty=qty,
            side=OrderSide.SELL,
            limit_price=limit_price,
            time_in_force=TimeInForce.GTC  
        )
        ordem_enviada = trading_client.submit_order(ordem_venda)
        print(f"Ordem de VENDA enviada! ID: {ordem_enviada.id}")
        return ordem_enviada
    else:
        print("Mercado fechado. Não é possível comprar/vender.")
        return "Mercado fechado"
    
@tool
def verificar_posicoes():
    posicoes = trading_client.get_all_positions()
    for posicao in posicoes:
        print(f"Ativo: {posicao.symbol} | Quantidade: {posicao.qty} | Valor: ${posicao.market_value}")
    return posicoes

@tool
def verificar_saldo():
    saldo = trading_client.get_account()
    print(f"Saldo: {saldo.equity}")
    return saldo

@tool
def historico_negociacoes():
    """Retorna e exibe o histórico de posições atuais"""
    historico = trading_client.get_all_positions()
    for transacao in historico:
        print(f"Transação: {transacao.symbol} | Quantidade: {transacao.qty} | Valor Atual: ${transacao.market_value} | Preço Médio: ${transacao.avg_entry_price}")
    return historico

if __name__ == "__main__":
    verificar_saldo()
    verificar_posicoes()
    historico_negociacoes()
    get_stock_price("AAPL")