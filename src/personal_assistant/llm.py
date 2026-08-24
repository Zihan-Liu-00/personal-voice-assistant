from __future__ import annotations
from mlx_lm import load, generate
from mlx_lm.sample_utils import make_sampler

class LLM:
    def __init__(self, model_path, max_tokens=512):
        self.model_path=model_path; self.max_tokens=max_tokens; self.model=None; self.tokenizer=None

    def _load(self):
        if self.model is None: self.model, self.tokenizer=load(self.model_path)

    def chat(self, text, context=''):
        self._load()
        system='你是一个本地个人语音助手。请用中文简洁、自然地回答。只输出最终答案，不输出隐藏推理过程。'
        user=text if not context else f'''用户问题：{text}\n\n以下是通过 Google 获取的网页结果。请只根据这些结果回答，区分事实与推断；如果结果不足以回答，请明确说明。保留关键来源 URL。\n\n网页结果：\n{context}'''
        messages=[{'role':'system','content':system}, {'role':'user','content':user}]
        prompt=self.tokenizer.apply_chat_template(messages, add_generation_prompt=True, enable_thinking=True)
        return generate(self.model,self.tokenizer,prompt=prompt,max_tokens=self.max_tokens,sampler=make_sampler(temp=0.4),verbose=False).strip()
