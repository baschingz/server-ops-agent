# Server Ops Agent

This project is designed to automate server operations and manage infrastructure tasks using a multi-agent system.

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd server-ops-agent
   ```

2. **Set up the environment**

   - Ensure you have Python 3.8+ installed.
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Configure environment variables**
   - Copy `.env.example` to `.env` and fill in the necessary environment variables:
     ```
     cp .env.example .env
     ```

## Usage

1. **Run the application**

   ```bash
   python app/main.py
   ```

2. **Interact with the system**
   - Use the provided API endpoints to interact with the agents.
   - The agents can automate tasks such as monitoring CPU, deploying an app, or modifying system configurations.

## Features

- Multi-agent system for task automation
- Integration with LINE messaging API for notifications
- SSH command execution on remote servers

## Contributing

Feel free to contribute to this project by submitting issues or pull requests.
