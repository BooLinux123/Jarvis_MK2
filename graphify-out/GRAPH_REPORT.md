# Graph Report - Jarvis_MK2  (2026-11-16)

## Corpus Check
- Corpus is ~1,976 words - fits in a single context window. You may not need a graph.

## Summary
- 54 nodes · 69 edges · 8 communities (3 shown, 5 thin omitted)
- Extraction: 77% EXTRACTED · 23% INFERRED · 0% AMBIGUOUS · INFERRED: 16 edges (avg confidence: 0.84)
- Token cost: 43,360 input · 0 output

## Community Hubs (Navigation)
- Jarvis Persona and Tool Policy
- Search Provider Abstraction
- Chat Loop and Ollama Client
- Requests Dependency Stack
- Weather Provider and Geocoding
- Time and Clock Utilities

## God Nodes (most connected - your core abstractions)
1. `SearchQuery` - 7 edges
2. `requests 2.34.2` - 6 edges
3. `send_to_ollama()` - 5 edges
4. `TavilyProvider` - 5 edges
5. `WeatherProvider` - 5 edges
6. `web_search Tool` - 5 edges
7. `handle_response()` - 4 edges
8. `Jarvis System Prompt` - 4 edges
9. `geocode()` - 3 edges
10. `get_time()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `web_search Tool` --conceptually_related_to--> `python-dotenv 1.2.4`  [INFERRED]
  Modelfile.txt → requirements.txt
- `web_search Tool` --conceptually_related_to--> `requests 2.34.2`  [INFERRED]
  Modelfile.txt → requirements.txt
- `weather_search Tool` --conceptually_related_to--> `requests 2.34.2`  [INFERRED]
  Modelfile.txt → requirements.txt

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Jarvis Tool-Use Discipline Policy** — modelfile_tool_specificity_rule, modelfile_no_search_preamble_rule, modelfile_ambiguity_clarification_rule, modelfile_capability_boundary_rule, modelfile_web_search_tool [EXTRACTED 1.00]
- **requests HTTP Dependency Stack** — requirements_requests, requirements_urllib3, requirements_certifi, requirements_charset_normalizer, requirements_idna [INFERRED 0.95]

## Communities (8 total, 5 thin omitted)

### Community 0 - "Jarvis Persona and Tool Policy"
Cohesion: 0.20
Nodes (6): Lights and Music Device Control, Jarvis System Prompt, qwen3:14b Base Model, weather_search Tool, web_search Tool, python-dotenv 1.2.4

### Community 3 - "Chat Loop and Ollama Client"
Cohesion: 0.60
Nodes (4): chat(), handle_response(), send_to_ollama(), trim_history()

### Community 5 - "Requests Dependency Stack"
Cohesion: 0.40
Nodes (5): certifi 2026.10.23, charset-normalizer 3.5.2, idna 3.20, requests 2.34.2, urllib3 2.8.0

## Knowledge Gaps
- **5 isolated node(s):** `python-dotenv 1.2.4`, `urllib3 2.8.0`, `certifi 2026.10.23`, `charset-normalizer 3.5.2`, `idna 3.20`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 23 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SearchQuery` connect `Search Provider Abstraction` to `Search Module and Dispatch`, `Weather Provider and Geocoding`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `requests 2.34.2` (e.g. with `weather_search Tool` and `web_search Tool`) actually correct?**
  _`requests 2.34.2` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `python-dotenv 1.2.4`, `urllib3 2.8.0`, `certifi 2026.10.23` to the rest of the system?**
  _5 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Why does `TavilyProvider` connect `Search Provider Abstraction` to `Search Module and Dispatch`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Why does `WeatherProvider` connect `Weather Provider and Geocoding` to `Search Provider Abstraction`, `Search Module and Dispatch`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._