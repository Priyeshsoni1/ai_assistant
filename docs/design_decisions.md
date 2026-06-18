# Design Decisions

## Why streaming?

Improves perceived latency and user experience.

## Why conversation memory?

LLM APIs are stateless.
To create multi-turn conversations, previous messages must be stored and sent with every request.

Benefits:
--context retention,--Better user experience ,--ChatGPT -like behaviour

## Why token counting?

Tracks cost and context window usage.
