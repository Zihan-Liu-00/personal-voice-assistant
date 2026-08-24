from __future__ import annotations
import asyncio
from browser_use import Agent, ChatOpenAI, BrowserProfile

async def google_search(query: str) -> str:
    llm=ChatOpenAI(model='qwen-local',api_key='local',base_url='http://127.0.0.1:8091/v1',dont_force_structured_output=True,max_completion_tokens=1024,reasoning_effort='none')
    task=f'''打开 Google 并搜索：{query}
严格要求：
1. 只能执行浏览器操作，不要编造搜索结果。
2. 每一步只输出 Browser Use 规定的合法动作 JSON；禁止输出 Markdown、解释文字或自定义字段。
3. 搜索完成后，最终只返回前 5 条结果的标题、URL 和一句摘要，使用 JSON 数组格式：[{{"title":"...","url":"...","snippet":"..."}}]。
4. 如果动作格式解析失败，立即重新推理并输出合法格式。'''
    profile=BrowserProfile(headless=False,keep_alive=True,enable_default_extensions=False,disable_security=False)
    agent=Agent(task=task,llm=llm,browser_profile=profile,max_failures=5,max_actions_per_step=1,use_vision=False,enable_planning=False,directly_open_url=True)
    history=await agent.run(max_steps=20)
    return history.final_result()

def search(query): return asyncio.run(google_search(query))
