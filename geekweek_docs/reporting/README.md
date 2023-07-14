# Reporting Toolchain
## A proof of concept data aggregator

### 1. Process
Currently, CyberGPT is limited to calling a single tool and returning a result. This is great, but what if we could aggregate data from multiple tools?

With limited time, our proof of concept was to implement a static suite of tools related to IP scanning that could be aggregated into a single result.

Here are the tools we used:
- Borealis
- openCTI
- Shodan
- IPAPI

#### Setup
##### The Tools
First we require a suite of tools. In this case we are using tools we developed during GeekWeek, but any tools that have similar inputs will work.

Then we can import them and iterate through them in our new tool:
```
    responses = [f"Tool: {tool.name}\n" + tool(query) for tool in ip_tools]
    report = ""
    for response in responses:
        report += f"{response}\n\n"
```

#### The Data
Once the responses from the tools have been collected we can aggregate the data using a custom LLMChain with a prompt that fits the style of report we would like.

```
tool_llm = create_llm()

template = """You have many IP analysis tools at your disposal.
Create a brief technical report based on the output provided from each tool.
The report should include brief but technical details in point form.

Report:
{report}"""
prompt_template = PromptTemplate(input_variables=["report"], template=template)
reporter_chain = LLMChain(llm=tool_llm, prompt=prompt_template, verbose=True)
```
Then within our custom tool we can simply run:
```
report = reporter_chain.run(report=report)
```

### Problems
Currently we are ingesting the data in one blob, this allows us to capture the most context for our LLM. However, we have a token limit which limits the amount of data we can ingest at once. For GPT-3.5-turbo, this is 4096 tokens. 

We experimented with a "running summary" approach to extend this limit significantly, but more experimentation is still needed to reach the level of quality of the blob approach.

### What we learned
This shows that data aggregation using LLMs is a powerful concept that needs to be further explored, especially for CyberGPT. As it stands this current proof of concept can be used to improve reporting using the tools we've created.

### Future improvements
We have two main goals for this idea moving forward:
1. Allow the LLM to pick the suite of tools
2. Generate conherent reports for larger sizes of input data

This will allow us to gather as much data as possible based on the context for any given prompt. This allows data to be more accessible for the end user without prior knowledge.