from temporalio.worker import Worker
from temporalio.client import Client
from workflows import EchoWorkflow, echo_activity

async def main():
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")

    # Create and run the worker
    worker = Worker(
        client,
        task_queue="echo-task-queue",
        workflows=[EchoWorkflow],
        activities=[echo_activity],
    )

    print("Worker started. Listening for tasks...")
    await worker.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
