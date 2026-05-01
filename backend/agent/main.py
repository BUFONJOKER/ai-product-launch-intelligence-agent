from agent.workflow.build_workflow import build_workflow

def main():
    workflow = build_workflow(model="gpt-4")
    result = workflow.invoke({'input':"MANI"})
    print(result)

if __name__ == "__main__":
    main()