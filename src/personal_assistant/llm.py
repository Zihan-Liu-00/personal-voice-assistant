from __future__ import annotations
from mlx_lm import load, generate
from mlx_lm.sample_utils import make_sampler

class LLM:
    def __init__(self, model_path, max_tokens=512):
        self.model_path=model_path; self.max_tokens=max_tokens; self.model=None; self.tokenizer=None

    def load(self):
        if self.model is None: self.model, self.tokenizer=load(self.model_path)

    def _generate(self, messages):
        prompt=self.tokenizer.apply_chat_template(messages, add_generation_prompt=True, enable_thinking=True)
        return generate(self.model,self.tokenizer,prompt=prompt,max_tokens=self.max_tokens,sampler=make_sampler(temp=0.4),verbose=False).strip()

    def chat(self, text, context='', history=None):
        self.load()
        system='''你是一个本地个人语音助手。请用中文简洁、自然地回答，只输出最终答案，不输出隐藏推理过程。
用户明确表达的个人偏好、个人事实、待办和回复风格可能会被保存在本地 SQLite 记忆库中；如果上下文中提供了相关记忆，应据此如实回答。不要声称“不会存储或访问任何个人数据”。如果上下文没有相关记录，就明确说当前没有查到。
语音识别文本可能包含同音错别字或近似音，例如“剧身智能”通常应结合上下文理解为“具身智能”。请优先根据语义、上下文和常见专业术语进行纠正后再回答，不要把明显的 ASR 错字当成新概念。'''
        messages=[{'role':'system','content':system}]+list(history or [])
        user=text if not context else f'用户问题：{text}\n\n可参考资料：\n{context}'
        messages.append({'role':'user','content':user})
        return self._generate(messages)

    def summarize(self, transcript):
        self.load()
        messages=[{'role':'system','content':'你是对话摘要器。用中文提炼对未来有用的事实、决定、偏好、待办和未解决问题。删除寒暄和重复内容，输出简洁摘要，不要输出隐藏推理。'}, {'role':'user','content':transcript}]
        return self._generate(messages)
