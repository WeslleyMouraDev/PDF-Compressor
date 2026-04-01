# PDF Compressor Premium 📂⚡

O **PDF Compressor Premium** é uma ferramenta desktop open-source rápida e avançada construída em Python (`CustomTkinter`) projetada especificamente para resolver um problema moderno: **Arquivos PDF gigantes originados de sistemas que exportam usando HTML2Canvas ou inúmeras imagens.**

Diferente de soluções online, este software roda 100% no seu Windows (Offline), não possui limites de envio (mesmo para arquivos > 400MB) e utiliza um motor matemático poderoso para entregar tamanhos inacreditáveis. 

## 🚀 Funcionalidades

- **Compressão Extrema:** Capaz de converter *400MB para menos de 40MB* com força bruta, forçando o recálculo progressivo das imagens internas via Ghostscript (`DCTEncode` a 72DPI Bicubic).
- **Sem Limites de MB ou Nuvem:** Todo o processamento dura de poucos segundos a poucos minutos ocorrendo localmente usando CPU Multithread.
- **Interface Dark Premium:** Desenvolvido puramente em *CustomTkinter* para uma experiência de janelas nativas, modernas, sem "travamentos" falsos e com barra indicadora de progresso em porcentagem real e ETA.

## 🛠️ Instalação Automática

1. Este Compressor utiliza o **Ghostscript** nativamente para espremer cada byte. **Por isso, antes de tudo, baixe e instale a dependência dele aqui:** [Download Ghostscript Windows](https://ghostscript.com/releases/gsdnld.html).
2. Clone este repositório `git clone https://github.com/WeslleyMouraDev/PDF-Compressor.git`.
3. Abra a pasta e dê dois cliques no arquivo `Inicializar.bat`. (Ele criará automaticamente o ambiente virtual leve e fará o download das bibliotecas do Python sem você precisar configurar nada!).
4. A interface aparecerá.

## 📦 Versão Executável (Portable .exe)

Pensando na melhor experiência, você também pode baixar diretamente o **Executável Premium** pré-compilado:

👉 [Acesse a Página Hotsite Oficial](https://weslleymouradev.github.io/PDF-Compressor/) e clique em "Baixar para Windows". 
*Nota: Mesmo com a versão EXE, o software requer que o Ghostscript esteja previamente instalado no Computador.*

## ⚙️ Modos de Compressão
* **Modo Leve (300dpi):** Otimiza a estrutura do PDF. Ideal para arquivos convencionais onde máxima qualidade original é necessária.
* **Modo Médio (150dpi - Ebook):** Equilibra nitidez perfeitamente com 50-70% de compressão em documentos padronizados ricos em fotos.
* **Modo Extremo (72dpi - JPEG DCTEncode):** Exclusivo para arquivos que incham em plataformas ou por causa do **HTML2Canvas**. Esse algoritmo não apenas cai a resolução pra 72DPI, mas força o re-encapsulamento de cada matriz colorida em compressão JPEG Bicúbica para destroçar o tamanho final (Reduções geralmente acima de 90% a 95%).

---
Feito de desenvolvedor para desenvolvedores ☕🚀
