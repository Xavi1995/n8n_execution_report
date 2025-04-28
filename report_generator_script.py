import json
import sys
from fpdf import FPDF

# Funciones auxiliares
def get_slowest_node(nodes):
    return max(nodes, key=lambda node: node.get('execution_time', 0))

def get_bottlenecks(nodes, pdf):
    pdf.set_font("Arial", "B", 11)
    pdf.write(5, "Bottleneck nodes",)
    pdf.ln(10)
    total_time = sum(n.get('execution_time', 0) for n in nodes)

    if total_time == 0:
        pdf.set_font("Arial", "", 10)
        pdf.write(5, "No execution time recorded")
    
    bottlenecks = [
        {
            "name": n['name'],
            "time": n['execution_time'],
            "percentage": round((n['execution_time'] / total_time) * 100, 2)
        }
        for n in nodes if (n.get('execution_time', 0) / total_time) > 0.3
    ]

    if not bottlenecks:
        pdf.set_font("Arial", "", 10)
        pdf.write(5, "No significant bottlenecks detected.")
        return

    for b in bottlenecks:
    
        pdf.set_font("Arial", "", 10)
        pdf.write(5, f"    ")
        pdf.write(5, f"- {b['name']}")
        

        pdf.set_font("Arial", "", 10)
        pdf.write(5, f" | {b['time']} ms |")

        pdf.set_font("Arial", "B", 10)
        pdf.write(5, f" {b['percentage']}%")

        pdf.set_font("Arial", "", 10)
        pdf.write(5, f" of total execution time")
        pdf.ln(10)

   

def format_node_table(pdf, nodes, title):
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, title, ln=True,)
    pdf.set_font("Arial", "B", 10,)
    pdf.set_fill_color(200)
    pdf.cell(60, 8, "Node", border=1, fill = True)
    pdf.cell(60, 8, "Type", border=1,  fill = True)
    pdf.cell(30, 8, "Time (ms)", border=1,  fill = True)
    pdf.set_font("Arial", '', 10)
    pdf.ln()
    for node in nodes:
        write_content(f"{node['name'][:30]}", pdf, 60, 8)
        write_content(f"{node['type'].split('.')[-1]}", pdf, 60,8)
        write_content(str(node.get('execution_time', 0)), pdf, 30, 8)
        pdf.ln()
    pdf.ln()

def process_workflow(pdf, workflow, level=0):
    indent = "  " * level
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"{indent}Workflow: {workflow['workflow_name']}", ln=True)
    
    
    pdf.set_font('Arial', 'B', 10)
    pdf.write(5, f"{indent}Execution ID: ")
    
    pdf.set_font('Arial', '', 10)
    pdf.write(5, f"{workflow['execution_id']}")
    pdf.ln()

    pdf.set_font("Arial", "B", 10)
    pdf.write(5, "Status: "),
    pdf.set_font("Arial", "", 10)
    pdf.write(5, f"{workflow['execution_status']}")
    pdf.ln()

    pdf.set_font("Arial", "B", 10)
    pdf.write(5, "Date: ")
    pdf.set_font("Arial", "", 10)
    pdf.write(5, f"{workflow['execution_date']}")
    pdf.ln()

    pdf.set_font("Arial", "B", 10)
    pdf.write(5, "Duration: ")
    pdf.set_font("Arial", "", 10)
    pdf.write(5, f"{workflow['execution_duration']}s")
    pdf.ln()

    pdf.set_font("Arial", "B", 10)
    pdf.write(5, "Total AI Cost ($): ")
    pdf.set_font("Arial", "", 10)
    pdf.write(5, f"{workflow.get('total_cost', 'N/A')}")
    pdf.ln()

    ai_nodes = workflow['nodes'].get('ai_nodes', [])
    non_ai_nodes = workflow['nodes'].get('non_ai_nodes', [])

    if ai_nodes:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 10, "AI Nodes", ln=True)
        pdf.set_font("Arial", "B", 10)
        pdf.set_fill_color(200)
        pdf.cell(50, 8, "Node", border=1, fill=True)

        pdf.cell(40, 8, "Model", border=1, fill=True)
        pdf.cell(30, 8, "Tokens", border=1, fill =True)
        pdf.cell(30, 8, "Time (ms)", border=1, fill = True)
        pdf.cell(30, 8, "Cost", border=1, fill = True)
        pdf.ln()

        pdf.set_font("Arial", "", 10)
        for ai in ai_nodes:
            details = ai.get('ai_details', {})
            write_content(f"{ai['name'][:25]}", pdf, 50, 8)
            write_content('gemini-2.5-pro-preview-03-25', pdf, 40, 8)
            tokens = f"{details.get('prompt_tokens', 0)} + {details.get('completion_tokens', 0)}"
            write_content(tokens, pdf, 30, 8)
            write_content(str(ai.get('execution_time', 0)), pdf, 30, 8)
            write_content(details.get('cost_execution', 'N/A'),pdf, 30, 8)
            pdf.ln()
        pdf.ln()

    if non_ai_nodes:
        format_node_table(pdf, non_ai_nodes, "Non-AI Nodes")

    # Subworkflows
    subs = workflow.get('sub_workflows', {})
    for sub_list in subs.values():
        for sub in sub_list:
            process_subworkflow(pdf, sub, 0)
    

    # Análisis
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Report Analysis", ln=True)
    pdf.ln(5)
    get_analysis(workflow, pdf)

    pdf.ln(5)
