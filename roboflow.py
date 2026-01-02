from inference_sdk import InferenceHTTPClient

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="BbNlVkaSYTUeNTmL11Su"
)

result = client.run_workflow(
    workspace_name="firsttest-s0stw",
    workflow_id="find-zlijs",
    images={
        "image": "z.png"
    },
    use_cache=True # cache workflow definition for 15 minutes
)
print(result)