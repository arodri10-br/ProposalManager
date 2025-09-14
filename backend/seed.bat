
REM Dominio :
curl -X POST http://127.0.0.1:8000/dominios/hd/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"tabela\":\"SimNao\",\"descricao\":\"Sim ou Não\",\"chave\":\"SN\"}"
curl -X POST http://127.0.0.1:8000/dominios/hd/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"tabela\":\"TipoDadoDominio\",\"descricao\":\"Tipos de dados para domínio\",\"chave\":\"TIPO\"}"
curl -X POST http://127.0.0.1:8000/dominios/hd/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"tabela\":\"FornecedorSistema\",\"descricao\":\"Fornecedores de sistemas ERP\",\"chave\":\"FORN\"}"
curl -X POST http://127.0.0.1:8000/dominios/hd/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"tabela\":\"ClassificacaoDocumento\",\"descricao\":\"Classificação de documentos\",\"chave\":\"CLASS\"}"
curl -X POST http://127.0.0.1:8000/dominios/hd/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"tabela\":\"RegraRetencao\",\"descricao\":\"Regras de retenção de documentos\",\"chave\":\"RET\"}"

curl -X POST http://127.0.0.1:8000/dominios/data/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"tabela\":\"SimNao\",\"chave_valor\":\"S\",\"valor01\":\"Sim\"}"
curl -X POST http://127.0.0.1:8000/dominios/data/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"tabela\":\"SimNao\",\"chave_valor\":\"N\",\"valor01\":\"Não\"}"

curl -X POST http://127.0.0.1:8000/dominios/data/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"tabela\":\"TipoDadoDominio\",\"chave_valor\":\"C\",\"valor01\":\"Caracter\"}"
curl -X POST http://127.0.0.1:8000/dominios/data/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"tabela\":\"TipoDadoDominio\",\"chave_valor\":\"N\",\"valor01\":\"Numérico\"}"
curl -X POST http://127.0.0.1:8000/dominios/data/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"tabela\":\"TipoDadoDominio\",\"chave_valor\":\"D\",\"valor01\":\"Data\"}"

curl -X POST http://127.0.0.1:8000/dominios/data/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"tabela\":\"FornecedorSistema\",\"chave_valor\":\"ORACLE\",\"valor01\":\"Oracle\"}"
curl -X POST http://127.0.0.1:8000/dominios/data/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"tabela\":\"FornecedorSistema\",\"chave_valor\":\"SAP\",\"valor01\":\"SAP\"}"

curl -X POST http://127.0.0.1:8000/dominios/data/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"tabela\":\"ClassificacaoDocumento\",\"chave_valor\":\"PUB\",\"valor01\":\"Público\"}"
curl -X POST http://127.0.0.1:8000/dominios/data/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"tabela\":\"ClassificacaoDocumento\",\"chave_valor\":\"INT\",\"valor01\":\"Interno\"}"
curl -X POST http://127.0.0.1:8000/dominios/data/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"tabela\":\"ClassificacaoDocumento\",\"chave_valor\":\"CONF\",\"valor01\":\"Confidencial\"}"

curl -X POST http://127.0.0.1:8000/dominios/data/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"tabela\":\"RegraRetencao\",\"chave_valor\":\"RET5Y\",\"valor01\":\"5 anos\"}"
curl -X POST http://127.0.0.1:8000/dominios/data/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"tabela\":\"RegraRetencao\",\"chave_valor\":\"RET10Y\",\"valor01\":\"10 anos\"}"
curl -X POST http://127.0.0.1:8000/dominios/data/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"tabela\":\"RegraRetencao\",\"chave_valor\":\"ETERNAL\",\"valor01\":\"Eterno\"}"


REM Clientes : 
curl -X POST http://127.0.0.1:8000/clientes/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"nome_cliente\":\"Action Systems\",\"cnpj\":\"12345678000100\"}"
curl -X POST http://127.0.0.1:8000/clientes/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"nome_cliente\":\"Cargill Agrícola\",\"cnpj\":\"98765432000199\"}"

REM Sistemas :
curl -X POST http://127.0.0.1:8000/sistemas/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"nome_sistema\":\"GRA\",\"fornecedor_chave\":\"ORACLE\",\"versao\":\"1.0\"}"
curl -X POST http://127.0.0.1:8000/sistemas/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"nome_sistema\":\"JDE\",\"fornecedor_chave\":\"ORACLE\",\"versao\":\"9.2\"}"
curl -X POST http://127.0.0.1:8000/sistemas/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"nome_sistema\":\"SAP\",\"fornecedor_chave\":\"SAP\",\"versao\":\"S/4HANA\"}"

REM Modulos :
curl -X POST http://127.0.0.1:8000/modulos/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"id_sistema\":1,\"nome_modulo\":\"KaWhy\",\"descricao\":\"Módulo KaWhy\"}"
curl -X POST http://127.0.0.1:8000/modulos/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"id_sistema\":1,\"nome_modulo\":\"GRA\",\"descricao\":\"Módulo GRA\"}"
curl -X POST http://127.0.0.1:8000/modulos/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"id_sistema\":2,\"nome_modulo\":\"Distribuição\",\"descricao\":\"Distribuição JDE\"}"
curl -X POST http://127.0.0.1:8000/modulos/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"id_sistema\":2,\"nome_modulo\":\"Contábil\",\"descricao\":\"Contabilidade JDE\"}"
curl -X POST http://127.0.0.1:8000/modulos/ -H "accept: application/json" -H "Content-Type: application/json" -d "{\"id_sistema\":3,\"nome_modulo\":\"Manufatura\",\"descricao\":\"Manufatura SAP\"}"

REM Documentos Web :
curl -X POST "http://127.0.0.1:8000/upload/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "id_cliente=1" -F "nome_arquivo=EMENDA_CONSTITUCIONAL_132.html" -F "tipo=WEB" -F "classificacao_chave=PUB" -F "retencao_chave=ETERNAL" -F "url=https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc132.htm"

REM Documentos PDF Publico :
curl -X POST "http://127.0.0.1:8000/upload/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "id_cliente=1" -F "nome_arquivo=agreement-management-implementation-guide.pdf" -F "tipo=MANUAL" -F "classificacao_chave=PUB" -F "retencao_chave=RET5Y" -F "file=@C:/Users/algr/OneDrive/Documentos/MANUAI~1/agreement-management-implementation-guide.pdf;type=application/pdf"

REM Documentos PDF Confidencial :
curl -X POST "http://127.0.0.1:8000/upload/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "id_cliente=1" -F "nome_arquivo=demand-scheduling-execution-implementation-guide.pdf" -F "tipo=MANUAL" -F "classificacao_chave=CONF" -F "retencao_chave=ETERNAL" -F "file=@C:/Users/algr/OneDrive/Documentos/MANUAI~1/demand-scheduling-execution-implementation-guide.pdf;type=application/pdf"

