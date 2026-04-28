# SL-Agent
AI-Agent for searching information and better studying


## Architectory:

Instructions - for spaces, general info about user (can be changed via settings)
Database 1 - Context of conversation 

## Should contain:
Web_crawler (Script for parsing info from the web for better answers)
RAG-based answers (With dynamic memory system)
LLM (For starters: GigaChat)
Search engine (Let it be: DuckDuckGoAPI) 
User Space Function (Ability to create spaces, which are basically Perplexity's function)
Various Parsers: (
    Docx Parser
    Pdf Parser
    Image Parser (text)
)


## Alghoritm of work:
1) Get a prompt from the user
2) Get LLM to generate search topics for the prompt and find info on the topic 
3) Add Instructions (Space + General Info) to the prompt + gotten info (2) + info from files + context
4) Give everything to LLM and generate answer
5) Give out answer


   
## Why is it a Web Application?

### Performance

For such kind of project, the UI does not need maximum native rendering power; it needs to display live text, status, logs, and controls with low perceived latency. Real-time dashboards work well when they prioritize responsiveness, highlight changes clearly, and avoid overloading the user, which fits a browser-based interface very naturally

### User Comfort

From the user’s perspective, a web app is more comfortable because there is no installation barrier, no platform-specific setup, and no separate update process. Users can open it in a browser and start working immediately, which lowers friction and makes the tool feel simpler and safer to try.