# Syuzhet web service

## Introduction
This document explains how to use the Syuzhet web api.

## Endpoints
The API exposes the following endpoints:

-   [https://syuzhet-web.herokuapp.com/](https://syuzhet-web.herokuapp.com/): main entry point where you can find this help;
-   [https://syuzhet-web.herokuapp.com/analyze](https://syuzhet-web.herokuapp.com/analyze): RESTFul endpoint to analyze a text, must send a POST request with JSON content (see below for an example);
-   [https://syuzhet-web.herokuapp.com/gui-test](https://syuzhet-web.herokuapp.com/gui-test): sample implementation of a GUI;

## Request format
The service accepts JSON data within an HTTP POST request.
The JSON data should have the following fields:

-   id: a number identifying the id of the sent text
-   corpus: will be returned as is
-   document: will be returned as is
-   content (**required**): the text to analyze


```javascript
{
    "id": number,
    "corpus": "name_of_corpus",
    "document": "name_of_document",
    "content": "Text of the document..."
}
```

**Warning**:

The only true required field of the request is the `content` field that defines the text to analyze. All other fields are irrelevant (at the moment).

### Example request
Here is a sample request object,

```javascript
{
    "id": 13,
    "corpus": "paziente X",
    "document": "Diario del giorno 22/03/2017",
    "content": "Stamattina mi sono svegliato con un gran mal di testa.\nCi sono voluti venti minuti per..."
}
```

and here is jQuery code to analyze a text

```javascript
// IMPORTANT! make a JSON string from the content of a JSON object
data_to_send = JSON.stringify({"content": "Text to analyze..."})

// use jQuery $.ajax to send and receive async requests
$.ajax({
    url: 'https://syuzhet-web.herokuapp.com/analyze',
    cache: false,
    type: 'POST', // don't forget this!
    data : data_to_send,
    contentType: 'application/json; charset=utf-8', // don't forget this!
    dataType: 'json',
    success: function(json_response) {
        // client code to execute in case of success
    },
    error: function(request, textStatus, errorThrown) {
        // client code to execute in case of error
    }
});
```

## Response format
The service will answer with a JSON formatted as follows:

```javascript
{
    "id": number, // if present in request
    "corpus": "the corpus name", // if present in request
    "document": "the document name", // if present in request
    "emotion-names": [array of Strings mapping the emotion names],
    "result": {
        "aggregate": [array of 10 values, one for each emotion],
        "sentences": [[10 values for sentence 1],
                                [10 values for sentence 2],
                                [10 values for sentence 3], ...]
    }
}
```

### Notes
At the moment, the API only outputs the aggregate and the per-sentence value of the 10 emotions. More options will come, along with more useful output (postprocessed output like Fourier...whatever!).
