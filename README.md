# basic-python-temporal

This project demonstrates how to use Temporal's Python SDK to create, execute, and manage workflows and activities. It includes an example workflow (`EchoWorkflow`) and an activity (`echo_activity`) that interact to process and log input data.

## Features

- **EchoWorkflow**: A workflow that receives a string as input and executes an activity to process the input.
- **echo_activity**: An activity that takes the workflow input and returns a formatted result.
- **Logging**: Structured logging for workflows and activities to aid in debugging and monitoring.
- **Error Handling**: Robust error handling to manage invalid inputs and unexpected failures.

## File Structure

- **`worker.py`**: Sets up and starts a Temporal worker to listen for tasks on a designated task queue.
- **`start_workflow.py`**: CLI-based script to start the `EchoWorkflow` with user-provided input.
- **`workflows.py`**: Contains the definition of the `EchoWorkflow` and the associated `echo_activity`.
- **`requirements.txt`**: Lists dependencies required to run the project.
- **`LICENSE`**: MIT License for the project.

## Prerequisites

1. Install Python 3.10 or higher.
2. Set up a Temporal server instance. You can use [Temporal's Quick Start](https://docs.temporal.io/application-development/foundations) guide for a local setup.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd basic-python-temporal
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Start the Temporal Worker
The worker listens for tasks on the `echo-task-queue` and processes workflows and activities.

```bash
python worker.py
```

### 2. Start a Workflow
Use the `start_workflow.py` script to initiate the `EchoWorkflow`.

```bash
python start_workflow.py --name "John Doe"
```

The output will display the result of the workflow execution.

### 3. View Logs
Logs provide detailed information about the workflow and activity execution. Logs are displayed in the console and can be configured to write to a file.

## Code Highlights

### EchoWorkflow
This workflow validates the input and executes the `echo_activity`.

```python
@workflow.defn(name="EchoWorkflow")
class EchoWorkflow:
    @workflow.run
    async def run(self, name: str = None) -> str:
        if not name:
            raise ValueError("Name parameter must be a non-empty string")
        return await workflow.execute_activity(
            echo_activity,
            EchoWorkflowParams(name),
            start_to_close_timeout=timedelta(seconds=10),
        )
```

### echo_activity
This activity processes the input and returns a formatted result.

```python
@activity.defn(name="echo_activity")
async def echo_activity(input: EchoWorkflowParams) -> str:
    if not input.name:
        raise ValueError("Invalid input: name cannot be empty")
    return f"===> {input.name} <==="
```

## Advanced Features

- **UUID-based Workflow IDs**: Ensures each workflow execution has a unique identifier.
- **Retry Policies**: Configure retry logic for resilient activity execution.
- **CLI Integration**: The `start_workflow.py` script leverages `click` for a user-friendly command-line interface.

## Contributing

Contributions are welcome! Please submit issues or pull requests for improvements or new features.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

