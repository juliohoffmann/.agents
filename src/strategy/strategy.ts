// Estrutura do documento Binance_Padrao.pdf em JavaScript
// Array de configurações de banca (baseado na tabela principal, com entradas incompletas no final)
const configuracoesBanca = [
  {
    banca: 'DE 90 A 150 USDT',
    strategy: 'Millionaire Strategy',
    long1stOrderSize: 9,
    short1stOrderSize: 3,
    leverage: 20,
    stopLoss: 180,
    doubleFirstLong: 'ON',
    doubleFirstShort: 'ON',
    quantidadeMoedas: 1
  },
  {
    banca: '300 USDT',
    strategy: 'Millionaire Strategy',
    long1stOrderSize: 9,
    short1stOrderSize: 3,
    leverage: 20,
    stopLoss: 180,
    doubleFirstLong: 'ON',
    doubleFirstShort: 'ON',
    quantidadeMoedas: 2
  },
  {
    banca: '500 USDT',
    strategy: 'Millionaire Strategy',
    long1stOrderSize: 9,
    short1stOrderSize: 3,
    leverage: 20,
    stopLoss: 180,
    doubleFirstLong: 'ON',
    doubleFirstShort: 'ON',
    quantidadeMoedas: 3
  },
  {
    banca: '1.000 USDT',
    strategy: 'Millionaire Strategy',
    long1stOrderSize: 9,
    short1stOrderSize: 3,
    leverage: 20,
    stopLoss: 180,
    doubleFirstLong: 'ON',
    doubleFirstShort: 'ON',
    quantidadeMoedas: 6
  },
  {
    banca: '2.000 USDT',
    strategy: 'Millionaire Strategy',
    long1stOrderSize: 9,
    short1stOrderSize: 3,
    leverage: 20,
    stopLoss: 180,
    doubleFirstLong: 'ON',
    doubleFirstShort: 'ON',
    quantidadeMoedas: 9
  },
  {
    banca: '3.000 USDT',
    strategy: 'Millionaire Strategy',
    long1stOrderSize: 9,
    short1stOrderSize: 10,
    leverage: 20,
    stopLoss: 600,
    doubleFirstLong: 'OFF',
    doubleFirstShort: 'OFF',
    quantidadeMoedas: 9
  },
  {
    banca: '5.000 USDT',
    strategy: 'Millionaire Strategy',
    long1stOrderSize: 9,
    short1stOrderSize: 15,
    leverage: 20,
    stopLoss: 900,
    doubleFirstLong: 'OFF',
    doubleFirstShort: 'OFF',
    quantidadeMoedas: 11
  },
  {
    banca: '7.000 USDT',
    strategy: 'Millionaire Strategy',
    long1stOrderSize: 9,
    short1stOrderSize: 20,
    leverage: 20,
    stopLoss: 1200,
    doubleFirstLong: 'ON',
    doubleFirstShort: 'ON',
    quantidadeMoedas: 11
  },
  {
    banca: '8.000 USDT',
    strategy: 'Millionaire Strategy',
    long1stOrderSize: 9,
    short1stOrderSize: 21,
    leverage: 20,
    stopLoss: 1260,
    doubleFirstLong: 'ON',
    doubleFirstShort: 'ON',
    quantidadeMoedas: 12
  },
  {
    banca: '9.000 USDT',
    strategy: 'Millionaire Strategy',
    long1stOrderSize: 9,
    short1stOrderSize: 24,
    leverage: 20,
    stopLoss: 1440,
    doubleFirstLong: 'ON',
    doubleFirstShort: 'ON',
    quantidadeMoedas: 12
  },
  {
    banca: '10.000 USDT',
    strategy: 'Millionaire Strategy',
    long1stOrderSize: 9,
    short1stOrderSize: 28,
    leverage: 20,
    stopLoss: 1680,
    doubleFirstLong: 'ON',
    doubleFirstShort: 'ON',
    quantidadeMoedas: 12
  },
  // Entradas adicionais/incompletas no final do documento
  {
    banca: '4.000 USDT',
    strategy: 'Millionaire Strategy',
    long1stOrderSize: 9,
    short1stOrderSize: 12,
    leverage: 20,
    stopLoss: 720,
    doubleFirstLong: 'OFF',
    doubleFirstShort: 'OFF',
    quantidadeMoedas: 10
  },
  {
    banca: '6.000 USDT',
    strategy: 'Millionaire Strategy',
    long1stOrderSize: 9,
    short1stOrderSize: 17,
    leverage: 20,
    stopLoss: null,  // Incompleto no documento
    doubleFirstLong: null,
    doubleFirstShort: null,
    quantidadeMoedas: null
  }
];

