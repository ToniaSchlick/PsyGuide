/* OBJECT */
function QuestionnaireBuilder(container){
    this.domContainer = $(container);
    this.domSetsContainer = this.domContainer.find(".question-sets-container");
    this.questionSets = [];
    this.scoringRanges = [];

    this.addQuestionSet = function(topic){
        var set = new QuestionSet(this, topic);
        this.domSetsContainer.append(set.domContainer);

        this.questionSets.push(set);
    };
    this.removeQuestionSet = function(questionSet){
        //Remove array elem by value
        this.questionSets = $.grep(this.questionSets, function(elem){
            return elem !== questionSet;
        });
    };

    this.addScoringRange = function(lowerBound, upperBound){

    };
    this.removeScoringRange = function(scoringRange){
        //Remove array elem by value
        this.scoringRanges = $.grep(this.scoringRanges, function(elem){
            return elem !== scoringRange;
        });
    };

    this.compileJson = function(){
        return {
            "name": this.domContainer.find("#questionnaire-name").val(),
            "questionSets": this.questionSets.map(set => set.compileJson())
        };
    };
}

/* OBJECT */
function ScoringRange(){
    this.domContainer = scoringRangeContainer.clone();

}

/* OBJECT */
function QuestionSet(questionnaire, topic){
    this.questionnaire = questionnaire;
    this.domContainer = questionSetContainer.clone();
    this.domTable = this.domContainer.find(`table`);

    this.domContainer.find(`.topic`).text(topic);

    this.topic = topic;
    this.scored = true;
    this.questions = [];
    this.answers = [];

    //Bind event listeners
    var that = this;
    this.domContainer.find(`input[type="checkbox"][name="scored"]`)
        .on("change", function(){ that.scored = this.checked; });
    this.domTable.find(".set-add-answer").on("submit", function(){
        that.addAnswer($(this).find("[name='name']").val());
        $(this).find("[name='name']").val("");
    });
    this.domTable.find(".set-add-question").on("submit", function(){
        that.addQuestion($(this).find("[name='name']").val());
        $(this).find("[name='name']").val("");
    });
    this.domContainer.find(".set-delete").on("click", function(){
        that.remove();
    });

    this.addAnswer = function(answerText){
        this.answers.push(answerText);

        var answerCell = $(`
            <th class="fit">
                <button class="btn btn-warning set-remove-answer">X</button>
                <span class="answer">${answerText}</span>
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
        console.log(this.answers.length);
        //Remove array elem by value
        this.answers = $.grep(this.answers, function(elem){
            return elem !== answer;
        });
        console.log(this.answers.length);
    };

    this.addQuestion = function(questionText){
        this.questions.push(questionText);

        var questionRowElem = $(`
            <tr><td>
                <button class="btn btn-warning set-remove-question">X</button>
                <span class="question">${questionText}</span>
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
        console.log(this.questions.length);
        //Remove array elem by value
        this.questions = $.grep(this.questions, function(elem){
            return elem !== question;
        });
        console.log(this.questions.length);
    };

    this.compileJson = function(){
        return {
            "topic": this.topic,
            "scored": this.scored,
            "questions": this.questions,
            "answers": this.answers
        };
    };

    this.remove = function(){
        this.questionnaire.removeQuestionSet(this);
        this.domContainer.remove();
    };
}

var mainContainer = $("#questionnaire-builder");
var mainBuilder = new QuestionnaireBuilder(mainContainer);

$(".add-question-set").submit(function(e){
    var setName = $(this).find("[name='name']").val();
    mainBuilder.addQuestionSet(setName);

    //Clear out name so it can be typed in again
    $(this).find("[name='name']").val("");
});
