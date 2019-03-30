/* OBJECT */
function QuestionnaireBuilder(){
    this.domContainer = $(`<div class="questionnaire"></div>`)
    this.qaSets = [];

    this.addQaSet = function(topic){
        var set = new QuestionAnswerSet(topic)
        this.domContainer.append(set.domContainer);

        this.qaSets.push(set);
    };
}

/* OBJECT */
function QuestionAnswerSet(topic){
    this.domContainer = qaContainer.clone();
    this.domTable = this.domContainer.find(`table`);

    var that = this;
    this.domContainer.find(`.topic`).text(topic);
    this.domContainer.find(`input[type="checkbox"][name="scored"]`).on("change", function(){
        that.setScored(this.checked);
    });

    this.topic = topic;
    this.questions = [];
    this.answers = [];
    this.scored = false;

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

    this.setScored = function(scored){
        this.scored = scored;
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
