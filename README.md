# A Aurora Ajusta a Trajetória na Aproximação a Marte - MGPEB
Este repositório contém o código-fonte do MGPEB, um sistema de missão crítica desenvolvido para simular o gerenciamento de pouso, telemetria e estabilização de uma colônia espacial em Marte (Missão Aurora Siger).

O algoritmo foi desenvolvido em ambiente local utilizando a linguagem Python, com foco em eficiência de hardware, proteção planetária e estruturas de dados otimizadas.

## Arquitetura e Funcionalidades do Código
O sistema foi moldado para operar em ambientes hostis e com grande escassez, como Marte. Dessa forma simulamos restrições severas de hardware, utilizando conceitos de Engenharia de Software e Ciência da Computação:

- Estruturas de Dados: Utilização de "collections.deque" para processamento O(1) no diagnóstico de sensores e encapsulamento da frota em uma lista dinâmica unificada de dicionários, denominada como "frota_status", economizando memória RAM ao invés de usar múltiplas listas redundantes.
  
- Inteligência Heurística de Pouso: A fila tradicional (FIFO) é quebrada através de um sistema de Score Dinâmico, que calcula a urgência de descida de cada módulo com base em 5 fatores (combustível, massa, prioridade nativa, criticidade e tempo de espera).

- Ordenação Dinâmica: Implementação do algoritmo Bubble Sort, a fim de reorganizar a matriz de dados em tempo real e garantindo que os módulos em estado crítico (emergência de combustível) saltem para o topo da fila de autorização de pouso.

- Modelagem Física e Matemática: Simulação do consumo de combustível em queda livre baseada na função de 1º grau C(t) = 18.5 - 0.8t, que calcula o ponto de esgotamento exato do tanque.


## Instruções de Instalação
Para garantir a integridade da simulação, antes de executar o código, o usuário deve se atentar a baixar as bibliotecas externas responsáveis pela telemetria visual e modelagem matemática, que não vêm instaladas por padrão no Python, por isso é tão necessário. 

- Abra o seu terminal e execute esse comando: "pip install matplotlib numpy".

- Matplotlib: Utilizada para gerar os gráficos de combustível inicial da frota e a a modelagem matemática de descida.

- Numpy: Utilizada para a geração eficiente de vetores temporais e cálculos da modelagem matemática.

## Como Executar o Software
O sistema é autossuficiente e, desse modo, ao ser iniciado, ele verifica e gera automaticamente o arquivo local de banco de dados em "modulos.csv", não sendo necessário criá-lo manualmente. Para executar o software sem transtornos, certifique-se que:

- O arquivo principal "mgpeb.py" está localizado em um diretório de fácil acesso.

- Abra o terminal, navegue até a pasta do projeto e digite o comando: "python mgpeb.py".

## Manual de Operação da Interface
Ao iniciar o algoritmo, o sistema apresentará ao usuário o painel de controle principal, que possui 5 opções de operação.

- Observação: após visualizar o conteúdo mostrado pela opção do centro de comando, sempre aperte ENTER para retornar ao menu principal e seguir com a operação.

- (1) Verificar Status da Estação: essa operação demonstra o diagnóstico dos sistemas ambientais e orbitais em tempo real processando a fila de sensores.

- (2) Mostrar Gráfico da Frota: exibe um gráfico de barras que comprova a teoria de combustível de chegada. (atenção: uma nova janela de interface gráfica será aberta. O usuário deve fechar a janela do gráfico para liberar o terminal e prosseguir com a simulação).

- (3) Iniciar Protocolo de Pouso MGPEB: Executa a inteligência principal, exibindo a tabela de aproximação onde os valores e status são atualizados automaticamente e ordenados pelo Score de prioridade. Aguarde o processamento contínuo até que todos os módulos estejam em solo para visualizar a simulação física com o resultado do pouso.

- (4) Modelagem Física de Descida: Exibe o gráfico de decaimento linear, evidenciando o limite de emergência da missão (18.5%). O usuário deve fechar a janela do gráfico para retornar ao menu.

- (5) Encerrar Sistema: essa operação desliga os motores virtuais e encerra o algoritmo com segurança.
