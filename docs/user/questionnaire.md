# View All Questionnaires

When the "Questionnaires" tab is selected on the top navigation bar, a list of all questionnaires is shown.  Each questionnaire can be viewed or edited from here by using the controls to the left of each questionnaire.

# View Questionnaire

When the "view" button next to a Questionnaire is clicked, the Questionnaire detail view is shown.  On this page the contents of the questionnaire are shown, including all question sets, and their corresponding questions and answers, along with their number/score values.

# Edit Questionnaire

When the "edit" button next to a Questionnaire is clicked, the questionnaire edit page is shown.  On this page all components of the questionnaire can be altered.  The title, the topic of each question set, the content of each question/answer and the scoring flags can all be changed.

**Please note that if a question is removed, so will the responses to that question.**  If a question's text is edited, however, the responses will remain untouched.

# Scoring

Each questionnaire can be scored according to a set of scoring "flags", each of which has a condition.  Within the condition, the answers to any question, or the score of any question set can be used to see of a given response matches these criteria.

## Conditions

Flag conditions are quite simple.  Two methods are provided for evaluating a questionnaire: `answer(set_number, question_number)` and `score(set_number)`.  Any combination of these two can be used to raise a specific flag for any given questionnaire and response.

### Simple Example

Given the following response to our simple questionnaire:



| *Question Set 1*                   | 0: Yes | 1: No |
|------------------------------------|--------|-------|
| 1. Are you okay?                   |        |   X   |

We can see that the patient answered "No" to set 1 question 1, and we want to raise a flag in this case because the patient is not okay.  The condition we would write to catch this would be as follows:

Condition: `answer(1, 1) == 1`

This condition read aloud is "If the answer to set 1 question 1 is 1".  When that statement is true in the response, the flag will be raised and the clinician will be notified.

Similarly, the score of the set can be used as a more general measure.  For example, `score(1) == 1` would be equivalent as there's only one set with one question.

### Real World Example

The MDQ scoring uses both the `answer` and `score` methods of evaluation.  In plain English the MDQ defines testing positive for bipolar disorder as follows:

```text
“YES” to 7 or more of the 13 Questions in Set 1
AND “Yes” to Set 2 Question 1
AND “Moderate Problem” or “Serious Problem” to Set 3 Question 1
```

The corresponding flag condition is as follows:

```text
score(1) >= 7
and answer(2, 1) == 1
and answer(3, 1) >= 2
```
