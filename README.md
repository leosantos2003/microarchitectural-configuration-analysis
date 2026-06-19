# Análise de Configurações Microarquiteturais

**INF01113 – Organização de Computadores – 2026/1**

Alunos: Henrique Anderson Knorst, Henrique de Lima Bortolomiol, Leonardo Rocha dos Santos, Leônidas Lewy de Paula dos Santos

## 1. Introdução e objetivo

O trabalho analisa o impacto de configurações microarquiteturais no desempenho de um processador utilizando o simulador gem5 (x86). Avaliamos o tempo de execução e os Ciclos por Instrução (CPI) para determinar os efeitos de cada alteração em hardware. Foram utilizados três benchmarks com características distintas:

#### Matrix-Mult:
- **Como funciona:** O algoritmo padrão multiplica as linhas de uma matriz pelas colunas de outra, calculando produtos escalares para formar uma matriz resultante. Estruturalmente, a execução consiste em três grandes laços de repetição aninhados.
- **Comportamento na arquitetura:** É um problema que gera gargalo de memória. Ao varrer colunas inteiras de matrizes grandes, o algoritmo exige o acesso constante a endereços de memória que estão distantes uns dos outros fisicamente. Isso sobrecarrega a hierarquia de cache, fazendo com que a CPU execute poucas instruções lógicas e passe muito tempo ociosa esperando os dados serem trazidos da memória RAM. Complexidade O(n³).

#### FFT (Fast Fourier Transform):
- **Como funciona:** É um algoritmo que calcula a Transformada Discreta de Fourier, convertendo sinais (como áudio ou ondas) do domínio do tempo para o domínio da frequência. Ele faz isso dividindo o problema matemático principal em dezenas de cálculos menores e recursivos envolvendo senos, cossenos e números complexos.
- **Comportamento na arquitetura:** Por causa da matemática pesada, apresenta um comportamento focado em estressar bastante a ALU com uma alta densidade de instruções de ponto flutuante. Devido à sua natureza de divisão e conquista, ele acessa os dados da memória em intervalos regulares e pré-calculados, dando saltos. Complexidade O(n log(n)).

#### BubbleSort:
- **Como funciona:** É um algoritmo de ordenação que percorre um vetor de dados repetidas vezes. Em cada passagem, compara pares de elementos adjacentes e os troca de lugar se estiverem na ordem errada, fazendo os maiores valores irem para o final da lista até que tudo esteja ordenado.
- **Comportamento na arquitetura:** Devido à sua estrutura baseada em sucessivas comparações, é caracterizado por laços curtos e com uma altíssima dependência da predição de desvios da CPU, o que dificulta o paralelismo. Como ele apenas troca posições vizinhas em um mesmo conjunto de dados, possui baixo uso e tráfego de memória. Complexidade O(n²).
 
## 2. Configuração base

Para isolar as variáveis, adotamos uma configuração como linha de base. Ao variar um parâmetro, os demais foram mantidos em seus valores originais:

- L1 Cache Size: 16kB.
- L1 Cache Associativity: 8-way.
- Fetch Buffer Size: 64 entradas.
 
## 3. Escolha e justificativa dos parâmetros
Selecionamos três parâmetros para testar gargalos específicos do processador:

- **Tamanho da Cache L1 (2kB a 16kB):** É a capacidade total de armazenamento da memória mais rápida e próxima à CPU. Escolhido para investigar as misses de cache por capacidade. O foco era avaliar como a localidade espacial (dados próximos acessados em sequência) e a localidade temporal (dados acessados repetidas vezes em curto período) afetam os algoritmos, causando misses. Eram esperadas alterações no desempenho de algoritmos com alta dependência espacial e temporal.
- **Associatividade da Cache L1 (1-way a 16-way):** É o número de blocos dentro de um conjunto da cache em que um mesmo endereço de memória pode ser alocado. Escolhida para analisar as faltas por conflito os misses de cache. Esperava-se afetar os algoritmos que apresentam localidade espacial, alterando a quantidade de misses da cache.
- **Tamanho do Fetch Buffer (8 a 64):** É a fila que armazena as instruções recém-buscadas da memória, aguardando a decodificação e o despacho para execução. Escolhido para avaliar o fluxo de entrada de instruções. Quanto maior o Fetch Buffer, mais instruções são processadas simultaneamente. A hipótese era afetar o Paralelismo em Nível de Instrução dos algoritmos.

## 4. Resultados

### 4.1. Tamanho da Cache L1 (2kB a 16kB)

<img width="675" height="450" alt="Grafico_CacheSize_IPC" src="https://github.com/user-attachments/assets/3df54e9f-7654-48cc-9937-2bc0c6487745" />

<img width="675" height="450" alt="Grafico_CacheSize_Tempo" src="https://github.com/user-attachments/assets/4317c496-66c8-4661-b5d0-861e26c36d38" />

