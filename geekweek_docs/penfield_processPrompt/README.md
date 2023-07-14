# Penfield.AI ProcessPrompt

## Problem Definition

A key issue with generative AI is its tendency to form incorrect assumptions or fall short when it comes to resolving problems requiring an understanding of customer-specific processes and contexts. This issue becomes more pronounced within the field of cybersecurity where processes are often heavily reliant on context. For instance, in a banking setting, the strategy for addressing the same type of cyber attack may differ depending on whether it targets an online banking server or a rewards server, owing to variations in processes, technological stacks, and business criticalities. Furthermore, analysts frequently rely on intuition to resolve issues, which may lead to insufficient documentation, thus obstructing automation and cross-training efforts.

## The Solution

ProcessPrompt aims to incorporate your specific process and tool information into any Copilot. This enables Language Learning Models (LLMs) to navigate and resolve issues efficiently and securely, effectively grounding your LLM. ProcessPrompts are generated using a lightweight browser extension named Pathfinder, which archives data in a Kubernetes instance deployable in your private cloud or bare metal server.

This solution encourages LLMs to learn from your analysts' best practices and emulate their decision-making processes using your tools. This process allows analysts to examine the tasks and thought processes of LLMs, freeing up their time for more significant responsibilities.

### Key Components

The key components of ProcessPrompt encompass:

1. Pathfinder Browser Extension
   This lightweight extension facilitates the capture of interaction data such as clicks, queries, and copy/paste actions on authorized web-based tools. The data collected from this extension is utilized to create Processes with Decision bounds, which are then displayed through the ProcessPrompt API.

2. ProcessPrompt API
   The ProcessPrompt API uses an alert title as input and delivers step-by-step instructions mined by ProcessPrompt.

3. Custom Agent using Langchain
   A customized Langchain Agent has been created using the REACT framework to logically reason and perform tasks. The REACT framework has been enhanced to ground its decision-making and thought processes from ProcessPrompt instructions, introducing safeguard mechanisms to ensure AI-driven tasks align with your processes, utilizing your tools.

4. Custom Tools
   Two proprietary tools have been developed to carry out analysis via ProcessPrompt: The Abuse IP DB for investigating IP reputation, and the AssemblyLine tool for analyzing potential malicious files.

## Step by Step Process

Kindly refer to documentation on ProcessPrompt UI.

## Lessons Learned

Our approach experimented with constructing a custom LangChain Agent using the REACT framework. A crucial learning point was understanding how to develop and incorporate existing process data into the REACT framework, enabling it to adhere to your processes without jeopardizing its ability to reason, decide, experiment, and learn safely.

We believe that grounding Copilots in this way is key to their effectiveness in the realm of cybersecurity.
