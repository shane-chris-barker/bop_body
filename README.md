[![Tests](https://github.com/shane-chris-barker/bop_body/actions/workflows/test.yml/badge.svg)](https://github.com/shane-chris-barker/bop_brain/actions/workflows/test.yml)
# 🦾 Bop Body
**Bop Body** is the reaction module for **Bop**, a work-in-progress Raspberry Pi-powered robot pet project.

This is **one of three core repositories**:
- [bop_sense](https://github.com/shane-chris-barker/bop_sense) - Listens to the world (mic, camera, sensors) and places AMQP or MQTT messages into a queue.

- [bop_brain](https://github.com/shane-chris-barker/bop_brain) - Responsible for processing the messages produced by `bop_sense` and making decisions based on their content before dispatching the related events.

- ***bop_body*** - Subscribes to events produced by `bop_brain` and then take an action (motors, display, feedback etc.)

> ⚠️ **Note**: This is an early, rough WIP and very much an experiment. Things will change, break, and improve rapidly. 

>I'm also very new to Python, so there are bound to be mistakes..

I will add more information here as the project progresses.

---
## ✅️ What Bop Body Can Do Right Now
- Handle events produced by `bop_brain` and placed into an MQTT.
- Use Pygame to update a HDMI screen with reactions

## 🛠️ Planned Features

- Take more events, such as weather report requests, movement instructions and more.

---

## 🧪 Testing

I am adding tests as I go. Run them via:

```bash
pytest --cov-report=term-missing
```
## 🚀 Getting Started
Clone this repo

Create a `.env.dev` file based on `.env.example`

Install dependencies:
```
sh setup.sh
```
Run the app
```
python main.py

```

## 📡 Communication Types
Supports consuming events with:

**AMQP** (e.g. RabbitMQ) - Coming Soon

**MQTT** (e.g. Mosquitto)


