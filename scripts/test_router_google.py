import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'..','src'))
from personal_assistant.llm import LLM
from personal_assistant.router import Router
from personal_assistant.google_tool import google_search

text=' '.join(sys.argv[1:]) or '搜索 SimFoundry NVIDIA'
route=Router(LLM('/Users/zihanliu/Projects/LLM/models/Qwen2.5-14B-4bit',256)).route(text)
print('ROUTE',route,flush=True)
if route['need_web_search']:
    print(google_search(route.get('query') or text),flush=True)
