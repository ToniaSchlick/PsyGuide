# Product introduction

(Subject to change during the development process)
## Our App
Our application gives medical professionals guidelines for typical diagnosis and treatment. When a medical professional uses our app, they can log in and create profiles for their patients. Information stored here, instead of the traditional method in stacks of paper, is more persistant and easier to access. 

Furthermore, our app can directly give the PHQ-9 questionnaires at will for regular psychological evaluations, keep track of results, and give the recommended diagnosis and treatment each time. Of course, not all patients fit the recommended diagnosis. In cases like this, medical professionals are free to choose a different diagnosis or treatment if it does not match the one recommended by our app. To stay up to date with current research, or if doctors want to make personal adjustments to the treatment algorithms, they may make adjustments to flowcharts using draw.io. 

By using our app, medical professionals can stay up to date about how best to treat patients without needing to look through their books before each appointment. This saves time that can instead be given on patients.

## Included Features:
- Secure login and storage, protecting patient information in accordance with HIPPA.
- Developers can easily adjust treatment protocols, so that our app always provides the latest most effective information. 
- Easy to use, so that medical professionals can focus their energy on patients. 

### How to start using the app: 
- Visit http://ec2dev.xeviansoftware.com/# and click 'Live Install'.
- To register, click 'Register', fill in your information, and hit 'register'. 
- To add a new patients, click on the 'Patients' header at the top, and then the 'add' button. Then fill in the patient's information. Keep in mind that the birthdate format is dd/mm/yyyy. 
- To edit a patient, click 'view' on the desired patient, and then 'edit'. 
- To evaluate a patient with a questionnaire, click 'evaluate' on the desired patient, and then the questionnaire you want them to take. Once submitted, responses will be saved. 

How to report a bug:

## Information for Developers:
Our code on github is [here](https://github.com/friday-the-13th/Front-end).

Information about project structure and setting up developer tools is [here](http://ec2dev.xeviansoftware.com/devinfo.html).
### Additional information about testing: 
- After navigating to the PsyGuideSite folder in your command prompt, type 'python manage.py shell'. Then, type'import os', followed by 'os.chdir(r *the directory where you have your tests*)'. From here, you can run your test file with 'exec(open(*filename*).read())'
- You will notice that changes made to your tests will take effect on the test server immediately, allowing for faster testing. 