def get_analysis(workflow, pdf):

    all_nodes = gather_all_nodes(workflow)
    if all_nodes:
        slowest = get_slowest_node(all_nodes)
        
        pdf.set_font("Arial", "B", 11)
        pdf.write(5, "Slowest node: ")
        pdf.set_font("Arial", "", 11)
        pdf.write(5, f"{slowest['name']} {slowest['execution_time']}ms")
        pdf.ln(10)

        get_bottlenecks(all_nodes, pdf)
        

def write_content(text, pdf, width, height):
    if (pdf.get_string_width(text) > width):
        pdf.set_font_size(8)
    else:
        pdf.set_font_size(10)
    pdf.cell(width, height, text, border = 1)
def gather_all_nodes(workflow):
    ai_nodes = workflow['nodes'].get('ai_nodes', [])
    non_ai_nodes = workflow['nodes'].get('non_ai_nodes', [])
    all_nodes = ai_nodes + non_ai_nodes

    subs = workflow.get('sub_workflows', {})
    for sub_list in subs.values():
        for sub in sub_list:
            all_nodes += gather_all_nodes(sub)

    return all_nodes
    
def process_subworkflow(pdf, sub, level):
    indent = "  " * level
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"{indent}Sub Workflow: {sub['workflow_name']}", ln=True)
    
    
    pdf.set_font('Arial', 'B', 10)
    pdf.write(5, f"{indent}Execution ID: ")
    
    pdf.set_font('Arial', '', 10)
    pdf.write(5, f"{sub['execution_id']}")
    pdf.ln()

    pdf.set_font("Arial", "B", 10)
    pdf.write(5, "Status: "),
    pdf.set_font("Arial", "", 10)
    pdf.write(5, f"{sub['execution_status']}")
    pdf.ln()

    pdf.set_font("Arial", "B", 10)
    pdf.write(5, "Date: ")
    pdf.set_font("Arial", "", 10)
    pdf.write(5, f"{sub['execution_date']}")
    pdf.ln()

    pdf.set_font("Arial", "B", 10)
    pdf.write(5, "Duration: ")
    pdf.set_font("Arial", "", 10)
    pdf.write(5, f"{sub['execution_duration']}s")
    pdf.ln()

    pdf.set_font("Arial", "B", 10)
    pdf.write(5, "Total AI Cost ($): ")
    pdf.set_font("Arial", "", 10)
    pdf.write(5, f"{sub.get('total_cost', 'N/A')}")
    pdf.ln()

    ai_nodes = sub['nodes'].get('ai_nodes', [])
    non_ai_nodes = sub['nodes'].get('non_ai_nodes', [])
    if ai_nodes:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 10, "AI Nodes", ln=True)
        pdf.set_font("Arial", "B", 10)
        pdf.set_fill_color(200)
        pdf.cell(50, 8, "Node", border=1, fill=True)

        pdf.cell(40, 8, "Model", border=1, fill=True)
        pdf.cell(30, 8, "Tokens", border=1, fill =True)
        pdf.cell(30, 8, "Time (ms)", border=1, fill = True)
        pdf.cell(30, 8, "Cost", border=1, fill = True)
        pdf.ln()

        pdf.set_font("Arial", "", 10)
        for ai in ai_nodes:
            details = ai.get('ai_details', {})
            write_content(ai['name'][:25], pdf, 50, 8)
            write_content(details.get('model_used', 'N/A'), pdf, 40, 8)
            
            tokens = f"{details.get('prompt_tokens', 0)} + {details.get('completion_tokens', 0)}"
            write_content(tokens, pdf, 30, 8)
            write_content(str(ai.get('execution_time', 0)), pdf, 30, 8)
            write_content(details.get('cost_execution', 'N/A'), pdf, 30, 8)
            pdf.ln()
        pdf.ln()

    if non_ai_nodes:
        format_node_table(pdf, non_ai_nodes, "Non-AI Nodes")


# Generar PDF
def generar_pdf_desde_json(json_path, output_path="workflow_report.pdf"):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Execution Report", ln=True)
    pdf.ln()

    for wf in data:
        process_workflow(pdf, wf)

    pdf.output(output_path)
    print(f"PDF generado con éxito: {output_path}")

# Ejecutar

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Provide JSON file as an argument")
        print("Example: python auditor.py my_json_file.json")
    else:
        json_file = sys.argv[1]
        generar_pdf_desde_json(json_file)

