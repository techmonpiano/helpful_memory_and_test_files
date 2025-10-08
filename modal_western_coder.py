"""
Modal Western Coding Models Deployment
Supports three Western/European coding models:
1. Mistral Codestral 25.01 (22B) - Latest coding model from France
2. Mistral Codestral Mamba 7B - Optimized code completion model
3. Microsoft Phi-4 (14B) - Strong reasoning and multimodal coding

Usage:
- Set MODEL_TYPE environment variable to choose model:
  - "codestral-25" (default)
  - "codestral-mamba" 
  - "phi4"
- Deploy with: modal deploy modal_western_coder.py
"""

import os
import json
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

import modal

# Modal app configuration
app = modal.App("western-coder")

# Model configuration
MODEL_TYPE = os.environ.get("MODEL_TYPE", "codestral-25")

class ModelType(Enum):
    CODESTRAL_25 = "codestral-25"
    CODESTRAL_MAMBA = "codestral-mamba"
    PHI4 = "phi4"

@dataclass
class ModelConfig:
    name: str
    model_id: str
    gpu_type: str
    gpu_count: int
    container_image: str
    max_context: int
    description: str

# Model configurations
MODEL_CONFIGS = {
    ModelType.CODESTRAL_25: ModelConfig(
        name="Mistral Codestral 25.01",
        model_id="mistralai/Codestral-25.01-Instruct",
        gpu_type="H100",
        gpu_count=1,
        container_image="pytorch/pytorch:2.1.0-cuda12.1-cudnn8-devel",
        max_context=256000,
        description="Latest Mistral coding model with 256k context"
    ),
    ModelType.CODESTRAL_MAMBA: ModelConfig(
        name="Mistral Codestral Mamba 7B",
        model_id="mistralai/Codestral-Mamba-7B-v0.1",
        gpu_type="A100",
        gpu_count=1,
        container_image="pytorch/pytorch:2.1.0-cuda12.1-cudnn8-devel",
        max_context=32000,
        description="Optimized Mamba architecture for code completion"
    ),
    ModelType.PHI4: ModelConfig(
        name="Microsoft Phi-4",
        model_id="microsoft/phi-4",
        gpu_type="A100",
        gpu_count=1,
        container_image="pytorch/pytorch:2.1.0-cuda12.1-cudnn8-devel",
        max_context=16000,
        description="Microsoft's latest small language model for coding"
    )
}

def get_current_config() -> ModelConfig:
    """Get the current model configuration based on MODEL_TYPE env var."""
    model_type = ModelType(MODEL_TYPE)
    return MODEL_CONFIGS[model_type]

# Container image setup
current_config = get_current_config()

image = modal.Image.from_registry(
    current_config.container_image,
    add_python="3.11"
).pip_install([
    "torch==2.1.0",
    "transformers==4.36.0",
    "accelerate==0.24.1",
    "bitsandbytes==0.41.3",
    "safetensors==0.4.0",
    "sentencepiece==0.1.99",
    "protobuf==4.25.0",
    "fastapi==0.104.1",
    "uvicorn==0.24.0",
    "pydantic==2.5.0",
    "huggingface_hub==0.19.4",
    "tokenizers==0.15.0"
])

# Base model class
class BaseModel:
    def __init__(self, config: ModelConfig):
        self.config = config
        self.model = None
        self.tokenizer = None
    
    def load_model(self):
        """Override in subclasses"""
        raise NotImplementedError
    
    def generate_code(self, prompt: str, max_tokens: int = 512, temperature: float = 0.1) -> str:
        """Override in subclasses"""
        raise NotImplementedError
    
    def format_prompt(self, instruction: str, code_context: str = "") -> str:
        """Format prompt for the specific model"""
        if code_context:
            return f"### Instruction:\n{instruction}\n\n### Code Context:\n{code_context}\n\n### Response:"
        return f"### Instruction:\n{instruction}\n\n### Response:"

