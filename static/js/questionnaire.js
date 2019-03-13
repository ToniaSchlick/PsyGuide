$(document).ready(function(){
    loadQuestionnaire();

    $("#loading").hide();
});

function loadQuestionnaire(){
    for (var qaSetIndex in questionnaire){
        var qaSet = questionnaire[qaSetIndex];

        //Check for topic header before
        if ('topic' in qaSet){
            $("#questionnaire-form").append("<h2>" + qaSet.topic + "</h2>");
        }

        var qaSetTable = $("<table class='table table-striped'></table>");

        //Load answers for table header
        var answerRow = $("<tr></tr>");
        answerRow.append($("<th></th>")); //Blank cell over question
        for (var a = 0; a < qaSet.answers.length; a++){
            answerRow.append($("<th class='fit'>" + qaSet.answers[a] + "</th>"));
        }
        answerRow.appendTo(qaSetTable);

        //Load in questions row by row
        for (var qIndex = 0; qIndex < qaSet.questions.length; qIndex++){
            var qaRow = $("<tr class='question-row'></tr>");
            qaRow.append($("<td>" + qaSet.questions[qIndex] + "</td>"));

            //Add checkbox for every possible response.
            for (var aIndex = 0; aIndex < qaSet.answers.length; aIndex++){
                //Tag radio with set number and question number for parsing later.
                qaRow.append($('<td class="fit response-radio"><input type="radio" name="s' + qaSetIndex + 'q' + qIndex + '" value="' + aIndex + '"></td>'));
            }
            qaRow.appendTo(qaSetTable);
        }

        qaSetTable.appendTo($("#questionnaire-form"));
    }
}

$("#background-form").on("submit", function(e){
    var jObj = { response: {} };
    var response = jObj.response;

    var errorFound = false;
    $("#questionnaire-form .question-row").each(function(){
        var selectedRadio = $(this).find("input[type='radio']:checked");


        if (selectedRadio.length){
            var radioName = selectedRadio.attr("name");
            var radioVal = selectedRadio.attr("value");

            var setNum = radioName.match(/^s(\d+)/)[1];

            if (!response[setNum]){
                response[setNum] = [];
            }

            response[setNum].push(radioVal);


            $(this).removeClass("alert-danger");
        }
        else {
            errorFound = true;
            $(this).addClass("alert-danger");
        }
    });



    if (!errorFound){
        $(this).find("[name='qrData']").attr("value", JSON.stringify(jObj));
    }
});
