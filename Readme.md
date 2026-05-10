How to start jenkins and ngrok after restarting of local machine:


s1: cd {to your folder}
s2: java -jar jenkins.war (http://localhost:8080)
s3: ngrok http 8080 (https://something.ngrok-free.dev)


Important Reminder
Because you use FREE ngrok:

URL changes every restart

So after restarting ngrok:

Go to your GitHub Repository Webhooks Settings
 repository webhook and update:

OLD:
https://old-url.ngrok-free.dev/github-webhook/

NEW:
https://new-url.ngrok-free.dev/github-webhook/

Otherwise GitHub pushes will stop triggering Jenkins.


must end with github-webhook/