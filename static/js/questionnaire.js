/* OBJECT */
function Questionnaire(container){
    this.domContainer = $(container);
    this.domSetsContainer = this.domContainer.find(".question-sets-container");
    this.domScoringFlagsContainer = this.domContainer.find(".scoring-flags-container");

    var that = this;
    this.domContainer.find(".add-scoring-flag").on("click", function(e){
        that.addScoringFlag();
    });

    this.questionSets = [];
    this.scoringFlags = [];

    this.addQuestionSet = function(topic){
        var set = new QuestionSet(this, topic);
        this.domSetsContainer.append(set.domContainer);
        this.questionSets.push(set);

        return set;
    };
    this.removeQuestionSet = function(questionSet){
        this.questionSets = array_remove(this.questionSets, questionSet);
    };

    this.addScoringFlag = function(expression, title, description){
        var flag = new ScoringFlag(this, expression, title, description);
        this.scoringFlags.push(flag);

        this.domScoringFlagsContainer.append(flag.domContainer);

        return flag;
    };
    this.removeScoringFlag = function(scoringFlag){
        this.scoringFlags = array_remove(this.scoringFlags, scoringFlag);
    };

    this.compileJson = function(){
        return {
            "name": this.domContainer.find("#questionnaire-name").val(),
            "questionSets": this.questionSets.map(set => set.compileJson()),
            "scoringFlags": this.scoringFlags.map(flag => flag.compileJson())
        };
    };
}

/* OBJECT */
function ScoringFlag(questionnaire, expression, title, description){
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
            "expression": this.domContainer.find("[name=flag-expression]").val(),
            "title": this.domContainer.find("[name=flag-title]").val(),
            "description": this.domContainer.find("[name=flag-description]").val()
        };
    };
}

/* OBJECT */
function QuestionSet(questionnaire, topic){
    this.questionnaire = questionnaire;
    this.domContainer = questionSetContainer.clone();
    this.domTable = this.domContainer.find(`table`);

    this.domContainer.find(`.topic`).prepend(topic);

    this.topic = topic;
    this.scored = true;
    this.questions = [];
    this.answers = [];

    //Bind event listeners
    var that = this;
    this.domContainer.find(`input[type="checkbox"][name="scored"]`)
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

    this.addAnswer = function(answerText){
        this.answers.push(answerText);

        var answerCell = $(`
            <th class="fit">
                <button class="btn btn-warning set-remove-answer">X</button>
                <b>${this.answers.length - 1}: </b>
                <span class="question">${answerText}</span>
            </th>
        `);

        //Bind remove event listener
        var that = this;
        answerCell.find(".set-remove-answer").on("click", function(){
            var answer = $(this).parent().find(".answer").text();
            that.removeAnswer(answer);

            //Remove dummy radios
            $(this).closest("table")
                .find("tbody>tr:not(:last-child)>td:last-child").remove();

            //Remove answer cell
            $(this).closest("th").remove();
        });

        //Append header cell to the answer row
        this.domTable
            .find("thead>tr>th:last-child")
            .before(answerCell);

        //Append another dummy radio to each question row for the new answer
        this.domTable
            .find("tbody>tr:not(:last-child)")
            .append(`<td class="fit"><input type="radio" checked></td>`);
    };
    this.removeAnswer = function(answer){
        this.answers = array_remove(this.answers, answer);
    };

    this.addQuestion = function(questionText){
        this.questions.push(questionText);

        var questionRowElem = $(`
            <tr><td>
                <button class="btn btn-warning set-remove-question">X</button>
                <b>${this.questions.length}. </b><span class="question">${questionText}</span>
            </td></tr>
        `);

        //Bind remove event
        var that = this;
        questionRowElem.find(".set-remove-question").on("click", function(){
            var question = $(this).parent().find(".question").text();
            that.removeQuestion(question);
            $(this).closest("tr").remove();
        });

        //Add dummy radio for each possible answer
        for (var i = 0; i < this.answers.length; i++){
            questionRowElem
                .append(`<td class="fit"><input type="radio" checked></td>`);
        }

        //Append the new question row to the table
        this.domTable.find("tbody>tr:last-child").before(questionRowElem);
    };
    this.removeQuestion = function(question){
        this.questions = array_remove(this.questions, question);
    };

    this.remove = function(){
        this.questionnaire.removeQuestionSet(this);
        this.domContainer.remove();
    };

    this.compileJson = function(){
        return {
            "topic": this.topic,
            "scored": this.scored,
            "questions": this.questions,
            "answers": this.answers
        };
    };
}




var mainContainer = $("#questionnaire-builder");
var mainQuestionnaire = new Questionnaire(mainContainer);

$(".add-question-set").submit(function(e){
    var topicInput = $(this).find("[name='set-topic']");

    var setName = topicInput.val();
    mainQuestionnaire.addQuestionSet(setName);

    //Clear out name so it can be typed in again
    topicInput.val("");
});

$("#data-form").on("submit", function(){
    var jsonString = JSON.stringify(mainQuestionnaire.compileJson());
    //alert(jsonString);
    $(this).append($(`<input type="text" name="questionnaire" hidden>`).attr("value", jsonString));
});


function array_remove(array, element){
    return $.grep(array, function(elem){
        return elem !== element;
    });
}
