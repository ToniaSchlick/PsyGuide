# Models

Questionnaires and their responses are handled by discrete models and the Django persistence layer.  They are then shown to the end user via templates that iterate through these objects and build the end HTML.

Each questionnaire object has a corresponding response object, so that duplicate data can be avoided.  Response objects are simply foreign key related dummy objects with supporting functions that call into the respective questionnaire object.

The base questionnaire models are as follows:
```text
Questionnaire       # Parent object for questionnaire storage
    QuestionSet     # Set of questions+answers with a topic
        Question    # Single question with text and an ordinal
        Answer      # Single answer with text and an ordinal
    ScoringFlag     # Used to signal that some scoring condition was met
```

And their corresponding response objects:
```text
QuestionnaireResponse       # Parent object for response storage
    QuestionSetResponse     # Set of QuestionResponse objects related to a set
        QuestionResponse    # Singular response, foreign key to question and answer
```

# Editing

Editing is handled by the ```edit(request)``` function in the ```questionnaire/views.py``` file.

Editing a questionnaire is somewhat complicated.  There isn't one form that is used, as a questionnaire is built out of many models linked together by foreign keys.  Therefore when editing the questionnaire data is sent to the end user by instantiating a JavaScript Questionnaire object defined in ```/static/js/questionnaire.js```.  The JavaScript used to create the instance is generated in the ```questionnaire/edit.html``` template on-the-fly from the questionnaire object passed in by the view.

When done, the client sends back the questionnaire in JSON form in ```POST["questionnaire"]```.  This JSON is then parsed and traversed in order to modify existing, create new and prune removed questionnaire elements from the persistence layer.

# Viewing/Administering

Viewing is handled by the ```view(request)``` function in the ```questionnaire/views.py``` file.

Viewing is quite simple.  The ```questionnaire``` object is passed to the view through the context, then the view.html template takes care of showing all components.

Administering is handled by the ```administer(request)``` function in the ```questionnaire/views.py``` file.

Administering is just like viewing, except the form data is taken and compiled to a JSON object in JavaScript that is then passed back to the view function through POST, then the view takes care of creating response objects that represent the JSON with Django persistent objects.
