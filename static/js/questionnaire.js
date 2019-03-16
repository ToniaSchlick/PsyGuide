function loadQuestionnaire(jsonObject, targetContainer){
    var questionnaire = jsonObject.questionnaire;

    for (var qaSetIndex in questionnaire){
        var qaSet = questionnaire[qaSetIndex];

        //Check for topic header before
        if ('topic' in qaSet){
            $(targetContainer).append(`<h2>${qaSet.topic}</h2>`);
        }

        var qaSetTable = $(`<table class='table table-striped' data-set-index='${qaSetIndex}'></table>`);

        //Load answers for table header
        var answerRow = $("<tr></tr>");
        answerRow.append($("<th></th>")); //Blank cell over question
        for (var a = 0; a < qaSet.answers.length; a++){
            answerRow.append($(`<th class='fit'>${qaSet.answers[a]}</th>`));
        }
        answerRow.appendTo(qaSetTable);

        //Load in questions row by row
        for (var qIndex = 0; qIndex < qaSet.questions.length; qIndex++){
            var qaRow = $("<tr class='question-row'></tr>");
            qaRow.append($(`<td>${qaSet.questions[qIndex]}</td>`));

            //Add checkbox for every possible response.
            for (var aIndex = 0; aIndex < qaSet.answers.length; aIndex++){
                //Tag radio with set number and question number for parsing later.
                qaRow.append($(`<td class="fit"><input type="radio" name="s${qaSetIndex}q${qIndex}" data-set-index="${qaSetIndex}" data-qindex="${qIndex}" data-answer-index="${aIndex}" value="${aIndex}"></td>`));
            }
            qaRow.appendTo(qaSetTable);
        }

        //Append to container last after everything is added to stop unnecessary redraws
        qaSetTable.appendTo($(targetContainer));
    }
}

function loadResponse(jsonObject, targetContainer){
    //Lock all inputs in container
    $(targetContainer).find("input[type=radio]").attr("disabled", true);

    //TODO: Iterate over table successively, avoid searching entire form to find radio inputs
    var response = jsonObject.response;
    for (var setIndex = 0; setIndex < response.length; setIndex++){
        var questions = response[setIndex];
        for (var qIndex = 0; qIndex < questions.length; qIndex++){
            $(targetContainer).find(`input[type=radio][data-set-index=${setIndex}][data-qindex=${qIndex}][data-answer-index=${questions[qIndex]}]`).attr("disabled", false).attr("checked", true);
        }
    }
}

$("#background-form").on("submit", function(e){
    var jObj = { response: {} };
    var response = jObj.response = [];

    var allFilledOut = true;
    $("#questionnaire-form .question-row").each(function(){
        //Find selected response
        var selectedRadio = $(this).find("input[type=radio]:checked");
        if (selectedRadio.length){
            var setNum = selectedRadio.attr("data-set-index");
            var radioVal = selectedRadio.attr("value");

            if (!response[setNum]){
                response[setNum] = [];
            }
            response[setNum].push(radioVal);

            //Question filled out, reset alert
            $(this).removeClass("alert-danger");
        }
        else {
            allFilledOut = false;

            //Set alert class to notify user to
            $(this).addClass("alert-danger");
        }
    });

    if (allFilledOut){
        $("#alert-container").hide();
        $(this).find("[name='qrData']").attr("value", JSON.stringify(jObj));
    }
    else {
        //Show fill out notice
        $("#alert-container").show();

        //Scroll page back to top of questionnaire to fill out missed
        $('html').animate({
            scrollTop: 0
        }, 500);
    }

    return allFilledOut;
});
