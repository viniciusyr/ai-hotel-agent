# Hotel Voice Agent

A real-time inbound phone agent for a United States hotel company. It uses Pipecat for voice orchestration, Twilio Media Streams for telephony, Deepgram Nova-3 for streaming speech-to-text, Anthropic Claude for conversation, and Cartesia Sonic for streaming text-to-speech.

## Prerequisites

- Python 3.11
- A Twilio account with a voice-capable phone number
- Deepgram API key
- Anthropic API key with access to the configured Claude model
- Cartesia API key and voice ID
- ngrok for local webhook testing
- Docker and Google Cloud CLI for Cloud Run deployment

## Local Setup

1. Create and activate a virtual environment.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Create your local environment file.

```bash
cp .env.example .env
```

4. Fill in `.env` with your Twilio, Deepgram, Anthropic, Cartesia, hotel, and app values.

## Run Locally

Start the FastAPI server.

```bash
python main.py
```

In another terminal, expose the local server with ngrok.

```bash
ngrok http 8080
```

Use the HTTPS forwarding URL from ngrok as the public base URL for Twilio. The webhook path is `/voice`, for example:

```text
https://your-ngrok-domain.ngrok-free.app/voice
```

Twilio will receive TwiML from `/voice`, then connect the call to `/ws` over a secure WebSocket URL generated from the same public host.

## Configure Twilio

1. Open the Twilio Console.
2. Go to Phone Numbers, then Manage, then Active numbers.
3. Select your hotel phone number.
4. Under Voice Configuration, set "A call comes in" to "Webhook".
5. Set the webhook URL to your public `/voice` URL.
6. Set the HTTP method to `POST`.
7. Save the configuration.

Call the Twilio number. The agent should answer, greet the guest with the hotel name, and keep the conversation on the WebSocket stream.

## Deploy To Google Cloud Run

1. Set your Google Cloud project.

```bash
gcloud config set project YOUR_PROJECT_ID
```

2. Build and submit the container image.

```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/hotel-voice-agent
```

3. Deploy to Cloud Run with the values from `.env`.

```bash
gcloud run deploy hotel-voice-agent \
  --image gcr.io/YOUR_PROJECT_ID/hotel-voice-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --env-vars-file .env
```

Cloud Run returns a public HTTPS service URL. Configure Twilio to send inbound calls to:

```text
https://YOUR_CLOUD_RUN_URL/voice
```

## Environment Variables

All runtime configuration lives in `.env`. The Dockerfile does not define application secrets or runtime configuration values.

Required variables:

- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `DEEPGRAM_API_KEY`
- `ANTHROPIC_API_KEY`
- `CLAUDE_MODEL`
- `CARTESIA_API_KEY`
- `CARTESIA_VOICE_ID`
- `HOTEL_NAME`
- `HOTEL_CITY`
- `HOTEL_PHONE`
- `HOTEL_CHECKIN_TIME`
- `HOTEL_CHECKOUT_TIME`
- `APP_HOST`
- `APP_PORT`
- `LOG_LEVEL`

## Health Check

Cloud Run can use the health endpoint:

```text
GET /health
```

Expected response:

```json
{"status":"ok"}
```
