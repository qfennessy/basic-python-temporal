from temporalio.client import Client
import uuid

async def main():
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")

    # Generate a unique WorkflowId
    unique_workflow_id = f"echo-workflow-{uuid.uuid4()}"

    # Start the workflow
    result = await client.start_workflow(
        workflow="EchoWorkflow",            # Workflow name
        arg="John Doe",                     # Workflow input
        id=unique_workflow_id,              # Workflow ID
        task_queue="echo-task-queue",       # Task queue
    )

    print(f"Workflow result: {result}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
