import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import tiktoken
import os
import requests
import logging
import re
from nltk.corpus import stopwords
from typing import List

# Set up logging
logging.basicConfig(filename='optimizer.log', level=logging.DEBUG,
                   format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
DEFAULT_MODEL = "gpt-3.5-turbo"
MAX_TOKEN_LIMIT = 130_000
MAX_TOKENS_PER_STEP = 500

def initialize_tiktoken():
    """Initialize tiktoken with robust fallback and diagnostics."""
    try:
        # First attempt: Use model-specific encoding
        enc = tiktoken.encoding_for_model('gpt-3.5-turbo')
        logging.info("Successfully initialized tiktoken with gpt-3.5-turbo encoding")
        return enc
    except Exception as e1:
        logging.warning(f"Failed to load gpt-3.5-turbo encoding: {str(e1)}")
        try:
            # Second attempt: Directly load cl100k_base
            enc = tiktoken.get_encoding("cl100k_base")
            logging.info("Successfully initialized tiktoken with cl100k_base encoding")
            return enc
        except Exception as e2:
            logging.warning(f"Failed to load cl100k_base encoding: {str(e2)}")
            # Check if cache directory exists and is writable
            cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "tiktoken")
            try:
                os.makedirs(cache_dir, exist_ok=True)
                if not os.access(cache_dir, os.W_OK):
                    raise PermissionError(f"Cache directory {cache_dir} is not writable")
                logging.info(f"Cache directory verified: {cache_dir}")
                
                # Attempt to download the encoding file
                registry_url = "https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken"
                response = requests.get(registry_url, timeout=10)
                response.raise_for_status()  # Raise exception for bad status codes
                encoding_file = os.path.join(cache_dir, "cl100k_base.tiktoken")
                with open(encoding_file, "wb") as f:
                    f.write(response.content)
                logging.info(f"Downloaded cl100k_base.tiktoken to {encoding_file}")
                
                # Try loading again after download
                enc = tiktoken.get_encoding("cl100k_base")
                logging.info("Successfully initialized tiktoken after downloading cl100k_base")
                return enc
            except requests.RequestException as e3:
                logging.error(f"Failed to download cl100k_base.tiktoken: {str(e3)}")
                error_msg = "Failed to download tiktoken encoding.\n"
                error_msg += "Check your internet connection or try:\n"
                error_msg += "pip install --force-reinstall tiktoken==0.8.0"
            except PermissionError as e4:
                logging.error(f"Permission error: {str(e4)}")
                error_msg = f"Permission denied writing to {cache_dir}.\n"
                error_msg += "Run the app with elevated privileges or change the cache location."
            except Exception as e5:
                logging.error(f"Unexpected error after download attempt: {str(e5)}")
                error_msg = "Failed to initialize tiktoken.\n"
                error_msg += "Try: pip uninstall tiktoken && pip install tiktoken==0.8.0"

            messagebox.showerror("Tiktoken Error", error_msg)
            raise Exception("Tiktoken initialization failed") from e5

def tokenize(text: str) -> int:
    """Count tokens in the given text."""
    try:
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception as e:
        logging.error(f"Token counting failed: {str(e)}")
        return len(text.split())  # Fallback to word count

def optimize_text(text: str, is_code: bool = False) -> str:
    """Optimizes text or preserves code structure while reducing tokens."""
    if is_code:
        # Minimize code while preserving syntax (remove comments, extra whitespace)
        text = re.sub(r'#.*$', '', text, flags=re.MULTILINE)  # Remove Python comments
        text = re.sub(r'//.*$', '', text, flags=re.MULTILINE)  # Remove JS single-line comments
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)  # Remove JS multi-line comments
        text = re.sub(r'\s+', ' ', text.strip())  # Normalize whitespace
        return text
    
    try:
        # Non-code text: remove fluff
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'[^\w\s.,-]', '', text)
        
        # Simple sentence splitting without punkt_tab
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        if not sentences:
            return text
        
        try:
            stop_words = set(stopwords.words('english'))
        except LookupError:
            logging.warning("Stopwords not found, using basic text optimization")
            stop_words = set()
        
        optimized_sentences = []
        for sentence in sentences:
            # Simple word tokenization without punkt_tab
            words = [w.strip() for w in sentence.split() if w.strip()]
            filtered_words = [w for w in words if w.lower() not in stop_words and w.isalnum()]
            if filtered_words:
                optimized_sentences.append(" ".join(filtered_words))
        
        return " ".join(optimized_sentences)
    except Exception as e:
        logging.error(f"Text optimization failed: {str(e)}")
        # Return original text if optimization fails
        return text

