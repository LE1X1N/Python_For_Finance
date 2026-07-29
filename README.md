# Python For Finance

## Part1 数据获取

### 1. BeautifulSoup
通过 `requests + BeautifulSoup4` 公网 HTTP 请求，解析 Yahoo Finance 获取股票数据

### 2. Selenium

使用 `Selenium` 结合`xpath`解析页面内容获取数据

### 3. API
国内：
    AKShare
    Baostock
    AllTick

国外：
    Massive (原Polygon)
    Finhub
    Twelve Data

### 4. 官方来源
国内A股正规行情请使用 Level 1 / Level 2 获取。

参考上海证券交易所Level-1和Level-2的产品说明书。
[Level-1](/docs/Level-1 产品说明书.pdf)
[Level-2](/docs/Level-2 产品说明书.pdf)

**Level1行情**

- 买卖档位：仅提供买一至五价/量和卖一至五价/量（五档行情）。

- 成交数据：显示分时成交的汇总信息（如每分钟的成交量、均价等）。

**Level2行情**

- 买卖档位：提供买一至买十、卖一至卖十的详细挂单（十档行情），可观察市场深度。

- 成交数据：包含逐笔成交明细，精确到每一笔订单的成交时间、价格和数量。

### 5. 模拟
提供脚本模拟tick级别数据变化

## Part2 量化策略

- MA Crossover Strategy
- MACD Crossover Strategy
- RSI Crossover Strategy
- BB Bounce Strategy



## Part3 实时交易