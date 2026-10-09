# AI Secretary

AI Secretary is an intelligent productivity assistant that helps you manage tasks effectively using TaskWarrior. It classifies user intents, schedules tasks, and provides productivity tips, all while handling non-standard time formats with the help of an LLM (Large Language Model).

## Features

- **Task Management:** Add, modify, and complete tasks using natural language commands.
- **Task Query:** Check tasks or suggest time slots for task completion.
- **Productivity Tips:** Receive actionable productivity advice with specific actions and times.
- **Location Query:** Get suggestions for places or options based on user queries.
- **General Query:** Handle general questions or requests that don't fit into other categories.
- **Error Handling:** Automatically corrects non-standard time formats using LLM until the task is successfully added to TaskWarrior.

## Requirements

- Python 3.12+
- UV package manager
- TaskWarrior
- Ollama LLM (for intent classification and time format correction)
- Subprocess module for running TaskWarrior commands

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/deadeyesky/AI_Secretary.git
    cd AI_Secretary
    ```

2. **Install the required Python packages:**

    ```sh
    uv sync
    ```

3. **Ensure TaskWarrior is installed:**

    ```sh
    sudo apt-get install taskwarrior    # Debian / Ubuntu
    sudo dnf install taskwarrior        # Fedora
    sudo pacman -S taskwarrior          # Arch / EndeavorOS / CachyOS

    ```

    Or for Mac:

    ```sh
    brew install task
    ```

## Usage

1. **Run the AI Secretary:**

    ```sh
    python3 ai_secretary.py
    ```

2. **Interact with the Assistant:**

    Type your requests and follow the prompts. Example interactions:

    - "Add task Buy groceries on 2024-07-03 at 15:00"
    - "I want to be more productive today"
    - "Where can I find a good coffee shop?"

3. **Exit the Assistant:**

    Type `exit` to quit the program.

## Code Overview

- `ai_secretary.py`: Main script for running the AI Secretary.
- `TaskWarriorIntegration`: Class for interacting with TaskWarrior.
- `ActionExecutor`: Class for executing actions based on user intents.
- `correct_time_format`: Function for correcting non-standard time formats using LLM.
- `classify_intent`: Function for classifying user input into predefined intents.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Thanks to the developers of TaskWarrior for their excellent task management tool.
- Thanks to Ollama for their powerful LLM used in this project.

## Troubleshooting

- Ensure that TaskWarrior is properly installed and configured on your system.
- Check that you have internet access for the LLM queries.
- If tasks are not being added correctly, review the log output for errors and ensure the time formats are correct.
