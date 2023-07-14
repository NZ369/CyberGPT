## Bullet point summary for writing docs
### The Process

Tools developed:

- Document Retrieval
    - Long-term memory storage
    - Large, reliable information retrieval database
    - Kendra or Pinecone?
- Toolchain
    - LLMs are context-aware
    - Instead of a single tool, let the AI choose the best suite of tools for the job
    - Data aggregation
    - Furthers automation and hands-off approach
    - Static suite of tools for PoC

### Problems encountered

- Kendra networking
- Kendra context length (query vs request api)
- Custom Kendra retriever
- AWS out of date lambda libraries
- GPT-3.5 token length
- Pinecone db state
- Base agent information loss

### What we learned

- Using Azure API gateways and lambda functions as a proxy to Kendra
- Kendra request API (and how important context length is)
- Building custom retrievers
- LangChain chains, agents, and more

### What we achieved

- Document Retrieval with Kendra
- Reporting from a suite of tools
- API-related tools (Borealis, IPAPI, openCTI, Shodan, MITRE)

### Future work

- Arbitrary tool calling and report generation
- Data source selection in Kendra
- More API tools
- Local LLM models
- Larger LLM models