$(document).ready(function(){

});

var editableTable =
`
<table class="table table-striped">
    <thead>
        <tr>
            <th></th>
            <th class="add-cell">
                <form class="form-inline set-add-answer" onsubmit="return false;">
                    <div class="form-group">
                        <div class="input-group">
                            <div class="input-group-prepend">
                                <div class="input-group-text">Answer:</div>
                            </div>
                            <input class="form-control" type="text" name="name">
                            <div class="input-group-append">
                                <button type="submit" class="btn btn-success">Add</button>
                            </div>
                        </div>
                    </div>
                </form>
            </th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="add-cell">
                <form class="form-inline set-add-question" onsubmit="return false;">
                    <div class="form-group">
                        <div class="input-group">
                            <div class="input-group-prepend">
                                <div class="input-group-text">Question:</div>
                            </div>
                            <input class="form-control" type="text" name="name">
                            <div class="input-group-append">
                                <button type="submit" class="btn btn-success">Add</button>
                            </div>
                        </div>
                    </div>
                </form>
            </td>
        </tr>
    </tbody>
</table>
`;

var jObj = { questionnaire: [] };
var questionnaireData = jObj.questionnaire;

function qaSetAddAnswer(){
    //Get info from the form data
    var answerText = $(this).find("[name='name']").val();
    var setIndex = parseInt($(this).attr("data-set-index"));

    //Add row to table builder
    $(this).parent().before(`<th class="answer">${answerText}</th>`);

    //Add data to jObj
    var qaSet = questionnaireData[setIndex];
    if (!qaSet){
        qaSet = questionnaireData[setIndex] = {};
    }
    if (!qaSet["answers"]){
        qaSet["answers"] = [];
    }

    qaSet.answers.push(answerText);

    alert(JSON.stringify(questionnaireData));

    $(this).find("[name='name']").val(""); //Clear out name for ease of use
}

function qaSetAddQuestion(){
    var questionText = $(this).find("[name='name']").val();
    var setIndex = parseInt($(this).attr("data-set-index"));

    $(this).parent().parent().before(`<tr class="question"><td>${questionText}</td></tr>`);

    var qaSet = questionnaireData[setIndex];
    if (!qaSet){
        qaSet = questionnaireData[setIndex] = {};
    }
    if (!qaSet["questions"]){
        qaSet["questions"] = [];
    }

    qaSet.questions.push(questionText);

    alert(JSON.stringify(questionnaireData));

    $(this).find("[name='name']").val(""); //Clear out name for ease of use
}

var numSets = 0;
$("#addQaSet").submit(function(e){
    var setContainer = $(`<div class="qaSet"></div>`);
    setContainer.append(`<h2>${$(this).find("[name='name']").val()}</h2>`);

    var newEditableTable = $(editableTable).attr("id", "set" + numSets);

    newEditableTable.find(".set-add-answer").on("submit", qaSetAddAnswer).attr("data-set-index", numSets);
    newEditableTable.find(".set-add-question").on("submit", qaSetAddQuestion).attr("data-set-index", numSets);

    setContainer.append(newEditableTable);

    $("#questionnaire-form").append(setContainer);
    $(this).find("[name='name']").val(""); //Clear out name for ease of use

    numSets++;
});
