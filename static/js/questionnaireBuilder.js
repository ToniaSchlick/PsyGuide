/* OBJECT */
function QuestionnaireBuilder(){
    this.domContainer = $(`<div class="questionnaire"></div>`)
    this.addQaSet = function(topic){
        var set = new QuestionAnswerSet(topic)
        this.domContainer.append(`<h2>${topic}</h2>`);
        this.domContainer.append(set.domTable);
    }
}

/* OBJECT */
function QuestionAnswerSet(topic){
    this.domTable = editableTable.clone();
    this.topic = topic;
    this.questions = [];
    this.answers = [];

    //Add event listeners to addforms
    var that = this;
    this.domTable.find(".set-add-answer").on("submit", function(){
        that.addAnswer($(this).find("[name='name']").val());
        $(this).find("[name='name']").val("");
    });
    this.domTable.find(".set-add-question").on("submit", function(){
        that.addQuestion($(this).find("[name='name']").val());
        $(this).find("[name='name']").val("");
    });

    this.addAnswer = function(answerText){
        this.answers.push(answerText);
        this.domTable.find("thead>tr>th:last-child").before(`<th class="answer">${answerText}</th>`);

        //Append another dummy radio to each question row for the new answer
        this.domTable.find("tbody>tr:not(:last-child)").append(`<td class="fit"><input type="radio" checked></td>`)
    };

    this.addQuestion = function(questionText){
        this.questions.push(questionText);
        var questionRowElem = $(`<tr class="question"><td>${questionText}</td></tr>`);
        this.domTable.find("tbody>tr:last-child").before(questionRowElem);

        //Add dummy radio for each possible answer
        for (var i = 0; i < this.answers.length; i++){
            questionRowElem.append(`<td class="fit"><input type="radio" checked></td>`);
        }
    };

    this.compileJson = function(){

    };
}

var mainBuilder = new QuestionnaireBuilder();

$("#addQaSet").submit(function(e){
    mainBuilder.addQaSet($(this).find("[name='name']").val());

    $("#questionnaire-form").append(mainBuilder.domContainer);

    $(this).find("[name='name']").val(""); //Clear out name for ease of use
});
