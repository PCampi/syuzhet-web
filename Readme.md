# Syuzhet web service

## Introduction
This document explains how to use the Syuzhet web api.

## Request format
The service accepts JSON data within an HTTP POST request.
The JSON data should have the following fields:

-   id (**required**): a number identifying the id of the sent text
-   corpus: will be returned as is
-   document: will be returned as is
-   contents (**required**) : the text to analyze


```javascript
{
    "id": number,
    "corpus": "name_of_corpus",
    "document": "name_of_document",
    "contents": "Text of the document..."
}
```

**Warning**:

The only true required field of the request is the `contents` field that defines the text to analyze. All other fields are irrelevant (at the moment).


Here is a sample request:

```javascript
{
    "id": 13,
    "corpus": "paziente X",
    "document": "Diario del giorno 22/03/2017",
    "contents": "Stamattina mi sono svegliato con un gran mal di testa.\nCi sono voluti venti minuti per..."
}
```


## Response format
The service will answer with a JSON formatted as follows:

```javascript
{
    "id": number,
    "corpus": "the corpus name",
    "document": "the document name",
    "results": {
        "emotion-names": [array of Strings mapping the emotion names],
        "aggregate": [array of 10 values, one for each emotion],
        "emotions-for-sentence": [[10 values for sentence 1],
                                [10 values for sentence 2],
                                [10 values for sentence 3], ...]
    }
}
```

### Notes
At the moment, the API only outputs the aggregate and the per-sentence value of the 10 emotions. More options will come, along with more useful output (postprocessed output like Fourier...whatever!).
