# Syuzhet web service

## Introduction
This document explains how to use the Syuzhet web api.

## Endpoints
The API exposes the following endpoints:

-   [https://syuzhet-web.herokuapp.com/](https://syuzhet-web.herokuapp.com/): main entry point where you can find this help;
-   [https://syuzhet-web.herokuapp.com/analyze](https://syuzhet-web.herokuapp.com/analyze): RESTFul endpoint to analyze a text, must send a POST request with JSON content (see below for an example);
-   [https://syuzhet-web.herokuapp.com/gui-test](https://syuzhet-web.herokuapp.com/gui-test): sample implementation of a GUI;
-   [https://syuzhet-web.herokuapp.com/lemmatize](https://syuzhet-web.herokuapp.com/lemmatize): lemmatization service;

## Request format for Lemmatization only
The service accepts JSON data within an HTTP POST request.
The JSON shall have the mandatory field `text` (String) and the optional field `delete_stopwords` (boolean, defaults to **true**).

An example request is:

```javascript
{
	"text": "Questo è il testo da lemmatizzare.
	Dovresti ritornarlo con i lemmi soltanto, grazie.
	Inoltre, fammi un piacere, scrivi a Link-up che ho messo
	online il lemmatizzatore.",
	"delete_stopwords": true
}
```

The response is a JSON that **only** contains the lemmatized sentences, under the key `sentences`. It is an array where each element is an array of strings, representing a lemmatized sentence.

The response for the request shown above is:

```javascript
{
    "sentences": [
        [
            "essere",
            "testo",
            "lemmatizzare"
        ],
        [
            "dovere",
            "ritornare",
            "lemma",
            "soltanto",
            "grazie"
        ],
        [
            "inoltre",
            "fare",
            "piacere",
            "scrivere",
            "link-up",
            "avere",
            "mettere",
            "online",
            "lemmatizzatore"
        ]
    ]
}
```

## Request format
The service accepts JSON data within an HTTP POST request.
The JSON data should have the following fields:

-   content (**required**): the text to analyze
-   postprocessing: boolean indicating wether to return post-processed harmonics too (see section [Harmonics postprocessing](#harmonics-postprocessing)); you should choose the number of harmonics you want with the "number\_of_harmonics" field (default is [5, 10, 15, 20])
-   number\_of_harmonics: integer or Array of integer values specifying the number of harmonics you want for postprocessing.


```javascript
{
    "content": "Text of the document..."
    "postprocessing": boolean,
    "number_of_harmonics": integer > 0 or Array[integer > 0]
}
```

### Example request
Here is a sample request object,

```javascript
{
	"content": "Stamattina mi sono svegliato con un gran mal di testa.\nCi sono voluti venti minuti per...",
	"postprocessing": true,
	"number_of_harmonics": [2, 5, 10]  // override the default
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
    "text_id": integer number, // id to use to refer to the same text in subsequent calls.
    "emotion-names": [array of Strings mapping the emotion names],
    "result": {
        "aggregate": [array of 10 values, one for each emotion],
        "emotions": {"emotion_1": [values of emotion_1 in each sentence],
			         "emotion_2": [values of emotion_2 in each sentence],
                     ...
                     },
	    "harmonics": {"5": {
	    					"emotion_1": [values of harmonics for emotion_1],
	    					"emotion_1": [values of harmonics for emotion_2],
	    					...
	    					},
	    			  "10": {
	    					"emotion_1": [values of harmonics for emotion_1],
	    					"emotion_1": [values of harmonics for emotion_2],
	    					...
	    					}
	    				}
	    }
}
```

**Note**: the `harmonics` field will be present only if requested in the request.

## Harmonics postprocessing
There are two ways to get post-processed data from the service:

1. set the "postprocessing" flag to true in the request and specify the number of harmonics you want
2. make a POST request to the `/postprocess` endpoint. The request **must** contain:
	- the id of the text as returned by the service when it was analyzed
	- the number of harmonics you want as a single integer or integer array

For example, let's say that you analyzed a text and its `id` is 2459. A request to get 10, 20 and 100 harmonics would be:

```javascript
{
	"text_id": 2459,
	"number_of_harmonics": [10, 20, 100]
}
```

The response will look like:

```javascript
{
	"text_id": 2459,
	"harmonics":
		{"10":
			{"emotion_name_1": [array of values...],
			 "emotion_name_2": [array of values...],
			 ...},
		 "20":
		 	{"emotion_name_1": [array of values...],
			 "emotion_name_2": [array of values...],
			 ...},
		 "100":
		 	{"emotion_name_1": [array of values...],
			 "emotion_name_2": [array of values...],
			 ...}
		}
}
```
