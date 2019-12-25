# <h1>restapicass</h1>
<H3><b>Installation</b></h3>
To run the app download it. Then type in <code>docker-compose up</code>. 



<H3><b>Post</b></h3>
<br>
There are two ways to post with this API
<h6>first:</h6>
through <code>/api/message</code> 
this requests adds to the datebase the "message" in format
<code>{"email":"vaild email adress","title":"text","content":"simple text","magic_number":int}</code>


example command:
<code>curl -X POST localhost:8080/api/message -d '{"email":"jan.kowalski@example.com","title":"Interview","content":"simple text","magic_number":101}'</code>

<h6>second:</h6>
through <code>/api/send</code> which allows api-user to post all the messages that include specific <code>magic_number</code>
and then <b>deletes</b> them from database


example:
<code>curl -X POST localhost:8080/api/send -d '{"magic_number":101}'</code>

<h3>Get</h3>

<code>/api/messages/{emailValue}</code> allows you to return all the messages with given email. 


<h4>Notes</h4>
The database wipes out all the messages that are 300 seconds old.