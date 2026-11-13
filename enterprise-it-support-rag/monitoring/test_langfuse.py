
from dotenv import load_dotenv
from langfuse import get_client

load_dotenv()

langfuse = get_client()

print("Testing Langfuse connection...")

with langfuse.start_as_current_observation(
    as_type="span",
    name="NEXUS-IT-connection-test",
    input={"test": "Langfuse connection"}
) as span:

    span.update(
        output={"status": "Connected successfully"}
    )

    # Get the URL while the observation is still active
    trace_url = langfuse.get_trace_url()
    print("Trace URL:", trace_url)

langfuse.flush()

print("Langfuse test completed!")
