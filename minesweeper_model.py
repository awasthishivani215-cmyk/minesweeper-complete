#!/usr/bin/python3
"""
Minesweeper Model - Optimized with Qwen2.5 (400MB)
Best balance of size and intelligence
"""
import time
import torch
from typing import Optional, Union, List

class MinesweeperAgent(object):
    """Professional Minesweeper agent with mine detection"""
    
    def __init__(self, **kwargs):
        """
        Initialize with Qwen2.5-0.5B - Best 400MB model for logic
        """
        print("\n" + "="*70)
        print("🎮 PROFESSIONAL MINESWEEPER AGENT")
        print("="*70)
        
        # Using Qwen2.5-0.5B-Instruct - 400MB, excellent reasoning
        self.model_name = "Qwen/Qwen2.5-0.5B-Instruct"
        
        print(f"📦 Model: Qwen2.5-0.5B-Instruct")
        print(f"📊 Size: 400MB - Perfect balance of speed and intelligence")
        print(f"⚡ Features: Mine detection, safe cell analysis, flagging")
        print("="*70 + "\n")
        
        # Import transformers
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        # Load tokenizer
        print("📥 Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            padding_side="left"
        )
        
        # Set pad token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        print("✓ Tokenizer loaded")
        
        # Load model (optimized for CPU)
        print("\n📥 Loading model (first time download: 400MB)...")
        start_time = time.time()
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map="cpu",
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        load_time = time.time() - start_time
        
        # Model info
        param_count = sum(p.numel() for p in self.model.parameters())
        print(f"✓ Model loaded in {load_time:.1f}s")
        print(f"✓ Parameters: {param_count/1e9:.2f}B")
        print(f"✓ Running on CPU - Ready for mine detection")
        print("="*70 + "\n")

    def generate_response(self, message: str, **kwargs) -> tuple:
        """Generate intelligent response for mine detection"""
        
        tgps_show = kwargs.get("tgps_show", False)
        
        # Qwen2.5 optimized prompt format
        prompt = f"""<|im_start|>system
You are a Minesweeper expert. Analyze the board carefully and choose the BEST move.
Look for safe cells and potential mines. Output ONLY row and column numbers.
Example: 2 3<|im_end|>
<|im_start|>user
{message}<|im_end|>
<|im_start|>assistant
"""
        
        # Tokenize
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
        
        # Generate
        start_time = time.time()
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=15,
                do_sample=False,
                temperature=0.1,
                pad_token_id=self.tokenizer.pad_token_id
            )
        gen_time = time.time() - start_time
        
        # Decode
        response = self.tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
        response = response.strip()
        
        token_count = outputs.shape[1] - inputs['input_ids'].shape[1]
        
        if tgps_show:
            print(f"🎯 AI Analysis: '{response}'")
        
        return response, token_count, gen_time