# n8n_execution_report
Analyze your n8n workflow executions and generate detailed reports in PDF format, including AI costs, node performance, and optimization suggestions.

## Features
- Summarizes execution duration, AI usage and estimated cost
- Detects AI nodes and calculates token usage
- Highlights slowest nodes and potential bottlenecks
- Outputs a clean, readable PDF report
- Simple to run locally with just Python

## Requirements
- Python 3.9 or higher
- Dependencies:
  ```bash
  pip install -r requirements.txt
 
## How to use it

### 1. Import included n8n workflow template
- Go to: n8n > Workflows > Import
- Load the template included in this repo

### 2. Modify the "get_execution_info" HTTP Request node in the workflow

- Update the domain and execution ID in this format
```bash
https://<your-n8n-domain>/api/v1/executions/<execution_id>

- Set this configuration in the HTTP Request node



### 3.