#### Matrix-Mult:
- **IPC:** Apresentou o maior ganho. Uma cache maior permite reter grupos inteiros da matriz próximas ao processador, evitando expulsões por falta de espaço. Consequentemente, a CPU sofre menos interrupções esperando dados da memória principal, reduzindo os ciclos ociosos e permitindo que o processador execute muito mais instruções úteis a cada pulso de clock.
- **Tempo de Execução:** Demonstrou uma redução expressiva e inversamente proporcional ao ganho de IPC, atingindo seu melhor resultado a partir de 8kB. Ao acessar os dados rapidamente direto da cache L1, o processador elimina o principal gargalo do algoritmo (o tráfego com a memória RAM), conseguindo concluir os pesados laços de repetição em muito menos tempo.

#### FFT:
- **IPC:** Demonstrou um crescimento quase linear e constante. Como esse algoritmo acessa dados dando saltos previsíveis na memória, o aumento gradual do tamanho da cache L1 permitiu reter uma quantidade cada vez maior de operandos úteis. Isso reduziu as idas à memória principal e manteve a ALU sendo alimentada com alta eficiência, aumentando continuamente as instruções executadas por ciclo.
- **Tempo de Execução:** Apresentou uma queda drástica e inversamente proporcional ao ganho de IPC. Com a mitigação das perdas de cache por capacidade, o processador eliminou seus ciclos ociosos. Essa alta disponibilidade constante de dados permitiu otimizar o fluxo das pesadas operações matemáticas de ponto flutuante, acelerando notavelmente a conclusão do algoritmo.

#### BubbleSort:
- **IPC:** Manteve-se praticamente inalterado, estagnado na faixa de ~0.94. Diferente da multiplicação de matrizes, o BubbleSort manipula um conjunto de dados pequeno e com trocas estritamente vizinhas. Isso significa que os dados já cabiam perfeitamente na configuração mínima de cache (2kB). Portanto, o aumento de capacidade foi indiferente, pois o verdadeiro gargalo que limita o desempenho não é o acesso à memória, mas sim as constantes quebras de fluxo no pipeline causadas pela dificuldade da CPU em prever os inúmeros desvios gerados pelas comparações do algoritmo.
- **Tempo de Execução:** Permaneceu constante e sem melhorias. Como não existiam misses por capacidade a serem mitigadas, o processador não teve nenhum ganho de tempo na busca de dados. Isso evidencia que adicionar recursos físicos na memória L1 é uma estratégia ineficaz para acelerar o tempo de execução de algoritmos curtos, orientados a controle lógico e com baixo tráfego de memória.

#### Médias globais e custo benefício:
- Ao dobrar o tamanho da cache inicial de 2kB para 4kB (um aumento de 100% no hardware), o ganho médio de IPC foi o mais expressivo, de +5,3% (saltando de 0.905 para 0.953), resultando na queda mais abrupta do tempo médio de execução. No entanto, quadruplicar ou octuplicar a memória para 8kB e 16kB gerou ganhos de IPC estagnados na faixa de +3,7% e +4,6%. Isso prova que o investimento inicial apresenta um ótimo custo-benefício por mitigar as faltas de cache mais críticas, mas configurações muito maiores encarecem o processador em área e energia sem multiplicar o desempenho na mesma proporção.

### 4.2. Associatividade da Cache L1 (1-way a 16-way)

<img width="675" height="450" alt="Grafico_FetchBuffer_IPC" src="https://github.com/user-attachments/assets/73a01a1b-048b-4726-8dd3-5add766c807e" />

<img width="675" height="450" alt="Grafico_Associativity_Tempo" src="https://github.com/user-attachments/assets/088e3be2-58e7-421c-b107-d49206b8ef28" />

#### Matrix-Mult:
- **IPC:** Apresentou um crescimento expressivo (de 1.01 para 1.20) ao sair do mapeamento direto (1-way) e avançar até a configuração 8-way. O aumento da associatividade resolveu misses de endereço ao permitir que múltiplos blocos mapeados para o mesmo conjunto coexistam na cache, eliminando paradas desnecessárias no processador e elevando drasticamente o IPC.
- **Tempo de Execução:** Demonstrou uma redução acentuada, estabilizando a partir de 8 vias de associatividade. Ao mitigar as severas penalidades de busca na memória RAM para resgatar dados recentemente expulsos devido a misses, o processador manteve um fluxo contínuo de execução, reduzindo drasticamente o tempo total.

#### FFT:
- **IPC:** Demonstrou um salto notável logo na transição inicial de 1-way para 2-way (subindo de 0.85 para 0.93). Devido à sua natureza de divisão e conquista, o algoritmo FFT acessa a memória em intervalos regulares e pré-calculados (saltos). A introdução de apenas duas vias (2-way) foi suficiente para resolver a maior parte dos misses de cache iniciais, garantindo que os dados de saltos diferentes residissem juntos na cache e aumentando a eficiência da ALU.
- **Tempo de Execução:** Exibiu uma queda imediata e expressiva no primeiro salto estrutural para 2-way. Nos incrementos subsequentes (de 4-way em diante), a curva de melhora no tempo de execução torna-se praticamente estável e com ganhos mínimos, uma vez que o gargalo principal de conflitos gerados pelo padrão de acesso do algoritmo já havia sido solucionado nas primeiras vias de associatividade.