// Sugestões de moedas (agrupadas por listas repetidas/variadas no documento)
// Cada subarray representa uma lista distinta; moedas em vermelho no original são de alta volatilidade/memecoins (ex: 1000PEPE/USDT, DOGE/USDT)
const sugestoesMoedas = [
  ['ADA/USDT', 'TRX/USDT', 'ARB/USDT', 'XRP/USDT', 'APT/USDT', 'FIL/USDT', 'SUSHI/USDT', 'ATOM/USDT', 'NOT/USDT', '1000PEPE/USDT', 'CFX/USDT', '1INCH/USDT', 'MASK/USDT', 'SNX/USDT', 'THETA/USDT', 'OP/USDT', 'COMP/USDT', 'SUI/USDT', 'CHZ/USDT', '1000SHIB/USDT', 'DOGE/USDT', 'NEAR/USDT', 'SAND/USDT', 'APE/USDT', 'SOL/USDT', 'CRV/USDT', 'DOT/USDT', 'UNI/USDT', 'BNB/USDT', 'LTC/USDT', 'BCH/USDT', 'LINK/USDT', 'ETC/USDT', 'ETH/USDT', 'AAVE/USDT', 'AVAX/USDT'],
  ['ADA/USDT', 'TRX/USDT', 'ARB/USDT', 'XRP/USDT', 'APT/USDT', 'FIL/USDT', 'SUSHI/USDT', 'ATOM/USDT', 'NOT/USDT', '1000PEPE/USDT', 'CFX/USDT', '1INCH/USDT', 'MASK/USDT', 'SNX/USDT', 'THETA/USDT', 'OP/USDT', 'COMP/USDT', 'SUI/USDT', 'CHZ/USDT', '1000SHIB/USDT', 'DOGE/USDT', 'NEAR/USDT', 'SAND/USDT', 'APE/USDT', 'SOL/USDT', 'CRV/USDT', 'DOT/USDT'],
  // As próximas 3 listas são idênticas à anterior (repetições no documento)
  ['ADA/USDT', 'TRX/USDT', 'ARB/USDT', 'XRP/USDT', 'APT/USDT', 'FIL/USDT', 'SUSHI/USDT', 'ATOM/USDT', 'NOT/USDT', '1000PEPE/USDT', 'CFX/USDT', '1INCH/USDT', 'MASK/USDT', 'SNX/USDT', 'THETA/USDT', 'OP/USDT', 'COMP/USDT', 'SUI/USDT', 'CHZ/USDT', '1000SHIB/USDT', 'DOGE/USDT', 'NEAR/USDT', 'SAND/USDT', 'APE/USDT', 'SOL/USDT', 'CRV/USDT', 'DOT/USDT'],
  ['ADA/USDT', 'TRX/USDT', 'ARB/USDT', 'XRP/USDT', 'APT/USDT', 'FIL/USDT', 'SUSHI/USDT', 'ATOM/USDT', 'NOT/USDT', '1000PEPE/USDT', 'CFX/USDT', '1INCH/USDT', 'MASK/USDT', 'SNX/USDT', 'THETA/USDT', 'OP/USDT', 'COMP/USDT', 'SUI/USDT', 'CHZ/USDT', '1000SHIB/USDT', 'DOGE/USDT', 'NEAR/USDT', 'SAND/USDT', 'APE/USDT', 'SOL/USDT', 'CRV/USDT', 'DOT/USDT'],
  ['ADA/USDT', 'TRX/USDT', 'ARB/USDT', 'XRP/USDT', 'APT/USDT', 'FIL/USDT', 'SUSHI/USDT', 'ATOM/USDT', 'NOT/USDT', '1000PEPE/USDT', 'CFX/USDT', '1INCH/USDT', 'MASK/USDT', 'SNX/USDT', 'THETA/USDT', 'OP/USDT', 'COMP/USDT', 'SUI/USDT', 'CHZ/USDT', '1000SHIB/USDT', 'DOGE/USDT', 'NEAR/USDT', 'SAND/USDT', 'APE/USDT', 'SOL/USDT', 'CRV/USDT', 'DOT/USDT'],
  ['ADA/USDT', 'TRX/USDT', 'ARB/USDT', 'XRP/USDT', 'APT/USDT', 'FIL/USDT', 'SUSHI/USDT', 'ATOM/USDT', 'NOT/USDT', '1000PEPE/USDT', 'CFX/USDT', '1INCH/USDT', 'MASK/USDT', 'SNX/USDT', 'THETA/USDT', 'OP/USDT', 'COMP/USDT', 'SUI/USDT', 'CHZ/USDT', '1000SHIB/USDT', 'DOGE/USDT', 'NEAR/USDT', 'SAND/USDT', 'APE/USDT', 'SOL/USDT', 'CRV/USDT', 'DOT/USDT', 'UNI/USDT'],
  ['ADA/USDT', 'TRX/USDT', 'ARB/USDT', 'XRP/USDT', 'APT/USDT', 'FIL/USDT', 'SUSHI/USDT', 'ATOM/USDT', 'NOT/USDT', '1000PEPE/USDT', 'CFX/USDT', '1INCH/USDT', 'MASK/USDT', 'SNX/USDT', 'THETA/USDT', 'OP/USDT', 'COMP/USDT', 'SUI/USDT', 'CHZ/USDT', '1000SHIB/USDT', 'DOGE/USDT', 'NEAR/USDT', 'SAND/USDT', 'APE/USDT', 'SOL/USDT', 'CRV/USDT', 'DOT/USDT', 'UNI/USDT', 'BNB/USDT'],
  ['ADA/USDT', 'TRX/USDT', 'ARB/USDT', 'XRP/USDT', 'APT/USDT', 'FIL/USDT', 'SUSHI/USDT', 'ATOM/USDT', 'NOT/USDT', '1000PEPE/USDT', 'CFX/USDT', '1INCH/USDT', 'MASK/USDT', 'SNX/USDT', 'THETA/USDT', 'OP/USDT', 'COMP/USDT', 'SUI/USDT', 'CHZ/USDT', '1000SHIB/USDT', 'DOGE/USDT', 'NEAR/USDT', 'SAND/USDT', 'APE/USDT', 'SOL/USDT', 'CRV/USDT', 'DOT/USDT', 'UNI/USDT', 'BNB/USDT'],
  ['ADA/USDT', 'TRX/USDT', 'ARB/USDT', 'XRP/USDT', 'APT/USDT', 'FIL/USDT', 'SUSHI/USDT', 'ATOM/USDT', 'NOT/USDT', '1000PEPE/USDT', 'CFX/USDT', '1INCH/USDT', 'MASK/USDT', 'SNX/USDT', 'THETA/USDT', 'OP/USDT', 'COMP/USDT', 'SUI/USDT', 'CHZ/USDT', '1000SHIB/USDT', 'DOGE/USDT', 'NEAR/USDT', 'SAND/USDT', 'APE/USDT', 'SOL/USDT', 'CRV/USDT', 'DOT/USDT', 'UNI/USDT', 'BNB/USDT', 'LTC/USDT', 'BCH/USDT', 'LINK/USDT', 'ETC/USDT', 'ETH/USDT', 'AAVE/USDT'],
  ['ADA/USDT', 'TRX/USDT', 'ARB/USDT', 'XRP/USDT', 'APT/USDT', 'FIL/USDT', 'SUSHI/USDT', 'ATOM/USDT', 'NOT/USDT', '1000PEPE/USDT', 'CFX/USDT', '1INCH/USDT', 'MASK/USDT', 'SNX/USDT', 'THETA/USDT', 'OP/USDT', 'COMP/USDT', 'SUI/USDT', 'CHZ/USDT', '1000SHIB/USDT', 'DOGE/USDT', 'NEAR/USDT', 'SAND/USDT', 'APE/USDT', 'SOL/USDT', 'CRV/USDT', 'DOT/USDT', 'UNI/USDT', 'BNB/USDT', 'LTC/USDT', 'BCH/USDT', 'LINK/USDT', 'ETC/USDT', 'ETH/USDT', 'AAVE/USDT', 'AVAX/USDT'],
  // As próximas 2 listas são idênticas à anterior (repetições no documento)
  ['ADA/USDT', 'TRX/USDT', 'ARB/USDT', 'XRP/USDT', 'APT/USDT', 'FIL/USDT', 'SUSHI/USDT', 'ATOM/USDT', 'NOT/USDT', '1000PEPE/USDT', 'CFX/USDT', '1INCH/USDT', 'MASK/USDT', 'SNX/USDT', 'THETA/USDT', 'OP/USDT', 'COMP/USDT', 'SUI/USDT', 'CHZ/USDT', '1000SHIB/USDT', 'DOGE/USDT', 'NEAR/USDT', 'SAND/USDT', 'APE/USDT', 'SOL/USDT', 'CRV/USDT', 'DOT/USDT', 'UNI/USDT', 'BNB/USDT', 'LTC/USDT', 'BCH/USDT', 'LINK/USDT', 'ETC/USDT', 'ETH/USDT', 'AAVE/USDT', 'AVAX/USDT'],
  ['ADA/USDT', 'TRX/USDT', 'ARB/USDT', 'XRP/USDT', 'APT/USDT', 'FIL/USDT', 'SUSHI/USDT', 'ATOM/USDT', 'NOT/USDT', '1000PEPE/USDT', 'CFX/USDT', '1INCH/USDT', 'MASK/USDT', 'SNX/USDT', 'THETA/USDT', 'OP/USDT', 'COMP/USDT', 'SUI/USDT', 'CHZ/USDT', '1000SHIB/USDT', 'DOGE/USDT', 'NEAR/USDT', 'SAND/USDT', 'APE/USDT', 'SOL/USDT', 'CRV/USDT', 'DOT/USDT'],
  // Última lista (após 4.000 USDT)
  ['ADA/USDT', 'TRX/USDT', 'ARB/USDT', 'XRP/USDT', 'APT/USDT', 'FIL/USDT', 'SUSHI/USDT', 'ATOM/USDT', 'NOT/USDT', '1000PEPE/USDT', 'CFX/USDT', '1INCH/USDT', 'MASK/USDT', 'SNX/USDT', 'THETA/USDT', 'OP/USDT', 'COMP/USDT', 'SUI/USDT', 'CHZ/USDT', '1000SHIB/USDT', 'DOGE/USDT', 'NEAR/USDT', 'SAND/USDT', 'APE/USDT', 'SOL/USDT', 'CRV/USDT', 'DOT/USDT']
];

// Notas e fragmentos adicionais do documento
const notasAdicionais = {
  sugestoes: 'sugestões de moedas | Moedas em Vermelho são de alta volatilidade ou memecoins',
  fragmentoSolto: '1020 ON ON 11',  // Fragmento isolado no documento
  tituloFinal: 'Binance - Estratégia Padrão'
};

// Exemplo de uso: Exibir no console
console.log('Configurações de Banca:', configuracoesBanca);
console.log('Sugestões de Moedas (primeira lista):', sugestoesMoedas[0]);
console.log('Notas Adicionais:', notasAdicionais);
