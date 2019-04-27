var mainContainer = $(`
<div id="questionnaire-builder">
    <div class="row">
        <div class="col-xl-6">
            <div class="form-group">
                <label for="questionnaire-name">Questionnaire Name</label>
                <input type="text" class="form-control" id="questionnaire-name" placeholder="Name">
            </div>
        </div>
    </div>

    <br/>

    <div class="question-sets-container"></div>
    <form class="form-inline add-question-set" onsubmit="return false;">
        <div class="form-group">
            <div class="input-group">
                <div class="input-group-prepend">
                    <div class="input-group-text">Title (optional):</div>
                </div>
                <input class="form-control" type="text" name="set-topic">
                <div class="input-group-append">
                    <button type="submit" class="btn btn-success">Add Question Set</button>
                </div>
            </div>
        </div>
    </form>

    <hr>
    <br/><br/>

    <h1>Scoring</h1>
    <div class="row">
        <div class="col-xl-6">
            <div class="scoring-flags-container"></div>
            <button class="btn btn-success add-scoring-flag">Add Scoring Flag</button>
        </div>
    </div>

    <hr>
</div>
`);

QUnit.test("Questionnaire add/remove set", function(assert){
    var q = new Questionnaire(mainContainer.clone());

    assert.equal(q.questionSets.length, 0, "New questionnaire has no sets");

    var set = q.addQuestionSet("boring topic");
    assert.equal(q.questionSets.length, 1, "Count = 1 after set added");

    q.removeQuestionSet(set);
    assert.equal(q.questionSets.length, 0, "Count = 0 after removal");
});

QUnit.test("Questionnaire add/remove flag", function(assert){
    var q = new Questionnaire(mainContainer.clone());

    assert.equal(q.scoringFlags.length, 0, "New questionnaire has no flags");

    var flag = q.addScoringFlag("danger will robinson");
    assert.equal(q.scoringFlags.length, 1, "Count = 1 after flag added");

    q.removeScoringFlag(flag);
    assert.equal(q.scoringFlags.length, 0, "Count = 0 after removal");
});

QUnit.test("JSON contains flags and sets", function(assert){
    var q = new Questionnaire(mainContainer.clone());

    var flag = q.addScoringFlag("danger will robinson");
    var set = q.addQuestionSet("boring topic");

    var qJson = JSON.stringify(q.compileJson());

    //See if the json contains the set and flag by looking for their title/topic
    assert.ok(qJson.indexOf("danger will robinson") != -1,
        "JSON contains flag");

    assert.ok(qJson.indexOf("boring topic") != -1,
        "JSON contains set");
});

QUnit.test("Set add/remove question/answer", function(assert){
    var q = new Questionnaire(mainContainer.clone());

    var qSet = q.addQuestionSet("boring topic");

    assert.equal(qSet.questions.length, 0, "Empty set has no questions");
    assert.equal(qSet.answers.length, 0, "Empty set has no answers");

    var question =
        qSet.addQuestion("You finna hit that YEET?"); // Cause I'm finna GET IT
    //No one's ever gonna read this garbage.
    assert.equal(qSet.questions.length, 1, "Question count is 1 after add");

    qSet.removeQuestion(question);
    assert.equal(qSet.questions.length, 0, "Question count is 0 after removal");

    var answer =
        qSet.addAnswer("Ye, shit's gonna be TURNT");
    assert.equal(qSet.answers.length, 1, "Answer count is 1 after add");

    qSet.removeAnswer(answer);
    assert.equal(qSet.answers.length, 0, "Answer count is 0 after removal");
});
