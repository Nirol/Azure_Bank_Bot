# Microsoft Azure Bank Bot Service using LUIS to implement core AI capabilities

## Overview
**Banking text bot Based on Microsoft beta python bot framework   
 using LUIS**
* **Based on microsoft [botbuilder-python](https://github.com/microsoft/botbuilder-python/) github repo.**
* **User input analyzed by the bank bot [LUIS cognitive engine](/BankBot/cognitiveModels/Bank.json):**
    * Support for different Salary Intents: average, year to date,  
     last salary and all salary data.
    * Support either net or gross information entities for  
     every salary intent.
     

<div style="text-align:center"><img src="bot_example1.png" width="480"></div>

* **Follow up dialogs for different intents, completing  
 required information**
    * If net and gross entities are missing from user request:  
       * Ask the user for either net, gross or both salary data.
     * If salary data type is missing from the user request: 
        * Ask for either total salary data or one of the possible answers.     
     * scoring the user dialog input versus the different possible  
      answers, covering for spelling mistakes.
    

<div style="text-align:center"><img src="bot_example2.png"  width="480"></div>

 
    
 
## Running the code

* Main python script function located in [botbuilder-python/BankBot/app.py](botbuilder-python/BankBot/app.py)  

 * ***best Practice in order to load the project is to add the root folder  
  (folder play_with_azure) as a project to pycharm***
  
  
 * required dependencies libraries are detaild in [botbuilder-python/BankBot/requirements.txt](botbuilder-python/BankBot/requirements.txt)
  install dependecies using:
   ```
    use pip install -r requirements.txt 
