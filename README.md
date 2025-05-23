# n8n_execution_report
Analyze your n8n workflow executions and generate detailed reports in PDF format, including AI costs, node performance, and optimization suggestions.

This tool currently supports workflows with one level of subworkflows only. Nested subworkflows beyond that level are not yet supported.

![](./assets/example_pdf_1.PNG)
![](./assets/example_pdf_2.PNG)
## Features
- Summarizes execution duration, AI usage and estimated cost
- Detects AI nodes and calculates token usage
- Highlights slowest nodes and potential bottlenecks
- Outputs a clean, readable PDF report
- Simple to run locally with just Python

## Requirements
- Python 3.9 or higher
- Install fpdf and sys to generate pdf report
  ```bash
  pip install fpdf
  pip install sys
 
## How to use it

### 1. Import included n8n workflow template

- Go to: n8n > Workflows > Import
- Load the template "Auditor.json" included in this repo

### 2. Modify the "get_execution_info" n8n API node in the workflow
- You need a n8n api key. Fill it in the field "Credential to connect with". Create a credential if you dont have it with the n8n api key and your hostname.
![](./assets/n8n_api_credential.PNG)

- Just need to get the execution ID and set in "Execution ID" field.
- Be sure to active the "Include Execution Details" toggle.

  #### - Example
   
  ![](./assets/n8n_node.PNG)

- Do the same for the node "get_execution_info_subworkflow"

### 3. Run the n8n workflow and get JSON file output

- Double click in "get_json_file" node

  ![](./assets/get_json_file.PNG)

- Download the JSON file

  ![](./assets/download_json.PNG)

### 4. Use python script to generate the report

- Download "report_generator_script.py" in this repo.
- Execute this command to get your PDF report.
```bash
python report_generator_script.py <name of your JSON file from n8n>
```
Example: python report_generator_script.py my_json_file.json

- This will save in the same root a PDF file with your execution report.

## What's next?

Guys I want to upgrade this tool have things in mind...

- Support for multiple executions across time periods
- Visual charts for cost evolution and execution load
- Optional web interface for easier use — Our at least improve the accesibility to this tool, too much steps...

Right now, the most value in this is you guys tell me things to improve, bugs to fixes etc..

Feel free to open an [issue](https://github.com/Xavi1995/n8n_execution_report/issues)

This tool is not affiliated with n8n — just a side project to make auditing easier for developers.

And give me a :star: if you found this usefull (what I'm trying to be).
