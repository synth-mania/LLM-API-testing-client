# LLM API testing client

A graphical user interface for interacting with the OpenAI compatible LLM APIs for text completions.

## Features

- User-friendly interface for sending prompts to any API
- Configuration management for API settings
- Token usage and cost tracking
- Response display and history

## Installation

### Automatic Setup

#### On Linux/macOS:
1. Make the setup script executable:
   ```
   chmod +x setup.sh
   ```
2. Run the setup script:
   ```
   ./setup.sh
   ```

#### On Windows:
1. Run the setup script:
   ```
   setup.bat
   ```

### Manual Setup
1. Clone this repository
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Using Run Scripts

#### On Linux/macOS:
```
./run.sh
```

#### On Windows:
```
run.bat
```

### Manual Execution
1. Activate the virtual environment:
   ```
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Run the application:
   ```
   python main.py
   ```