#### BubbleSort:
- **IPC:** Permaneceu completamente estagnado na faixa de ~0.94, independentemente do nível de associatividade adotado. Como o BubbleSort possui uma excelente localidade espacial por varrer o vetor comparando estritamente elementos adjacentes (vizinhos de memória), ele naturalmente quase não sofre com misses. Como os dados sequenciais entram e saem de forma organizada na cache, alterar a forma como os conjuntos são subdivididos é indiferente para o algoritmo , mantendo o processador limitado pelo seu gargalo real, que são as quebras de pipeline por erros de predição de desvios.
- **Tempo de Execução:** Manteve-se perfeitamente constante ao longo de todos os testes. Como o tráfego de memória e a latência de busca de dados não eram problemas para a estrutura linear do BubbleSort, a mudança de associatividade da cache L1 não trouxe qualquer aceleração prática.

#### Médias globais e custo-benefício:
- A transição inicial do mapeamento direto (1-way) para 2-way entrega o melhor custo-benefício prático, gerando o maior ganho isolado de IPC (+5,1%, saltando de 0.939 para 0.987) e uma queda brusca no tempo médio de execução, pois apenas duas vias já solucionam a maioria das colisões de endereço. A partir desse ponto, dobrar sucessivamente a complexidade do hardware de busca para 4, 8 e 16 vias revela-se sublinear: os ganhos de IPC despencam progressivamente para +2,3%, +2,1% e pífios +1,6%, com a redução extra de tempo tornando-se muito pequena após o 8-way. Isso indica que arquiteturas altamente associativas (como 16-way) aumentam drasticamente a complexidade física do chip para retornos práticos quase irrelevantes.

### 4.3. Tamanho do Fetch Buffer (8 a 64)

<img width="675" height="450" alt="Grafico_FetchBuffer_IPC" src="https://github.com/user-attachments/assets/fd0324f5-3cad-44cf-8cc3-7cf8a456c5e3" />

<img width="675" height="450" alt="Grafico_FetchBuffer_Tempo" src="https://github.com/user-attachments/assets/8b1396c8-345a-4795-8e50-4dcfb175410a" />

#### Matrix-Mult:
- **IPC:** Apresentou um salto expressivo ao expandir o buffer de 8 para 32 entradas. Como a multiplicação de matrizes possui laços longos e previsíveis com alto potencial de Paralelismo em Nível de Instrução (ILP), um buffer maior garante que o processador superescalar seja alimentado continuamente com instruções úteis. Acima de 32 entradas, o ganho estagna, indicando que a limitação passou a não ser mais a busca de instruções.
- **Tempo de Execução:** Obteve uma excelente redução acompanhando o crescimento do buffer até o limite de 32 posições. Ao evitar ociosidade aguardando novas instruções para decodificar, o processador maximiza o desempenho. A partir de 64 entradas, o tempo não apresenta mais melhorias.

#### FFT:
- **IPC:** Demonstrou um comportamento muito semelhante ao Matrix-Mult, destravando o ILP com grandes ganhos até a marca de 32 entradas. Sendo um algoritmo focado em processamento aritmético, o aumento do Fetch Buffer permitiu à CPU enfileirar e despachar múltiplas operações de ponto flutuante simultaneamente, saturando logo em seguida.
- **Tempo de Execução:** Exibiu uma queda notável e proporcional até estabilizar em 32 entradas. Com uma grande fila de instruções sempre disponíveis, o processador pôde decodificar e executar a matemática avançada da FFT de forma contínua, evitando a ociosidade e otimizando o tempo total.

#### BubbleSort:
- **IPC:** Permaneceu completamente inalterado e insensível às mudanças. O BubbleSort é guiado por laços curtos e comparações condicionais sucessivas. Essa estrutura gera frequentes falhas na predição de desvios, o que força a CPU a esvaziar o buffer de instruções constantemente. Portanto, anula-se totalmente a vantagem de buscar dezenas de instruções adiantadas se a maioria delas será descartada logo em seguida.
- **Tempo de Execução:** Manteve-se estagnado. O processador acaba desperdiçando ciclos preciosos apenas preenchendo e limpando um buffer gigantesco após cada erro de predição, o que não traz qualquer aceleração ou benefício prático para o tempo real da ordenação.

#### Médias globais custo-benefício:
- Dobrar a capacidade inicial de 8 para 16 entradas gerou um excelente custo-benefício, com o IPC médio saltando +8,3% (de 0.913 para 0.989) e o tempo de execução despencando proporcionalmente. Um novo dobro para 32 posições ainda entregou um ganho relevante de +3,8%, mas a saturação tornou-se evidente ao testar 64 entradas: o hardware de controle dobrou de tamanho, porém o ganho de IPC foi quase inexistente (+0,4%), formando um platô estagnado e perfeitamente reto no tempo de execução. Isso comprova que investir em uma fila gigantesca tem um péssimo custo-benefício se as unidades de execução (ALUs) ou a memória já não têm vazão para consumir tantas instruções simultâneas.

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## Contact

Leonardo Santos - <leorsantos2003@gmail.com>
