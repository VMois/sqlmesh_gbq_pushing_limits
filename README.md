# SQLMesh GBQ - pushing the limits

## Setup

Raw data tables are located in the `setup/` folder. Execute these SQL files directly in BigQuery to create the initial tables with sample data.

## Running SQLMesh

- To run SQLMesh with a specific gateway in prod: `uv run sqlmesh --gateway location_us plan prod`

## Notes

### Authentication
- `gcloud auth application-default login` for local auth

### State Management
- **State DB is required**: SQLMesh requires a state database to track model versions, environments, and deployment history. Without it, SQLMesh cannot manage incremental deployments or environment isolation.

### Important Limitations
- **No drift detection**: SQLMesh does NOT detect if the target environment has been tampered with manually. For example:
  - If you manually change a column in a BigQuery view
  - Then run `sqlmesh plan` without updating the local model file
  - SQLMesh will produce NO errors or warnings about the drift
  - This can lead to inconsistencies between your codebase and actual database objects
  - **Best practice**: Always make changes through SQLMesh model files, never directly in BigQuery