@app.cls(
    gpu=current_config.gpu_type,
    image=image,
    allow_concurrent_inputs=10,
)
class WesternCoder:
    """Main class for Western coding models deployment"""
    
    def __init__(self):
        self.current_model = None
        self.model_type = ModelType(MODEL_TYPE)
        self.config = MODEL_CONFIGS[self.model_type]
        
    @modal.enter()
    def load_model(self):
        """Load the selected model based on MODEL_TYPE"""
        print(f"Loading {self.config.name}...")
        
        if self.model_type == ModelType.CODESTRAL_25:
            self.current_model = CodestralModel(self.config) 
        elif self.model_type == ModelType.CODESTRAL_MAMBA:
            self.current_model = CodestralMambaModel(self.config)
        elif self.model_type == ModelType.PHI4:
            self.current_model = Phi4Model(self.config)
            
        self.current_model.load_model()
        print(f"✅ {self.config.name} loaded successfully!")
        
    @modal.method()
    def info(self) -> Dict:
        """Get model information"""
        return {
            "model_name": self.config.name,
            "model_id": self.config.model_id,
            "max_context": self.config.max_context,
            "description": self.config.description,
            "gpu_type": self.config.gpu_type
        }
    
    @modal.method()
    def generate_code(
        self,
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.1,
        top_p: float = 0.9
    ) -> Dict:
        """Generate code using the loaded model"""
        try:
            result = self.current_model.generate_code(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return {
                "model": self.config.name,
                "prompt": prompt,
                "generated_code": result,
                "success": True
            }
        except Exception as e:
            return {
                "model": self.config.name,
                "prompt": prompt,
                "error": str(e),
                "success": False
            }
    
    @modal.method()
    def code_completion(self, code_context: str, cursor_position: str = "") -> Dict:
        """Complete code at cursor position"""
        prompt = f"Complete the following code:\n\n{code_context}\n\n# Complete from here: {cursor_position}"
        return self.generate_code(prompt, max_tokens=256, temperature=0.05)
    
    @modal.method()
    def explain_code(self, code: str) -> Dict:
        """Explain what the code does"""
        prompt = f"Explain what this code does:\n\n```\n{code}\n```\n\nExplanation:"
        return self.generate_code(prompt, max_tokens=400, temperature=0.1)
    
    @modal.method()
    def fix_bug(self, buggy_code: str, error_message: str = "") -> Dict:
        """Fix bugs in code"""
        prompt = f"Fix the bug in this code:\n\n```\n{buggy_code}\n```\n"
        if error_message:
            prompt += f"\nError message: {error_message}\n"
        prompt += "\nFixed code:"
        return self.generate_code(prompt, max_tokens=600, temperature=0.1)
    
    @modal.method()
    def review_code(self, code: str) -> Dict:
        """Review code for improvements"""
        prompt = f"Review this code and suggest improvements:\n\n```\n{code}\n```\n\nCode review:"
        return self.generate_code(prompt, max_tokens=500, temperature=0.2)

# Individual model implementations

class CodestralModel(BaseModel):
    """Mistral Codestral 25.01 implementation"""
    
    def load_model(self):
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        
        print(f"Loading {self.config.name} from {self.config.model_id}...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config.model_id,
            trust_remote_code=True,
            use_fast=True
        )
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.config.model_id,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True,
            low_cpu_mem_usage=True,
            load_in_4bit=True  # Use 4-bit quantization for efficiency
        )
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
    
    def generate_code(self, prompt: str, max_tokens: int = 512, temperature: float = 0.1) -> str:
        import torch
        
        # Format prompt for Codestral
        formatted_prompt = f"<s>[INST] {prompt} [/INST]"
        
        inputs = self.tokenizer.encode(formatted_prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=temperature > 0,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                repetition_penalty=1.1
            )
        
        response = self.tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
        return response.strip()


class CodestralMambaModel(BaseModel):
    """Mistral Codestral Mamba 7B implementation"""
    
    def load_model(self):
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        
        print(f"Loading {self.config.name} from {self.config.model_id}...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config.model_id,
            trust_remote_code=True
        )
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.config.model_id,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
    
    def generate_code(self, prompt: str, max_tokens: int = 512, temperature: float = 0.1) -> str:
        import torch
        
        # Mamba models work well with simple prompts
        inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=temperature > 0,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
        
        response = self.tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
        return response.strip()


