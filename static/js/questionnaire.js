/* OBJECT */
function Questionnaire(jsonData, dataForm){
    this.questionnaireJson = jsonData.questionnaire;
    this.scoringJson = jsonData.scoring;

    this.domTable = $(`<div class="questionnaire"></div>`);
    for (var qaSetIndex in this.questionnaireJson){
        var qaSet = this.questionnaireJson[qaSetIndex];

        //Check for topic header before
        if ('topic' in qaSet){
            this.domTable.append(`<h2>${qaSet.topic}</h2>`);
        }

        var qaSetTable = $(`<table class='table table-striped qa-set' data-set-index='${qaSetIndex}'><thead></thead><tbody></tbody></table>`);

        //Load answers for table header
        var responseRow = $("<tr></tr>");
        responseRow.append($("<th></th>")); //Blank cell over question
        for (var a = 0; a < qaSet.answers.length; a++){
            responseRow.append($(`<th class='fit'>${qaSet.answers[a]}</th>`));
        }
        responseRow.appendTo(qaSetTable.find("thead"));

        //Load in questions row by row
        for (var qIndex = 0; qIndex < qaSet.questions.length; qIndex++){
            var qaRow = $("<tr class='question-row'></tr>");
            qaRow.append($(`<td>${qaSet.questions[qIndex]}</td>`));

            //Add checkbox for every possible response.
            for (var aIndex = 0; aIndex < qaSet.answers.length; aIndex++){
                //Tag radio with set number and question number for parsing later.
                qaRow.append($(`<td class="fit"><input type="radio" name="s${qaSetIndex}q${qIndex}" data-set-index="${qaSetIndex}" data-qindex="${qIndex}" data-answer-index="${aIndex}" value="${aIndex}"></td>`));
            }
            qaRow.appendTo(qaSetTable.find("tbody"));
        }

        //Append to container last after everything is added to stop unnecessary redraws
        this.domTable.append(qaSetTable);
    }

    this.dataForm = dataForm;

    var that = this;
    this.dataForm.on("submit", function(){ return that.submit(); });
    this.domTable.append(this.dataForm);

    this.loadResponse = function(responseJson){
        //Lock all inputs in container
        this.domTable.find("input[type=radio]").prop("hidden", true);
        this.dataForm.remove();

        //TODO: Iterate over table successively, avoid searching entire form to find radio inputs
        var response = responseJson.response;
        for (var setIndex = 0; setIndex < response.length; setIndex++){
            var questions = response[setIndex];
            for (var qIndex = 0; qIndex < questions.length; qIndex++){
                this.domTable.find(`input[type=radio][data-set-index=${setIndex}][data-qindex=${qIndex}][data-answer-index=${questions[qIndex]}]`).prop("hidden", false).prop("checked", true);
            }
        }
    };

    this.compileResponse = function(){
        var jObj = { response: [] };
        var response = jObj.response;

        var allFilledOut = true;
        var score = 0;
        var that = this;
        this.domTable.find(`.question-row`).each(function(){
            //Find selected response
            var selectedRadio = $(this).find("input[type=radio]:checked");
            if (selectedRadio.length){
                var setNum = selectedRadio.attr("data-set-index");
                var radioVal = selectedRadio.attr("value");

                if (!response[setNum]){
                    response[setNum] = [];
                }
                //Record response value in json
                response[setNum].push(radioVal);

                //Add value to score if this set is scored.
                if (that.questionnaireJson[setNum].scored){
                    score += parseInt(radioVal);
                }

                //Question filled out, reset alert
                $(this).removeClass("alert-danger");
            }
            else {
                allFilledOut = false;

                //Set alert class to notify user to
                $(this).addClass("alert-danger");
            }
        });

        return allFilledOut ? {"jObj": jObj, "score": score} : false;
    };

    this.submit = function(){
        var response = this.compileResponse();

        if (response !== false){
            $("#alert-container").hide();

            //Set data field of hidden submit form
            this.dataForm.find("[name='data']").attr("value", JSON.stringify(response.jObj));
            this.dataForm.find("[name='score']").attr("value", response.score);

            //Interpret score for response
            for (var range in this.scoringJson){
                let lowerBound = parseInt(range.match(/^(\d+):/)[1]);
                let upperBound = parseInt(range.match(/:(\d+)$/)[1]);

                if (response.score >= lowerBound && response.score <= upperBound){
                    this.dataForm.find("[name='severity']")
                        .attr("value", this.scoringJson[range].severity);
                    this.dataForm.find("[name='treatment']")
                        .attr("value", this.scoringJson[range].treatment);
                    break;
                }
            }
        }
        else {
            //Show fill out notice
            $("#alert-container").show();

            //Scroll page back to top of questionnaire to fill out missed
            $('html').animate({
                scrollTop: 0
            }, 500);

            //Return false to cancel form submit
            return false;
        }
    };
}