def extract_code_blocks(file_path: str) -> List[str]:
    """Extract code blocks from a file with intelligent parsing for multiple languages."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Determine file type from extension
        ext = os.path.splitext(file_path)[1].lower()
        
        # Language-specific patterns
        patterns = {
            # Python patterns
            '.py': [
                r'(def\s+\w+\s*\([^)]*\)\s*:(?:\s*"""[\s\S]*?""")?\s*(?:(?!\ndef\s+|\sclass\s+).*\n?)+)',  # Functions
                r'(class\s+\w+(?:\([^)]*\))?\s*:(?:\s*"""[\s\S]*?""")?\s*(?:(?!\sclass\s+).*\n?)+)',  # Classes
                r'(if\s+__name__\s*==\s*["\']__main__[\'"]\s*:(?:\s*(?!def|class).*\n?)+)',  # Main block
                r'([^=\s]+\s*=\s*(?:(?!\ndef\s+|\sclass\s+).*\n?)+)'  # Assignments
            ],
            # JavaScript patterns
            '.js': [
                r'(function\s+\w+\s*\([^)]*\)\s*{[^}]*})',  # Named functions
                r'(const|let|var)\s+\w+\s*=\s*function\s*\([^)]*\)\s*{[^}]*}',  # Function assignments
                r'(class\s+\w+\s*{[^}]*})',  # Classes
                r'(\w+\s*=\s*{[^}]*})',  # Object literals
                r'(export\s+(?:default\s+)?(?:function|class|const|let|var)[^;]*;?)'  # Exports
            ],
            # HTML patterns
            '.html': [
                r'(<script\b[^>]*>[\s\S]*?</script>)',  # Script tags
                r'(<style\b[^>]*>[\s\S]*?</style>)',  # Style tags
                r'(<template\b[^>]*>[\s\S]*?</template>)',  # Template tags
                r'(<[^>]+>[\s\S]*?</[^>]+>)',  # HTML elements
                r'(<!--[\s\S]*?-->)'  # Comments
            ],
            # CSS patterns
            '.css': [
                r'([^{}]*\{[^}]*\})',  # CSS rules
                r'(@media[^{]*\{[^}]*\})',  # Media queries
                r'(@keyframes[^{]*\{[^}]*\})',  # Keyframes
                r'(@import[^;]*;)',  # Imports
                r'(@font-face\s*\{[^}]*\})'  # Font face declarations
            ],
            # TypeScript patterns
            '.ts': [
                r'(interface\s+\w+\s*{[^}]*})',  # Interfaces
                r'(type\s+\w+\s*=\s*[^;]+;)',  # Type definitions
                r'(enum\s+\w+\s*{[^}]*})',  # Enums
                r'(function\s+\w+\s*<[^>]*>\s*\([^)]*\)\s*{[^}]*})'  # Generic functions
            ],
            # Java patterns
            '.java': [
                r'(public\s+class\s+\w+\s*(?:extends\s+\w+)?\s*(?:implements\s+[^{]+)?\s*\{[^}]*\})',  # Classes
                r'(public\s+(?:static\s+)?(?:final\s+)?(?:\w+\s+)+\w+\s*\([^)]*\)\s*{[^}]*})',  # Methods
                r'(private|protected|public)\s+(?:static\s+)?(?:final\s+)?(?:\w+\s+)+\w+\s*=\s*[^;]+;'  # Field declarations
            ]
        }
        
        # Default patterns for unknown file types
        default_patterns = [
            r'(\b(?:function|def|class)\s+\w+[^{]*{[^}]*})',  # Functions and classes
            r'([^=\s]+\s*=\s*[^;]+;)',  # Assignments
            r'(<[^>]+>[\s\S]*?</[^>]+>)',  # XML-like tags
            r'([^{}]*\{[^}]*\})'  # Braced blocks
        ]
        
        # Get patterns for file type or use defaults
        file_patterns = patterns.get(ext, default_patterns)
        
        blocks = []
        remaining_content = content
        
        # Extract blocks using patterns
        for pattern in file_patterns:
            matches = re.finditer(pattern, remaining_content, re.MULTILINE | re.DOTALL)
            for match in matches:
                block = match.group(1).strip()
                if block and not any(block in existing for existing in blocks):
                    blocks.append(block)
                    # Remove matched content to avoid overlap
                    remaining_content = remaining_content.replace(match.group(1), '')
        
        # Add any remaining significant content
        remaining_lines = [line.strip() for line in remaining_content.split('\n') 
                         if line.strip() and not line.strip().startswith(('#', '//', '/*', '*', '<!--'))]
        if remaining_lines:
            blocks.append('\n'.join(remaining_lines))
        
        logging.debug(f"Extracted {len(blocks)} code blocks from {file_path} ({ext} file)")
        return blocks
    except Exception as e:
        logging.error(f"Failed to read file {file_path}: {str(e)}")
        return []

def generate_steps(prompt: str, code_blocks: List[str] = []) -> List[str]:
    """Generates optimized steps from prompt and code blocks."""
    # Optimize prompt separately
    optimized_prompt = optimize_text(prompt, is_code=False)
    prompt_tokens = tokenize(optimized_prompt)
    
    # Optimize code blocks if provided
    optimized_blocks = [optimize_text(block, is_code=True) for block in code_blocks] if code_blocks else []
    
    # Combine into steps
    steps = []
    current_step = []
    current_tokens = 0
    
    # Add prompt as first step(s)
    if prompt_tokens > MAX_TOKENS_PER_STEP:
        # Simple sentence splitting without punkt_tab
        prompt_sentences = [s.strip() for s in optimized_prompt.split('.') if s.strip()]
        for sentence in prompt_sentences:
            sentence_tokens = tokenize(sentence)
            if current_tokens + sentence_tokens > MAX_TOKENS_PER_STEP:
                if current_step:
                    steps.append(" ".join(current_step))
                    current_step = []
                    current_tokens = 0
                if sentence_tokens > MAX_TOKENS_PER_STEP:
                    # Simple word splitting
                    words = sentence.split()
                    sub_step = []
                    sub_tokens = 0
                    for word in words:
                        word_tokens = tokenize(word + " ")
                        if sub_tokens + word_tokens > MAX_TOKENS_PER_STEP:
                            steps.append(" ".join(sub_step))
                            sub_step = [word]
                            sub_tokens = word_tokens
                        else:
                            sub_step.append(word)
                            sub_tokens += word_tokens
                    if sub_step:
                        steps.append(" ".join(sub_step))
                else:
                    current_step.append(sentence)
                    current_tokens = sentence_tokens
            else:
                current_step.append(sentence)
                current_tokens += sentence_tokens
    else:
        steps.append(optimized_prompt)
    
    if current_step:
        steps.append(" ".join(current_step))
    
    # Add code blocks as separate steps
    for block in optimized_blocks:
        block_tokens = tokenize(block)
        if block_tokens > MAX_TOKENS_PER_STEP:
            # Split large code blocks
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
    
    # Ensure total token count stays under MAX_TOKEN_LIMIT
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
    
    return steps if steps else [""]

class TokenizerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Code Prompt Optimizer")
        master.geometry("800x600")
        
        try:
            self.encoder = initialize_tiktoken()
        except Exception as e:
            logging.error(f"Failed to initialize tokenizer: {str(e)}")
            messagebox.showerror("Error", f"Failed to initialize tokenizer: {str(e)}")
            master.destroy()
            return

        # Prompt input
        tk.Label(master, text="Enter Your Prompt:").pack(pady=5)
        self.prompt_text = tk.Text(master, height=5, width=80)
        self.prompt_text.pack(pady=5)

        # File selection
        tk.Label(master, text="Select Code File (optional):").pack(pady=5)
        file_frame = tk.Frame(master)
        file_frame.pack(pady=5)
        self.file_path_var = tk.StringVar()
        tk.Entry(file_frame, textvariable=self.file_path_var, width=60).pack(side=tk.LEFT)
        tk.Button(file_frame, text="Browse", command=self.browse_file).pack(side=tk.LEFT, padx=5)

        # Process button
        tk.Button(master, text="Optimize Steps", command=self.optimize).pack(pady=10)

        # Output area
        self.output_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=25)
        self.output_text.pack(pady=10, padx=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Code files", "*.py;*.js;*.cpp;*.java;*.txt"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.file_path_var.set(file_path)

    def optimize(self):
        logging.debug("Optimize button clicked")
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        file_path = self.file_path_var.get()
        
        if not prompt:
            logging.debug("No prompt entered")
            messagebox.showerror("Error", "Please enter a prompt.")
            return
        
        logging.debug(f"Processing prompt: {prompt}")
        code_blocks = []
        if file_path and os.path.exists(file_path):
            logging.debug(f"Processing file: {file_path}")
            code_blocks = extract_code_blocks(file_path)
        
        self.output_text.delete("1.0", tk.END)
        try:
            steps = generate_steps(prompt, code_blocks)
            output = "Optimized Steps:\n\n"
            for i, step in enumerate(steps, 1):
                tokens = tokenize(step)
                output += f"Step {i} (Tokens: {tokens}):\n{step}\n\n"
            self.output_text.insert(tk.END, output)
            logging.debug("Steps generated successfully")
        except Exception as e:
            logging.error(f"Error generating steps: {str(e)}")
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")

def main():
    root = tk.Tk()
    app = TokenizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()