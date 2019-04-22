/* OBJECT */
function Questionnaire(container, pk=-1){
    this.pk = pk;

    this.domContainer = $(container);
    this.domSetsContainer = this.domContainer.find(".question-sets-container");
    this.domScoringFlagsContainer = this.domContainer.find(".scoring-flags-container");

    var that = this;
    this.domContainer.find(".add-scoring-flag").on("click", function(e){
        that.addScoringFlag();
    });

    this.questionSets = [];
    this.scoringFlags = [];

    this.addQuestionSet = function(topic, scored=true, pk=-1){
        var set = new QuestionSet(this, topic, scored, pk);
        this.domSetsContainer.append(set.domContainer);
        this.questionSets.push(set);

        return set;
    };
    this.removeQuestionSet = function(questionSet){
        this.questionSets = array_remove(this.questionSets, questionSet);
    };

    this.addScoringFlag = function(expression, title, description, pk=-1){
        var flag = new ScoringFlag(this, expression, title, description, pk);
        this.scoringFlags.push(flag);

        this.domScoringFlagsContainer.append(flag.domContainer);

        return flag;
    };
    this.removeScoringFlag = function(scoringFlag){
        this.scoringFlags = array_remove(this.scoringFlags, scoringFlag);
    };

    this.compileJson = function(){
        return {
            "pk": this.pk,
            "name": this.domContainer.find("#questionnaire-name").val(),
            "questionSets": this.questionSets.map(set => set.compileJson()),
            "scoringFlags": this.scoringFlags.map(flag => flag.compileJson())
        };
    };
}

/* OBJECT */
function ScoringFlag(questionnaire, expression, title, description, pk=-1){
    this.pk = pk;

    this.domContainer = scoringFlagContainer.clone();
    this.questionnaire = questionnaire;

    this.domContainer.find("[name=flag-expression]").val(expression);
    this.domContainer.find("[name=flag-title]").val(title);
    this.domContainer.find("[name=flag-description]").val(description);

    //Bind event listeners.
    var that = this;
    this.domContainer.find(".flag-delete").on("click", function(){
        that.remove();
    });

    this.remove = function(){
        this.questionnaire.removeScoringFlag(this);
        this.domContainer.remove();
    };

    this.compileJson = function(){
        return {
            "pk": this.pk,
            "expression": this.domContainer.find("[name=flag-expression]").val(),
            "title": this.domContainer.find("[name=flag-title]").val(),
            "description": this.domContainer.find("[name=flag-description]").val()
        };
    };
}

/* OBJECT */
function QuestionSet(questionnaire, topic, scored=true, pk=-1){
    this.pk = pk;

    this.questionnaire = questionnaire;
    this.domContainer = questionSetContainer.clone();
    this.domTable = this.domContainer.find(`table`);

    this.domContainer.find(`.topic`).prepend(topic);

    this.topic = topic;
    this.scored = scored;
    this.questions = [];
    this.answers = [];

    this.domContainer.find(`input[name="scored"]`).attr("checked", scored);

    //Bind event listeners
    var that = this;
    this.domContainer.find(`input[name="scored"]`)
        .on("change", function(){ that.scored = this.checked; });
    this.domTable.find(".set-add-answer").on("submit", function(){
        var answerInput = $(this).find("[name='answer-text']");

        that.addAnswer(answerInput.val());
        answerInput.val("");
    });
    this.domTable.find(".set-add-question").on("submit", function(){
        var questionInput = $(this).find("[name='question-text']");

        that.addQuestion(questionInput.val());
        questionInput.val("");
    });
    this.domContainer.find(".set-delete").on("click", function(){
        that.remove();
    });

    this.addAnswer = function(answerText, pk){
        var answer = new Answer(this, answerText, pk);

        this.answers.push(answer);

        //Append header cell to the answer row
        this.domTable
            .find("thead>tr>th:last-child")
            .before(answer.domContainer);

        this.updateDisplay();
    };
    this.removeAnswer = function(answer){
        this.answers = array_remove(this.answers, answer);

        this.updateDisplay();
    };

    this.addQuestion = function(questionText, pk){
        var question = new Question(this, questionText, pk);

        this.questions.push(question);

        //Append the new question row to the table
        this.domTable.find("tbody>tr:last-child").before(question.domContainer);

        this.updateDisplay();
    };
    this.removeQuestion = function(question){
        this.questions = array_remove(this.questions, question);

        this.updateDisplay();
    };

    this.updateDisplay = function(){
        this.questions.forEach((question, i) => {
            question.updateRadios();
            question.setNumber(i + 1);
        });

        this.answers.forEach((answer, i) => {
            answer.setNumber(i);
        });
    };

    this.remove = function(){
        this.questionnaire.removeQuestionSet(this);
        this.domContainer.remove();
    };

    this.compileJson = function(){
        return {
            "pk": this.pk,
            "topic": this.topic,
            "scored": this.scored,
            "questions": this.questions.map(question => question.compileJson()),
            "answers": this.answers.map(answer => answer.compileJson())
        };
    };
}

