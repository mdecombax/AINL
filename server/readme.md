# launch server

## launch api

uvicorn api:app --reload
pyenv install 3.10.7

## Launch ngrok
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
	| sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
	&& echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
	| sudo tee /etc/apt/sources.list.d/ngrok.list \
	&& sudo apt update \
	&& sudo apt install ngrok

ngrok config add-authtoken 2NQpmj097zvuOlfaUxYDPc617s8_7cT8NH89DAswjuzxdDTwV

ngrok http 8000

## Replace fetch endpoint
fetch('**https://12e0-35-205-136-159.ngrok-free.app**/newsletter/?subreddit=artificial',{
