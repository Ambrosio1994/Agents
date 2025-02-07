# Ferramentas para fazer análises das ações para verificar o desempenho e tomar decisões

from langchain_core.tools import tool
import yfinance as yf
import numpy as np

@tool
def analyze_stock(symbol: str) -> str:
    """
    Realiza uma análise detalhada da ação utilizando dados históricos e métricas fundamentais.
    
    - Coleta dados do último ano para obter informações técnicas (médias móveis, RSI, volume e volatilidade).
    - Obtém métricas fundamentais via yf.Ticker.info, como P/L, P/VPA, Dividend Yield, EV/EBITDA, ROE,
      Dívida Líquida/EBITDA e crescimento (receita e lucro).
    - Sugere uma decisão simples baseada na comparação do preço atual com as médias móveis (50 e 200 dias).
    """
    try:
        # Obter dados históricos do último ano para análise técnica
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1y")
        if hist.empty:
            return f"Nenhum dado disponível para {symbol}."
        
        # Cálculo dos indicadores técnicos
        current_price = hist['Close'].iloc[-1]
        sma20 = hist['Close'].rolling(window=20).mean().iloc[-1]
        sma50 = hist['Close'].rolling(window=50).mean().iloc[-1]
        sma200 = hist['Close'].rolling(window=200).mean().iloc[-1] if len(hist) >= 200 else None
        sma200_text = f"{sma200:.2f}" if sma200 is not None else "N/A"
        
        # Cálculo do RSI (período 14)
        delta = hist['Close'].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(window=14, min_periods=14).mean()
        avg_loss = loss.rolling(window=14, min_periods=14).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]
        
        # Último volume registrado e volatilidade anualizada (usando 252 dias de negociação)
        volume = int(hist['Volume'].iloc[-1])
        hist['Daily Return'] = hist['Close'].pct_change()
        volatility = hist['Daily Return'].std() * np.sqrt(252)
        
        # Obter métricas fundamentais do ticker
        info = ticker.info
        pe = info.get("trailingPE", "N/A")
        price_to_book = info.get("priceToBook", "N/A")
        dividend_yield = info.get("dividendYield", "N/A")
        enterprise_to_ebitda = info.get("enterpriseToEbitda", "N/A")
        roe = info.get("returnOnEquity", "N/A")
        revenue_growth = info.get("revenueGrowth", "N/A")
        earnings_growth = info.get("earningsQuarterlyGrowth", "N/A")
        
        # Dívida Líquida/EBITDA
        total_debt = info.get("totalDebt")
        total_cash = info.get("totalCash")
        ebitda = info.get("ebitda")
        if total_debt is not None and total_cash is not None and ebitda is not None and ebitda != 0:
            net_debt = total_debt - total_cash
            debt_to_ebitda = net_debt / ebitda
        else:
            debt_to_ebitda = "N/A"
        
        # Formatação dos valores em porcentagem, se numéricos
        if isinstance(dividend_yield, (float, int)):
            dividend_yield_pct = f"{dividend_yield * 100:.2f}%"
        else:
            dividend_yield_pct = dividend_yield
        
        if isinstance(roe, (float, int)):
            roe_pct = f"{roe * 100:.2f}%"
        else:
            roe_pct = roe
        
        if isinstance(revenue_growth, (float, int)):
            revenue_growth_pct = f"{revenue_growth * 100:.2f}%"
        else:
            revenue_growth_pct = revenue_growth
        
        if isinstance(earnings_growth, (float, int)):
            earnings_growth_pct = f"{earnings_growth * 100:.2f}%"
        else:
            earnings_growth_pct = earnings_growth
        
        analysis_text = (
            f"Análise para {symbol}:\n\n"
            f"--- Métricas Técnicas ---\n"
            f"Preço atual: {current_price:.2f}\n"
            f"SMA 20 dias: {sma20:.2f}\n"
            f"SMA 50 dias: {sma50:.2f}\n"
            f"SMA 200 dias: {sma200_text}\n"
            f"RSI (14): {current_rsi:.2f}\n"
            f"Volume de negociação (último dia): {volume}\n"
            f"Volatilidade anualizada: {volatility:.2%}\n\n"
            f"--- Métricas Fundamentais ---\n"
            f"P/L (Preço/Lucro): {pe}\n"
            f"P/VPA (Preço/Valor Patrimonial): {price_to_book}\n"
            f"Dividend Yield: {dividend_yield_pct}\n"
            f"EV/EBITDA: {enterprise_to_ebitda}\n"
            f"ROE: {roe_pct}\n"
            f"Dívida Líquida/EBITDA: {debt_to_ebitda}\n"
            f"Crescimento de Receita: {revenue_growth_pct}\n"
            f"Crescimento de Lucro Trimestral: {earnings_growth_pct}\n\n"
        )
        return analysis_text
    except Exception as e:
        return f"Erro ao analisar {symbol}: {str(e)}"

if __name__ == "__main__":
    symbol = "AAPL" 
    print(analyze_stock.invoke(symbol))