"""Minimal OpenAI-compatible adapter for MLX Qwen, used by Browser Use."""
from __future__ import annotations
import json, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from mlx_lm import load, generate
from mlx_lm.sample_utils import make_sampler

MODEL=os.getenv('ASSISTANT_MODEL','/Users/zihanliu/Projects/LLM/models/Qwen2.5-14B-4bit')
PORT=int(os.getenv('ASSISTANT_LLM_PORT','8091'))
model, tokenizer = load(MODEL)

def complete(messages):
    prompt=tokenizer.apply_chat_template(messages,add_generation_prompt=True,enable_thinking=True)
    return generate(model,tokenizer,prompt=prompt,max_tokens=1024,sampler=make_sampler(temp=0.2),verbose=False).strip()

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def do_GET(self):
        if self.path=='/health': return self.reply({'ok':True,'model':MODEL})
        self.reply({'error':'not found'},404)
    def reply(self,obj,status=200):
        data=json.dumps(obj,ensure_ascii=False).encode(); self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_POST(self):
        try:
            size=int(self.headers.get('Content-Length','0')); body=json.loads(self.rfile.read(size)); answer=complete(body.get('messages',[]))
            self.reply({'id':'qwen-local','object':'chat.completion','choices':[{'index':0,'message':{'role':'assistant','content':answer},'finish_reason':'stop'}],'model':'qwen-local'})
        except Exception as e: self.reply({'error':str(e)},500)

if __name__=='__main__':
    print(f'local LLM API: http://127.0.0.1:{PORT}/v1',flush=True); ThreadingHTTPServer(('127.0.0.1',PORT),Handler).serve_forever()
