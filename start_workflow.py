import asyncio
import logging
import uuid

import click
from temporalio.client import Client

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def start_workflow(name: str):
    try:
        # Connect to Temporal server
        client = await Client.connect("localhost:7233")

        # Generate a unique WorkflowId
        unique_workflow_id = f"echo-workflow-{uuid.uuid4()}"

        logger.info(f"Starting workflow with name: {name}")
        # Start the workflow
        result = await client.execute_workflow(
            "EchoWorkflow",  # Workflow name
            name,  # Workflow input
            id=unique_workflow_id,  # Workflow ID
            task_queue="echo-task-queue",  # Task queue
        )

        logger.info(f"Workflow completed successfully with result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error starting workflow: {e}", exc_info=True)
        raise


@click.command()
@click.option("--name", "-n", required=True, help="Name to echo in the workflow")
def main(name: str):
    """Start the Echo workflow with the provided name."""
    try:
        result = asyncio.run(start_workflow(name))
        click.echo(f"Workflow result: {result}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
