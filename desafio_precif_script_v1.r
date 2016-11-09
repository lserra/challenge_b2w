# OBJETIVO: TESTE DE PRECIFICAÇÃO
# EMPRESA:  B2W
# AUTOR:    laercio.serra@gmail.com
# DATA:     26/09/2016
# VERSÃO:   1.0


# CARREGAR OS PACOTES
require(data.table)
require(dplyr)
require(pryr)
require(lubridate)
require(ggplot2)
require(stringr)
require(reshape2)

# SELECIONAR O DIRETÓRIO DE TRABALHO
# setwd(dir = "F:/B2W")
setwd(dir = "/home/lserra/Downloads/b2w")

### 1) IMPORTAR E ESTUTURAR OS DADOS
### VENDAS
sales <- fread(input = "bases/sales.csv", verbose = TRUE)
setnames(x = sales, old = "DATE_ORDER", new = "DATE")
setkey(sales, PROD_ID, DATE)
summary(sales) # Não tem missing
str(sales)
