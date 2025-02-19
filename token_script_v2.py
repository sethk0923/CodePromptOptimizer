import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import tiktoken
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
import re
import os
from typing import List
import logging  # Add logging import

# Set up logging
logging.basicConfig(filename='optimizer.log', level=logging.DEBUG,
                   format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize NLTK data
def initialize_nltk():
    """Initialize NLTK resources with proper error handling."""
    required_resources = ['punkt', 'stopwords']
    missing_resources = []
    
    for resource in required_resources:
        try:
            nltk.data.find(f'tokenizers/{resource}')
            logging.info(f"Found NLTK resource: {resource}")
        except LookupError:
            missing_resources.append(resource)
    
    if missing_resources:
        logging.info(f"Downloading missing NLTK resources: {missing_resources}")
        for resource in missing_resources:
            try:
                nltk.download(resource, quiet=True)
                logging.info(f"Successfully downloaded {resource}")
            except Exception as e:
                logging.error(f"Failed to download {resource}: {str(e)}")
                messagebox.showerror("Error", 
                    f"Failed to download required NLTK data ({resource}). "
                    "Please check your internet connection and try again.")
                return False
    return True

# Initialize NLTK before proceeding
if not initialize_nltk():
    logging.error("Failed to initialize NLTK resources")
    raise SystemExit("Failed to initialize required NLTK resources")

DEFAULT_MODEL = "gpt-3.5-turbo"  # For token counting
MAX_TOKEN_LIMIT = 130_000
MAX_TOKENS_PER_STEP = 500  # Smaller steps for code-related prompts

def get_encoding(model: str = DEFAULT_MODEL) -> tiktoken.Encoding:
    """Returns tiktoken encoding for token counting."""
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        try:
            # Fallback to cl100k_base encoding if model-specific encoding fails
            return tiktoken.get_encoding("cl100k_base")
        except Exception as e:
            logging.error(f"Failed to get tiktoken encoding: {str(e)}")
            messagebox.showerror("Error", 
                "Failed to initialize token counter. Please ensure you have the latest version of tiktoken installed:\n"
                "pip install --upgrade tiktoken")
            raise

def tokenize(text: str, model: str = DEFAULT_MODEL) -> int:
    """Tokenizes text using the specified model."""
    encoding = get_encoding(model)
    return len(encoding.encode(text, allowed_special={"<|*|>"}))

def extract_code_blocks(file_path: str) -> List[str]:
    """Extracts meaningful blocks from code files (e.g., functions, classes)."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()

        # Patterns for common code structures (adjust for specific languages if needed)
        patterns = [
            r'(def\s+\w+\s*\(.*?\):(?:\s*?\n(?:\s+.*?\n)+?)+)',  # Python functions
            r'(class\s+\w+(?:\s*\(.*?\))?:.*?(?:\n\s+.*)+?\n)',   # Python classes
            r'(function\s+\w+\s*\(.*?\)\s*{.*?(?:}.*?\n)+?)',     # JavaScript functions
            r'({.*?(?:}.*?\n)+?)',                                # Generic braced blocks
            r'(.+?\n)'                                            # Fallback: line-by-line
        ]
        
        blocks = []
        remaining_content = content
        for pattern in patterns:
            matches = re.findall(pattern, remaining_content, re.DOTALL | re.MULTILINE)
            if matches:
                blocks.extend(match.strip() for match in matches if match.strip())
                # Remove matched content to avoid overlap
                for match in matches:
                    remaining_content = remaining_content.replace(match, '')
            if not remaining_content.strip():
                break
        
        # If no blocks found, split by lines as fallback
        if not blocks and remaining_content.strip():
            blocks = [line.strip() for line in remaining_content.split('\n') if line.strip()]
        
        return blocks
    except Exception as e:
        print(f"Warning: Failed to read file {file_path}: {e}")
        return []

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
        
        try:
            sentences = sent_tokenize(text)
        except LookupError as e:
            logging.error(f"NLTK sentence tokenization failed: {str(e)}")
            # Fallback to simple sentence splitting
            sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        if not sentences:
            return text
        
        try:
            stop_words = set(stopwords.words('english'))
        except LookupError as e:
            logging.error(f"NLTK stopwords lookup failed: {str(e)}")
            # Fallback to basic optimization without stopwords
            return text
        
        optimized_sentences = []
        for sentence in sentences:
            try:
                words = word_tokenize(sentence)
            except LookupError as e:
                logging.error(f"NLTK word tokenization failed: {str(e)}")
                # Fallback to simple word splitting
                words = sentence.split()
            
            filtered_words = [w for w in words if w.lower() not in stop_words and w.isalnum()]
            if filtered_words:
                optimized_sentences.append(" ".join(filtered_words))
        
        return " ".join(optimized_sentences)
    except Exception as e:
        logging.error(f"Text optimization failed: {str(e)}")
        # Return original text if optimization fails
        return text

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
        prompt_sentences = sent_tokenize(optimized_prompt)
        for sentence in prompt_sentences:
            sentence_tokens = tokenize(sentence)
            if current_tokens + sentence_tokens > MAX_TOKENS_PER_STEP:
                if current_step:
                    steps.append(" ".join(current_step))
                    current_step = []
                    current_tokens = 0
                if sentence_tokens > MAX_TOKENS_PER_STEP:
                    words = word_tokenize(sentence)
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

class CodePromptOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Prompt Optimizer")
        self.root.geometry("600x500")

        # Prompt input
        tk.Label(root, text="Enter Your Prompt (e.g., 'Review this code'):").pack(pady=5)
        self.prompt_text = tk.Text(root, height=5, width=50)
        self.prompt_text.pack(pady=5)

        # File selection (optional code context)
        tk.Label(root, text="Select Code File (optional):").pack(pady=5)
        self.file_path_var = tk.StringVar()
        file_frame = tk.Frame(root)
        file_frame.pack(pady=5)
        tk.Entry(file_frame, textvariable=self.file_path_var, width=50).pack(side=tk.LEFT)
        tk.Button(file_frame, text="Browse", command=self.browse_file).pack(side=tk.LEFT, padx=5)

        # Process button
        tk.Button(root, text="Optimize Steps", command=self.optimize).pack(pady=10)

        # Output area
        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20)
        self.output_text.pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Code files", "*.py *.js *.cpp *.java *.txt"), ("All files", "*.*")])
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
        if file_path and os.path.exists(file_path):
            logging.debug(f"File path: {file_path}")
            code_blocks = extract_code_blocks(file_path)
        else:
            code_blocks = []
        
        self.output_text.delete(1.0, tk.END)
        try:
            steps = generate_steps(prompt, code_blocks)
        except Exception as e:
            logging.error(f"Error generating steps: {str(e)}")
            self.output_text.insert(tk.END, f"Error: Something went wrong - {str(e)}\n")
            return
        
        if not steps or steps == [""]:
            logging.debug("No steps generated")
            self.output_text.insert(tk.END, "No optimized steps generated.\n")
            return
        
        output = "Optimized Steps for Manual AI Entry (Code Review):\n\n"
        for step_idx, step in enumerate(steps, 1):
            tokens = tokenize(step)
            output += f"Step {step_idx} (Tokens: {tokens}):\n{step}\n\n"
        
        logging.debug("Steps generated successfully")
        self.output_text.insert(tk.END, output)

def main():
    root = tk.Tk()
    app = CodePromptOptimizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()