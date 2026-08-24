from __future__ import annotations
import json, re
from .llm import LLM

SEARCH_WORDS=('搜索','查一下','查找','网上','最新','今天','现在','新闻','价格','天气','github','官网')

class Router:
    def __init__(self,llm): self.llm=llm
    def route(self,text):
        prompt='''判断用户是否需要联网搜索，只输出 JSON，不要 Markdown：{"need_web_search":true或false,"query":"搜索词"}。需要联网：最新、今天、现在、新闻、价格、天气、Google、GitHub、官网或用户明确要求搜索。'''
        try:
            raw=self.llm.chat(prompt+'\n用户：'+text)
            match=re.search(r'\{.*\}',raw,re.S)
            data=json.loads(match.group(0)) if match else {}
            if isinstance(data.get('need_web_search'),bool): return data
        except Exception: pass
        return {'need_web_search':any(w.lower() in text.lower() for w in SEARCH_WORDS),'query':text}
