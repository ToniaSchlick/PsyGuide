$(document).ready(function(){
    var questionnaire = qData.questionnaire;
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
            var qaRow = $("<tr></tr>");
            qaRow.append($("<td>" + qaSet.questions[qIndex] + "</td>"));

            //Add checkbox for every possible response.
            for (var aIndex = 0; aIndex < qaSet.answers.length; aIndex++){
                qaRow.append($('<td class="fit"><input type="radio" name="s' + qaSetIndex + 'q' + qIndex + '" value="' + aIndex + '"></td>'));
            }
            qaRow.appendTo(qaSetTable);
        }

        qaSetTable.appendTo($("#questionnaire-form"));
    }

    $("#loading").hide();
});