class Phi4Model(BaseModel):
    """Microsoft Phi-4 implementation"""
    
    def load_model(self):
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        
        print(f"Loading {self.config.name} from {self.config.model_id}...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config.model_id,
            trust_remote_code=True
        )
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.config.model_id,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True,
            low_cpu_mem_usage=True,
            load_in_4bit=True  # 4-bit quantization for efficiency
        )
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
    
    def generate_code(self, prompt: str, max_tokens: int = 512, temperature: float = 0.1) -> str:
        import torch
        
        # Phi-4 uses a specific chat format
        formatted_prompt = f"<|user|>\n{prompt}<|end|>\n<|assistant|>\n"
        
        inputs = self.tokenizer.encode(formatted_prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=temperature > 0,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                repetition_penalty=1.05
            )
        
        response = self.tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
        return response.strip()


# OpenAI-compatible API endpoint
@app.function(image=image)
@modal.web_endpoint(method="POST", label=f"western-coder-{MODEL_TYPE}")
def generate_completion(data: dict):
    """OpenAI-compatible completion endpoint"""
    
    # Create model instance
    coder = WesternCoder()
    
    # Extract OpenAI-style parameters
    prompt = data.get("prompt", "")
    messages = data.get("messages", [])
    max_tokens = data.get("max_tokens", 512)
    temperature = data.get("temperature", 0.1)
    
    # Handle both prompt and messages format
    if messages:
        # Convert messages to prompt
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
    
    if not prompt:
        return {"error": "No prompt or messages provided"}
    
    # Generate response
    result = coder.generate_code.remote(
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature
    )
    
    if result["success"]:
        return {
            "id": f"western-coder-{MODEL_TYPE}",
            "object": "text_completion",
            "model": result["model"],
            "choices": [{
                "text": result["generated_code"],
                "index": 0,
                "logprobs": None,
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": len(result["generated_code"].split()),
                "total_tokens": len(prompt.split()) + len(result["generated_code"].split())
            }
        }
    else:
        return {"error": result["error"]}


# Web interface for easy testing
@app.function(image=image)
@modal.web_endpoint(method="GET", label=f"western-coder-ui-{MODEL_TYPE}")
def web_ui():
    """Simple web UI for testing the models"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Western Coder - {get_current_config().name}</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
            textarea {{ width: 100%; height: 100px; margin: 10px 0; }}
            button {{ background: #007cba; color: white; padding: 10px 20px; border: none; cursor: pointer; }}
            .response {{ background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }}
            .info {{ background: #e7f3ff; padding: 10px; margin: 10px 0; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <h1>Western Coder - {get_current_config().name}</h1>
        <div class="info">
            <strong>Model:</strong> {get_current_config().description}<br>
            <strong>Max Context:</strong> {get_current_config().max_context:,} tokens<br>
            <strong>GPU:</strong> {get_current_config().gpu_type}
        </div>
        
        <h3>Code Generation</h3>
        <textarea id="prompt" placeholder="Enter your coding prompt here...">Write a Python function to calculate fibonacci numbers</textarea>
        <br>
        <button onclick="generateCode()">Generate Code</button>
        
        <div id="response" class="response" style="display:none;">
            <h4>Generated Code:</h4>
            <pre id="code"></pre>
        </div>

        <script>
            async function generateCode() {{
                const prompt = document.getElementById('prompt').value;
                const responseDiv = document.getElementById('response');
                const codeElement = document.getElementById('code');
                
                responseDiv.style.display = 'block';
                codeElement.textContent = 'Generating...';
                
                try {{
                    const response = await fetch('/generate_completion', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ prompt: prompt, max_tokens: 512, temperature: 0.1 }})
                    }});
                    
                    const data = await response.json();
                    
                    if (data.choices) {{
                        codeElement.textContent = data.choices[0].text;
                    }} else {{
                        codeElement.textContent = 'Error: ' + (data.error || 'Unknown error');
                    }}
                }} catch (error) {{
                    codeElement.textContent = 'Error: ' + error.message;
                }}
            }}
        </script>
    </body>
    </html>
    """
    return modal.Response(html, headers={"Content-Type": "text/html"})


if __name__ == "__main__":
    print(f"Western Coder - {get_current_config().name}")
    print(f"Model ID: {get_current_config().model_id}")
    print(f"Description: {get_current_config().description}")
    print("\nTo deploy this model:")
    print(f"MODEL_TYPE={MODEL_TYPE} modal deploy modal_western_coder.py")
    print("\nAvailable models:")
    for model_type, config in MODEL_CONFIGS.items():
        print(f"- {model_type.value}: {config.name} ({config.description})")