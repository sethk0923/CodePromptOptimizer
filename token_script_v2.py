import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os
import re
from typing import List

# Constants
MAX_TOKEN_LIMIT = 2500
MAX_TOKENS_PER_STEP = 500

def tokenize(text: str) -> int:
    """Count tokens using basic word splitting."""
    return len(text.split())

def optimize_text(text: str, is_code: bool = False) -> str:
    """Optimize text or code while reducing tokens."""
    if is_code:
        text = re.sub(r'#.*$', '', text, flags=re.MULTILINE)  # Python comments
        text = re.sub(r'<!--[\s\S]*?-->', '', text)  # HTML comments
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)  # CSS/JS multi-line comments
        text = re.sub(r'\s+', ' ', text.strip())  # Normalize whitespace
        return text
    
    text = re.sub(r'\s+', ' ', text.strip())
    text = re.sub(r'[^\w\s.,-]', '', text)
    return text

def extract_code_blocks(file_path: str) -> List[str]:
    """Extract key code blocks from a file based on language."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        ext = os.path.splitext(file_path)[1].lower()
        patterns = {
            '.py': [r'(def\s+\w+\s*\([^)]*\)\s*:.*?(?=\n\s*(def|class|$)))',  # Functions
                    r'(class\s+\w+(?:\([^)]*\))?\s*:.*?(?=\n\s*(def|class|$)))'],  # Classes
            '.js': [r'(function\s+\w+\s*\([^)]*\)\s*{[^}]*})',  # Functions
                    r'(class\s+\w+\s*{[^}]*})'],  # Classes
            '.html': [r'(<script\b[^>]*>[\s\S]*?</script>)',  # Script tags
                      r'(<style\b[^>]*>[\s\S]*?</style>)',  # Style tags
                      r'(<[^>]+>[\s\S]*?</[^>]+>)'],  # HTML elements
            '.css': [r'([^{}]*\{[^}]*\})',  # CSS rules
                     r'(@media[^{]*\{[^}]*\})',  # Media queries
                     r'(@keyframes[^{]*\{[^}]*\})'],  # Keyframes
            '.txt': [r'(.+)',]  # Plain text
        }
        
        file_patterns = patterns.get(ext, [r'(.+)',])
        blocks = []
        for pattern in file_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
            blocks.extend(match.group(1).strip() for match in matches if match.group(1).strip())
        
        return blocks if blocks else [content.strip()]
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return []

def generate_steps(prompt: str, code_blocks: List[str] = []) -> List[str]:
    """Generate optimized steps from prompt and code blocks."""
    optimized_prompt = optimize_text(prompt, is_code=False)
    prompt_tokens = tokenize(optimized_prompt)
    
    steps = []
    current_step = []
    current_tokens = 0
    
    # Handle prompt
    if prompt_tokens > MAX_TOKENS_PER_STEP:
        words = optimized_prompt.split()
        for word in words:
            word_tokens = tokenize(word + " ")
            if current_tokens + word_tokens > MAX_TOKENS_PER_STEP:
                if current_step:
                    steps.append(" ".join(current_step))
                    current_step = []
                    current_tokens = 0
                current_step.append(word)
                current_tokens = word_tokens
            else:
                current_step.append(word)
                current_tokens += word_tokens
    else:
        steps.append(optimized_prompt)
    
    if current_step:
        steps.append(" ".join(current_step))
    
    # Handle code blocks
    for block in [optimize_text(b, is_code=True) for b in code_blocks]:
        block_tokens = tokenize(block)
        if block_tokens > MAX_TOKENS_PER_STEP:
            lines = block.split('\n')
            sub_block = []
            sub_tokens = 0
            for line in lines:
                line_tokens = tokenize(line)
                if sub_tokens + line_tokens > MAX_TOKENS_PER_STEP:
                    steps.append("\n".join(sub_block))
                    sub_block = [line]
                    sub_tokens = line_tokens
                else:
                    sub_block.append(line)
                    sub_tokens += line_tokens
            if sub_block:
                steps.append("\n".join(sub_block))
        else:
            steps.append(block)
    
    # Enforce total token limit
    total_tokens = sum(tokenize(step) for step in steps)
    if total_tokens > MAX_TOKEN_LIMIT:
        truncated_steps = []
        total_tokens = 0
        for step in steps:
            step_tokens = tokenize(step)
            if total_tokens + step_tokens <= MAX_TOKEN_LIMIT:
                truncated_steps.append(step)
                total_tokens += step_tokens
            else:
                break
        steps = truncated_steps
    
    return steps if steps else ["No content to process"]

class TokenizerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Code Prompt Optimizer")
        master.geometry("600x400")
        
        tk.Label(master, text="Enter Your Prompt:").pack(pady=5)
        self.prompt_text = tk.Text(master, height=4, width=60)
        self.prompt_text.pack(pady=5)

        tk.Label(master, text="Select Code File (optional):").pack(pady=5)
        file_frame = tk.Frame(master)
        file_frame.pack(pady=5)
        self.file_path_var = tk.StringVar()
        tk.Entry(file_frame, textvariable=self.file_path_var, width=40).pack(side=tk.LEFT)
        tk.Button(file_frame, text="Browse", command=self.browse_file).pack(side=tk.LEFT, padx=5)

        tk.Button(master, text="Optimize Steps", command=self.optimize).pack(pady=10)
        self.output_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=60, height=15)
        self.output_text.pack(pady=10, padx=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Code files", "*.py;*.js;*.html;*.css;*.txt"), 
                                                         ("All files", "*.*")])
        if file_path:
            self.file_path_var.set(file_path)

    def optimize(self):
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        file_path = self.file_path_var.get()
        
        if not prompt:
            messagebox.showerror("Error", "Please enter a prompt.")
            return
        
        code_blocks = extract_code_blocks(file_path) if file_path and os.path.exists(file_path) else []
        steps = generate_steps(prompt, code_blocks)
        
        self.output_text.delete("1.0", tk.END)
        output = "Optimized Steps:\n\n"
        for i, step in enumerate(steps, 1):
            tokens = tokenize(step)
            output += f"Step {i} (Tokens: {tokens}):\n{step}\n\n"
        self.output_text.insert(tk.END, output)

def main():
    root = tk.Tk()
    app = TokenizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()