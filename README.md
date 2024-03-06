# Chatbot para Arline Travel Information System (ATIS) - IF144 Processamento de Linguagem Natural

## Sobre o Projeto

Este projeto foi desenvolvido como parte da disciplina IF144 - Processamento de Linguagem Natural, do curso de Ciência da Computação na Universidade Federal de Pernambuco (UFPE). O objetivo é construir um chatbot focado em um domínio específico. No nosso caso, escolhemos [um conjunto de ATIS](https://github.com/howl-anderson/ATIS_dataset) disponível publicamente. 

## Funcionalidades

O chatbot é capaz de:
- Classificar intenções e extrair informações específicas das perguntas dos usuários.
- Responder a perguntas relacionadas a voos, utilizando um modelo de Q&A.

## Tecnologias Utilizadas

- **Classificador**: Bag-of-Words com SVM, CNN, LSTM, e Transformers.
- **Extrator**: LSTM e Transformers.
- **Chatbot**: Rasa.
- **Q&A**: Typesense.
- Também conectamos com a API da OpenAI para poder responder perguntas relacionadas à intenção `atis_abbreviation`.

## Esquema do Modelo de Conversa

O nosso chatbot construído com o auxílio do Rasa segue o seguinte fluxo de conversação:

![Esquema do Modelo de Conversa](chat_flow.png)