/* OBJECT */
function Question(questionSet, text, pk=-1){
    this.pk = pk;

    this.domContainer = questionRow.clone();
    this.questionSet = questionSet;

    //Set text of generic container clone
    this.domContainer.find(".question").text(text);
    this.domContainer.find(".number").text(this.questionSet.questions.length + 1);


    // Bind events
    var that = this;
    this.domContainer.find(".question").on("click", function(){
        var newText = prompt("Enter new question text");

        if (newText === null || newText === ""){
            return;
        }

        that.setText(newText);
    });
    this.domContainer.find(".set-remove-question").on("click", function(){
        that.remove();
    });

    this.updateRadios = function(){
        if (this.domContainer.find(".dummy-radio-cell").length
            == this.questionSet.answers.length){
            return;
        }

        //Remove existing radio cells
        this.domContainer.find(".dummy-radio-cell").remove();

        //Append new radio cell for each answer
        for (var answer in this.questionSet.answers){
            this.domContainer.append(dummyRadioCell.clone());
        }
    };

    this.updateRadios();

    this.setText = function(text){
        this.domContainer.find(".question").text(text);
    };

    this.setNumber = function(number){
        this.domContainer.find(".number").text(number);
    };

    this.remove = function(){
        this.questionSet.removeQuestion(this);
        this.domContainer.remove();
    };

    this.compileJson = function(){
        return {
            "pk": this.pk,
            "text": this.domContainer.find(".question").text()
        };
    };
}

/* OBJECT */
function Answer(questionSet, text, pk=-1){
    this.pk = pk;

    this.domContainer = answerCell.clone();
    this.questionSet = questionSet;

    this.domContainer.find(".answer").text(text);
    this.domContainer.find(".number").text(this.questionSet.answers.length);

    // Bind events
    var that = this;
    this.domContainer.find(".answer").on("click", function(){
        var newText = prompt("Enter new answer text");

        if (newText === null || newText === ""){
            return;
        }

        that.setText(newText);
    });
    this.domContainer.find(".set-remove-answer").on("click", function(){
        that.remove();
    });

    this.setText = function(text){
        this.domContainer.find(".answer").text(text);
    };

    this.setNumber = function(number){
        this.domContainer.find(".number").text(number);
    };

    this.remove = function(){
        this.questionSet.removeAnswer(this);
        this.domContainer.remove();
    };

    this.compileJson = function(){
        return {
            "pk": this.pk,
            "text": this.domContainer.find(".answer").text()
        };
    };
}


/*
    Helper function to remove a specific element from an array

    Used in remove* methods of questionnaire* objects
*/
function array_remove(array, element){
    return $.grep(array, function(elem){
        return elem !== element;
    });
}
