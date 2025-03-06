import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import os
import re
import sys  # Added missing sys import
from typing import List, Tuple, Optional, Dict
import pathlib
from pathlib import Path
import threading
import subprocess
import tempfile
import json
import shutil
import time
import platform
from ctypes import windll, byref, c_int, sizeof
from PIL import Image, ImageTk  # Added PIL import for better icon handling
import heapq  # For prioritizing code blocks

# Import new libraries as per the upgrade plan
try:
    import tiktoken
    import nltk
    from nltk.corpus import words
    import ast
    from bs4 import BeautifulSoup
    import esprima
    import pycparser
    from tree_sitter import Language, Parser
    import cssparser
    import javalang
    import black
    import pyflakes
    import chardet
    import construct
    try:
        import pefile
        import elftools
        from capstone import *
        import r2pipe
    except ImportError:
        pass  # Binary analysis libraries are optional
except ImportError as e:
    print(f"Warning: Some libraries could not be imported: {e}")
    print("Run 'pip install -r requirements.txt' to install all dependencies")

# Constants
MAX_TOKEN_LIMIT = 2500
MAX_TOKENS_PER_STEP = 500

# Dark theme colors
DARK_THEME_BG = "#2d2d2d"
DARK_THEME_FG = "white"
DARK_THEME_BUTTON = "#4a4a4a"
DARK_THEME_HIGHLIGHT = "#3c3c3c"
DARK_THEME_ACCENT = "#0078d7"
DARK_THEME_MENUBAR = "#555555"  # Graphite color for menu bar

# Light theme colors
LIGHT_THEME_BG = "#f0f0f0"
LIGHT_THEME_FG = "#333333"
LIGHT_THEME_BUTTON = "#e1e1e1"
LIGHT_THEME_HIGHLIGHT = "#ffffff"
LIGHT_THEME_ACCENT = "#0078d7"
LIGHT_THEME_MENUBAR = "#d4d4d4"  # Light graphite for menu bar

# Default to dark theme
THEME_BG = DARK_THEME_BG
THEME_FG = DARK_THEME_FG
THEME_BUTTON = DARK_THEME_BUTTON
THEME_HIGHLIGHT = DARK_THEME_HIGHLIGHT
THEME_ACCENT = DARK_THEME_ACCENT
THEME_MENUBAR = DARK_THEME_MENUBAR  # Initialize with dark theme menu bar color

GHIDRA_HEADLESS_PATH = ""  # Will be set if Ghidra is found

# Ensure NLTK data is available
try:
    nltk.data.find('corpora/words')
except LookupError:
    try:
        nltk.download('words', quiet=True)
    except:
        print("Warning: NLTK words corpus could not be downloaded")

# Initialize Tree-sitter if available
PARSERS = {}
try:
    # This path would need to be adjusted based on where the compiled language files are stored
    LANGUAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tree-sitter-grammars")
    if os.path.exists(LANGUAGE_DIR):
        for lang_file in os.listdir(LANGUAGE_DIR):
            if lang_file.endswith('.so'):
                lang_name = os.path.splitext(lang_file)[0].replace('tree-sitter-', '')
                try:
                    PARSERS[lang_name] = {
                        'language': Language(os.path.join(LANGUAGE_DIR, lang_file), lang_name),
                        'parser': Parser()
                    }
                    PARSERS[lang_name]['parser'].set_language(PARSERS[lang_name]['language'])
                except Exception as e:
                    print(f"Failed to load Tree-sitter language {lang_name}: {e}")
except Exception as e:
    print(f"Tree-sitter initialization error: {e}")

def tokenize(text: str) -> int:
    """Count tokens using tiktoken (OpenAI's tokenizer)."""
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except Exception as e:
        print(f"Tiktoken error: {e}. Falling back to basic tokenization.")
        return len(text.split())

def detect_file_encoding(file_path: str) -> str:
    """Detect the encoding of a file using chardet."""
    try:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        return result['encoding'] or 'utf-8'
    except Exception:
        return 'utf-8'  # Fallback to UTF-8

def optimize_text(text: str, is_code: bool = False, file_type: str = None) -> str:
    """Optimize text or code while reducing tokens."""
    if not text:
        return ""
        
    # First apply basic optimization
    if is_code:
        # Remove comments based on file type
        text = re.sub(r'#.*$', '', text, flags=re.MULTILINE)  # Python comments
        text = re.sub(r'<!--[\s\S]*?-->', '', text)  # HTML comments
        text = re.sub(r'/\*[\s\S]*?\*/', '', text)  # CSS/JS multi-line comments
        text = re.sub(r'//.*$', '', text, flags=re.MULTILINE)  # JS/C/Java single-line comments
        
        # Apply more advanced formatting if available
        if file_type == '.py':
            try:
                text = black.format_str(text, mode=black.Mode())
            except:
                pass  # Fall back to basic formatting
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        return text
    
    # For natural language text
    text = re.sub(r'\s+', ' ', text.strip())
    return text

def extract_with_tree_sitter(content: str, lang_name: str) -> List[str]:
    """Extract code blocks using Tree-sitter."""
    if lang_name not in PARSERS:
        return []
        
    parser = PARSERS[lang_name]['parser']
    tree = parser.parse(bytes(content, 'utf-8'))
    root = tree.root_node
    
    # Get relevant node types based on language
    node_types = {
        'python': ['function_definition', 'class_definition'],
        'javascript': ['function_declaration', 'class_declaration', 'arrow_function'],
        'java': ['method_declaration', 'class_declaration'],
        'c': ['function_definition', 'struct_declaration'],
        'cpp': ['function_definition', 'class_declaration']
    }
    
    target_types = node_types.get(lang_name, [])
    blocks = []
    
    for child in root.children:
        if child.type in target_types:
            blocks.append(content[child.start_byte:child.end_byte])
    
    return blocks

def extract_code_blocks(file_path: str) -> List[str]:
    """Extract key code blocks from a file based on language."""
    if not os.path.exists(file_path):
        return []
        
    try:
        encoding = detect_file_encoding(file_path)
        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
            content = f.read()
        
        ext = os.path.splitext(file_path)[1].lower()
        
        # Try language-specific parsers first
        if ext == '.py':
            try:
                tree = ast.parse(content)
                blocks = []
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                        start_line = node.lineno
                        end_line = 0
                        for child in ast.walk(node):
                            if hasattr(child, 'lineno'):
                                end_line = max(end_line, child.lineno)
                        
                        if end_line >= start_line:
                            lines = content.split('\n')
                            block_text = '\n'.join(lines[start_line-1:end_line])
                            blocks.append(block_text)
                return blocks if blocks else [content]
            except SyntaxError:
                pass  # Fall back to regex
                
        elif ext == '.html':
            try:
                soup = BeautifulSoup(content, 'html.parser')
                blocks = []
                # Extract scripts
                for script in soup.find_all('script'):
                    blocks.append(str(script))
                # Extract styles
                for style in soup.find_all('style'):
                    blocks.append(str(style))
                # Extract main elements
                for elem in soup.find_all(['div', 'header', 'footer', 'main', 'section']):
                    blocks.append(str(elem))
                return blocks if blocks else [content]
            except:
                pass  # Fall back to regex
                
        elif ext == '.js':
            try:
                # Use esprima to parse JavaScript
                parsed = esprima.parseScript(content)
                blocks = []
                for node in parsed.body:
                    if node.type in ['FunctionDeclaration', 'ClassDeclaration']:
                        blocks.append(content[node.range[0]:node.range[1]])
                return blocks if blocks else [content]
            except:
                pass  # Fall back to regex
                
        # Try Tree-sitter as a backup for supported languages
        lang_map = {'.py': 'python', '.js': 'javascript', '.java': 'java', '.c': 'c', '.cpp': 'cpp'}
        if ext in lang_map and lang_map[ext] in PARSERS:
            blocks = extract_with_tree_sitter(content, lang_map[ext])
            if blocks:
                return blocks
        
        # Fall back to regex for unsupported languages or if parsing failed
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
            '.java': [r'(public|private|protected)?\s+(static)?\s*(\w+)\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}',  # Methods
                     r'(public|private|protected)?\s+(class|interface|enum)\s+\w+\s*(?:extends\s+\w+)?(?:implements\s+\w+(?:,\s*\w+)*)?\s*\{[^}]*\}'],  # Classes
            '.c': [r'(\w+)\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}',  # C functions
                  r'(struct|enum|union)\s+\w+\s*\{[^}]*\}'],  # C structs/enums
            '.cpp': [r'(\w+)\s+(\w+)::(\w+)\s*\([^)]*\)\s*\{[^}]*\}',  # C++ methods
                    r'(class|struct|enum|union)\s+\w+\s*(?::\s*\w+(?:,\s*\w+)*)?\s*\{[^}]*\}'],  # C++ classes
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

# Find Ghidra installation if available
def find_ghidra():
    """Try to find Ghidra installation on the system."""
    global GHIDRA_HEADLESS_PATH
    
    # Common installation locations
    possible_locations = []
    
    if platform.system() == "Windows":
        # Windows locations
        program_files = os.environ.get("ProgramFiles", "C:\\Program Files")
        program_files_x86 = os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
        
        possible_locations.extend([
            os.path.join(program_files, "Ghidra"),
            os.path.join(program_files_x86, "Ghidra"),
            "C:\\Ghidra",
            os.path.join(os.path.expanduser("~"), "Ghidra")
        ])
    else:
        # Linux/macOS locations
        possible_locations.extend([
            "/usr/local/ghidra",
            "/opt/ghidra",
            "/Applications/Ghidra",
            os.path.join(os.path.expanduser("~"), "ghidra")
        ])
    
    # Check if GHIDRA_HOME environment variable is set
    if "GHIDRA_HOME" in os.environ:
        possible_locations.insert(0, os.environ["GHIDRA_HOME"])
    
    # Look for analyzeHeadless script in each location
    for location in possible_locations:
        if not os.path.exists(location):
            continue
        
        # Check for version-specific subdirectories
        for item in os.listdir(location):
            if not os.path.isdir(os.path.join(location, item)):
                continue
                
            # Check if this looks like a Ghidra version directory
            if item.startswith("ghidra_") or os.path.exists(os.path.join(location, item, "support", "analyzeHeadless")):
                headless_path = ""
                
                # Check for the analyzeHeadless script
                if platform.system() == "Windows":
                    headless_path = os.path.join(location, item, "support", "analyzeHeadless.bat")
                else:
                    headless_path = os.path.join(location, item, "support", "analyzeHeadless")
                
                if os.path.exists(headless_path):
                    GHIDRA_HEADLESS_PATH = headless_path
                    print(f"Found Ghidra at: {GHIDRA_HEADLESS_PATH}")
                    return True
    
    return False

# Try to find Ghidra
try:
    find_ghidra()
except Exception as e:
    print(f"Warning: Error while looking for Ghidra: {e}")
    
# Create Ghidra analysis script
GHIDRA_SCRIPT_CONTENT = '''
// Ghidra script to extract function information and decompile code
// @category CodePromptOptimizer

import java.io.File;
import java.io.FileWriter;
import java.util.HashMap;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionManager;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.util.task.TaskMonitor;

public class ExtractFunctionsScript extends GhidraScript {

    @Override
    public void run() throws Exception {
        println("Extracting functions from binary...");
        
        // Output file for results
        String outputPath = getScriptArgs()[0];
        File outputFile = new File(outputPath);
        FileWriter writer = new FileWriter(outputFile);
        
        // Get all functions
        FunctionManager functionManager = currentProgram.getFunctionManager();
        int count = 0;
        
        // Set up decompiler
        DecompInterface decompInterface = new DecompInterface();
        decompInterface.openProgram(currentProgram);
        
        writer.write("{\\"functions\\": [");
        
        // Process each function
        for (Function function : functionManager.getFunctions(true)) {
            if (count > 0) {
                writer.write(",");
            }
            
            String name = function.getName();
            String signature = function.getSignature().toString();
            String entryPoint = function.getEntryPoint().toString();
            
            // Get decompiled code
            DecompileResults results = decompInterface.decompileFunction(
                function, 30, TaskMonitor.DUMMY);
            String decompiled = "";
            
            if (results.decompileCompleted()) {
                decompiled = results.getDecompiledFunction().getC();
                // Escape JSON special characters
                decompiled = decompiled.replace("\\"", "\\\\"")
                                     .replace("\\n", "\\\\n")
                                     .replace("\\r", "\\\\r")
                                     .replace("\\t", "\\\\t");
            }
            
            writer.write(String.format(
                "{\\"name\\": \\"%s\\", \\"signature\\": \\"%s\\", \\"entry\\": \\"%s\\", \\"decompiled\\": \\"%s\\"}",
                name, signature, entryPoint, decompiled
            ));
            
            count++;
            monitor.setProgress(count);
            
            // Limit to 20 functions to avoid excessive output
            if (count >= 20) {
                break;
            }
        }
        
        writer.write("]}");
        writer.close();
        
        println("Extracted " + count + " functions to " + outputPath);
    }
}
'''

def create_ghidra_script():
    """Create a temporary Ghidra script file."""
    try:
        script_dir = os.path.join(tempfile.gettempdir(), "code_prompt_optimizer")
        os.makedirs(script_dir, exist_ok=True)
        
        script_path = os.path.join(script_dir, "ExtractFunctionsScript.java")
        with open(script_path, "w") as f:
            f.write(GHIDRA_SCRIPT_CONTENT)
            
        return script_dir, script_path
    except Exception as e:
        print(f"Error creating Ghidra script: {e}")
        return None, None

def analyze_with_ghidra(file_path):
    """Use Ghidra to analyze a binary file."""
    if not GHIDRA_HEADLESS_PATH:
        return ["Ghidra not found - binary decompilation not available"]
    
    try:
        # Create temporary directories
        temp_dir = tempfile.mkdtemp(prefix="ghidra_analysis_")
        project_dir = os.path.join(temp_dir, "project")
        os.makedirs(project_dir, exist_ok=True)
        
        # Create script
        script_dir, script_path = create_ghidra_script()
        if not script_path:
            return ["Error creating Ghidra script"]
        
        # Output file for results
        output_file = os.path.join(temp_dir, "output.json")
        
        # Prepare command
        file_name = os.path.basename(file_path)
        project_name = "temp_project"
        
        cmd = [
            GHIDRA_HEADLESS_PATH,
            project_dir,
            project_name,
            "-import",
            file_path,
            "-scriptPath",
            script_dir,
            "-postScript",
            "ExtractFunctionsScript.java",
            output_file,
            "-deleteProject"
        ]
        
        # Show status
        print(f"Running Ghidra analysis on {file_path}...")
        print(f"Command: {' '.join(cmd)}")
        
        # Run Ghidra (this can take a while)
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Wait for up to 2 minutes
        try:
            stdout, stderr = process.communicate(timeout=120)
        except subprocess.TimeoutExpired:
            process.kill()
            return ["Ghidra analysis timed out after 2 minutes"]
        
        # Check for results
        if not os.path.exists(output_file):
            return [f"Ghidra analysis failed: {stderr}"]
        
        # Parse results
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        # Clean up
        try:
            shutil.rmtree(temp_dir)
            shutil.rmtree(script_dir)
        except:
            pass
        
        # Format results for display
        results = [f"Ghidra Decompilation of {file_name}:"]
        for function in data.get('functions', []):
            results.append(f"\nFunction: {function.get('name')} {function.get('signature')}")
            decompiled = function.get('decompiled', '')
            if decompiled:
                # Format the decompiled code for display
                decompiled = decompiled.replace("\\n", "\n").replace("\\t", "    ")
                results.append(decompiled)
            else:
                results.append("(Decompilation failed)")
                
        return results
        
    except Exception as e:
        print(f"Error in Ghidra analysis: {e}")
        return [f"Ghidra analysis error: {str(e)}"]

def analyze_binary_file(file_path: str) -> List[str]:
    """Extract meaningful information from binary files."""
    try:
        ext = os.path.splitext(file_path)[1].lower()
        
        # Try Ghidra analysis first if available
        if GHIDRA_HEADLESS_PATH:
            try:
                # Show a message in the console that Ghidra is being used
                print(f"Using Ghidra for decompilation of {file_path}")
                results = analyze_with_ghidra(file_path)
                if results and not results[0].startswith("Ghidra analysis error"):
                    return results
                print(f"Ghidra analysis failed, falling back to basic analysis: {results[0]}")
            except Exception as e:
                print(f"Ghidra processing error: {e}, falling back to basic analysis")
        
        # Fallback to basic analysis
        if ext == '.exe':
            try:
                pe = pefile.PE(file_path)
                sections = []
                sections.append(f"PE File: {os.path.basename(file_path)}")
                sections.append(f"Machine: {pe.FILE_HEADER.Machine}")
                sections.append(f"Number of sections: {pe.FILE_HEADER.NumberOfSections}")
                sections.append("Imports:")
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    sections.append(f"  {entry.dll.decode()}")
                    for imp in entry.imports[:10]:  # Limit to 10 imports per DLL
                        if imp.name:
                            sections.append(f"    {imp.name.decode()}")
                return sections
            except:
                return ["Binary file (PE/EXE) - cannot extract meaningful text"]
        else:
            # Generic binary file analysis
            return ["Binary file - cannot extract meaningful text"]
    except Exception as e:
        print(f"Error analyzing binary file {file_path}: {str(e)}")
        return ["Error analyzing binary file"]

def extract_keywords(prompt: str) -> List[str]:
    """Extract meaningful keywords from the prompt.
    
    Args:
        prompt: User's input prompt
        
    Returns:
        List of significant keywords
    """
    # Remove common words and punctuation
    common_words = {
        'a', 'an', 'the', 'and', 'or', 'but', 'if', 'then', 'else', 'when',
        'at', 'from', 'by', 'for', 'with', 'about', 'to', 'in', 'on', 'is',
        'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'can', 'could', 'will', 'would', 'should', 'shall',
        'may', 'might', 'must', 'of', 'that', 'this', 'these', 'those', 'it',
        'its', 'it\'s', 'their', 'there', 'here', 'where', 'how', 'what', 'why',
        'who', 'whom', 'whose', 'which', 'while', 'i', 'me', 'my', 'mine', 'you',
        'your', 'yours', 'they', 'them', 'as', 'so', 'just', 'very', 'really',
        'code', 'function', 'class', 'method', 'variable', 'object', 'file',
        'program', 'script', 'data', 'value', 'type', 'return', 'input', 'output',
    }
    
    # Clean the prompt and split into words
    clean_prompt = re.sub(r'[^\w\s]', ' ', prompt.lower())
    words = clean_prompt.split()
    
    # Filter out common words and short words
    keywords = [word for word in words if word not in common_words and len(word) > 2]
    
    # Get unique keywords
    unique_keywords = list(set(keywords))
    
    # Add any capitalized words from the original prompt as they might be important names
    capitalized = re.findall(r'\b[A-Z][a-zA-Z0-9_]*\b', prompt)
    for word in capitalized:
        if word.lower() not in common_words and word not in unique_keywords:
            unique_keywords.append(word)
    
    return unique_keywords

def filter_relevant_blocks(blocks: List[str], keywords: List[str]) -> List[Tuple[str, float]]:
    """Filter and rank code blocks by relevance to keywords.
    
    Args:
        blocks: List of code blocks extracted from the file
        keywords: List of keywords from the user's prompt
        
    Returns:
        List of tuples containing (block, relevance_score)
    """
    if not keywords:
        return [(block, 0.0) for block in blocks]  # No filtering if no keywords
    
    scored_blocks = []
    
    for block in blocks:
        # Calculate relevance score based on keyword presence
        score = 0.0
        block_lower = block.lower()
        
        for keyword in keywords:
            # Check exact matches (case insensitive)
            matches = re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', block_lower)
            score += len(matches) * 2  # Exact matches are weighted higher
            
            # Check partial matches (for variable/function names)
            if keyword.lower() in block_lower:
                score += 1
                
            # Give higher score for keywords in function/class definitions or comments
            if re.search(r'(def|class|function)\s+\w*' + re.escape(keyword.lower()) + r'\w*', block_lower):
                score += 5
                
            if re.search(r'[#//]\s.*' + re.escape(keyword.lower()), block_lower):
                score += 3  # Keywords in comments
        
        # Normalize score by block length to not overly favor long blocks
        normalized_score = score / (len(block.split()) + 1)
        
        # Only include blocks with some relevance
        if normalized_score > 0:
            scored_blocks.append((block, normalized_score))
    
    # Sort blocks by relevance score (descending)
    scored_blocks.sort(key=lambda x: x[1], reverse=True)
    
    # If no blocks matched, return all blocks with zero score
    if not scored_blocks and blocks:
        return [(block, 0.0) for block in blocks]
        
    return scored_blocks

def generate_steps(prompt: str, code_blocks: List[str] = [], relevance_info: List[float] = None) -> List[str]:
    """Generate optimized steps from prompt and code blocks.
    
    Args:
        prompt: The user's input prompt
        code_blocks: List of extracted code blocks
        relevance_info: Optional list of relevance scores for each block
        
    Returns:
        List of formatted steps to display to the user
    """
    optimized_prompt = optimize_text(prompt, is_code=False)
    prompt_tokens = tokenize(optimized_prompt)
    
    steps = []
    current_step = []
    current_tokens = 0
    
    # Add an initial step with the extracted keywords if available
    keywords = extract_keywords(prompt)
    if keywords:
        keyword_step = "Extracted Keywords: " + ", ".join(keywords)
        steps.append(keyword_step)
    
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
    
    if current_step and len(current_step) > 0 and " ".join(current_step) not in steps:
        steps.append(" ".join(current_step))
    
    # Handle code blocks with relevance information
    for i, block in enumerate(code_blocks):
        file_type = '.py' if "def " in block or "class " in block else \
                   '.js' if "function " in block or "var " in block else \
                   '.html' if "<" in block and ">" in block else \
                   '.css' if "{" in block and ":" in block else '.txt'
                   
        optimized_block = optimize_text(block, is_code=True, file_type=file_type)
        block_tokens = tokenize(optimized_block)
        
        # Add relevance score comment if available
        if relevance_info and i < len(relevance_info) and relevance_info[i] > 0:
            relevance_header = f"\n# Relevance Score: {relevance_info[i]:.2f} - This code matches your keywords\n"
            optimized_block = relevance_header + optimized_block
        
        if block_tokens > MAX_TOKENS_PER_STEP:
            lines = optimized_block.split('\n')
            sub_block = []
            sub_tokens = 0
            for line in lines:
                line_tokens = tokenize(line)
                if sub_tokens + line_tokens > MAX_TOKENS_PER_STEP:
                    if sub_block:
                        steps.append("\n".join(sub_block))
                        sub_block = [line]
                        sub_tokens = line_tokens
                else:
                    sub_block.append(line)
                    sub_tokens += line_tokens
            if sub_block:
                steps.append("\n".join(sub_block))
        else:
            steps.append(optimized_block)
    
    # Enforce total token limit
    total_tokens = sum(tokenize(step) for step in steps)
    if total_tokens > MAX_TOKEN_LIMIT:
        # Trim steps to fit within limit
        trimmed_steps = []
        current_total = 0
        for step in steps:
            step_tokens = tokenize(step)
            if current_total + step_tokens <= MAX_TOKEN_LIMIT:
                trimmed_steps.append(step)
                current_total += step_tokens
            else:
                # Add a final note about truncation
                trimmed_steps.append("... [Additional content truncated due to token limit]")
                break
        steps = trimmed_steps
    
    return steps if steps else ["No content to process"]

class TokenizerGUI:
    def __init__(self, master):
        self.master = master
        self.is_dark_mode = True  # Start with dark mode by default
        master.title("Code Prompt Optimizer")
        master.geometry("800x600")
        master.configure(bg=THEME_BG)
        
        # Set window bar color if on Windows
        if platform.system() == "Windows":
            try:
                windll.dwmapi.DwmSetWindowAttribute(
                    windll.user32.GetParent(master.winfo_id()), 
                    20,  # DWMWA_CAPTION_COLOR
                    byref(c_int(int(THEME_MENUBAR.lstrip('#'), 16))), 
                    sizeof(c_int)
                )
            except Exception as e:
                print(f"Could not set window bar color: {e}")
        
        # Configure ttk styles for modern look
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use a theme that supports custom styling
        self.style.configure("TButton", padding=6, relief="flat", background=THEME_BUTTON, foreground=THEME_FG)
        self.style.configure("TLabel", padding=6, background=THEME_BG, foreground=THEME_FG)
        self.style.configure("TEntry", fieldbackground=THEME_HIGHLIGHT, foreground=THEME_FG)
        self.style.configure("TFrame", background=THEME_BG)
        
        # Main container
        main_frame = ttk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Top section with buttons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, side=tk.TOP, pady=(0, 10))
        
        # Add theme toggle button
        self.theme_button = ttk.Button(
            buttons_frame, 
            text="🌙 Dark Mode" if not self.is_dark_mode else "☀️ Light Mode", 
            command=self.toggle_theme
        )
        self.theme_button.pack(side=tk.RIGHT, padx=5)
        
        # Add export to text file button
        self.export_button = ttk.Button(
            buttons_frame,
            text="💾 Export to TXT",
            command=self.export_to_txt
        )
        self.export_button.pack(side=tk.RIGHT, padx=5)
        
        # Prompt input section
        ttk.Label(main_frame, text="Enter Your Prompt:").pack(anchor="w", pady=(0, 5))
        
        self.prompt_frame = ttk.Frame(main_frame)
        self.prompt_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.prompt_text = tk.Text(self.prompt_frame, height=6, bg=THEME_HIGHLIGHT, fg=THEME_FG, 
                                  insertbackground=THEME_FG, relief="flat", padx=10, pady=10)
        self.prompt_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.prompt_text.bind("<Tab>", self.autocomplete)
        
        prompt_scrollbar = ttk.Scrollbar(self.prompt_frame, command=self.prompt_text.yview)
        prompt_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.prompt_text.config(yscrollcommand=prompt_scrollbar.set)
        
        # File selection section
        ttk.Label(main_frame, text="Select Code File (optional):").pack(anchor="w", pady=(10, 5))
        
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=5)
        
        self.file_path_var = tk.StringVar()
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, style="TEntry")
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        browse_button = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_button.pack(side=tk.RIGHT)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.optimize_button = ttk.Button(button_frame, text="Optimize Steps", command=self.optimize)
        self.optimize_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.copy_button = ttk.Button(button_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack(side=tk.LEFT)
        
        # Token counter
        self.token_label = ttk.Label(button_frame, text="Tokens: 0")
        self.token_label.pack(side=tk.RIGHT)
        
        # Status bar
        self.status_bar = ttk.Label(main_frame, text="Ready", anchor="w")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))
        
        # Output section
        ttk.Label(main_frame, text="Optimized Steps:").pack(anchor="w", pady=(10, 5))
        
        self.output_frame = ttk.Frame(main_frame)
        self.output_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.output_text = tk.Text(self.output_frame, height=15, bg=THEME_HIGHLIGHT, fg=THEME_FG, 
                                  insertbackground=THEME_FG, relief="flat", padx=10, pady=10)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        output_scrollbar = ttk.Scrollbar(self.output_frame, command=self.output_text.yview)
        output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=output_scrollbar.set)
        
        # Initial focus and bindings
        self.prompt_text.focus_set()
        self.prompt_text.bind("<KeyRelease>", self.update_token_count)
        
        # Word list for autocomplete
        self.word_list = set()
        try:
            self.word_list = set(words.words())
        except:
            print("Warning: NLTK words corpus not available")
            
        # Add programming keywords to autocomplete
        programming_keywords = {
            "function", "class", "import", "from", "def", "return", "if", "else", "elif",
            "while", "for", "try", "except", "finally", "with", "as", "async", "await",
            "break", "continue", "pass", "raise", "True", "False", "None", "lambda",
            "global", "nonlocal", "yield", "assert", "del", "in", "is", "not", "and", "or"
        }
        self.word_list.update(programming_keywords)
        
        # Suggestions for autocomplete
        self.current_suggestions = []
        self.suggestion_index = 0

    def update_token_count(self, event=None):
        """Update the token count in real-time."""
        try:
            text = self.prompt_text.get("1.0", tk.END)
            count = tokenize(text)
            self.token_label.config(text=f"Tokens: {count}")
        except Exception as e:
            print(f"Error counting tokens: {e}")

    def autocomplete(self, event):
        """Handle autocomplete with Tab key."""
        # Get current word
        current_line = self.prompt_text.get("insert linestart", "insert")
        if not current_line.strip():
            return "break"  # Just insert a tab if line is empty
            
        words_in_line = current_line.split()
        if not words_in_line:
            return "break"
            
        current_word = words_in_line[-1].lower()
        if len(current_word) < 2:
            return "break"  # Don't autocomplete very short words
            
        # If we already have suggestions and Tab was pressed again
        if self.current_suggestions and hasattr(self, 'last_word') and self.last_word == current_word:
            self.suggestion_index = (self.suggestion_index + 1) % len(self.current_suggestions)
            suggestion = self.current_suggestions[self.suggestion_index]
            
            # Replace the current word with the next suggestion
            self.prompt_text.delete("insert-" + str(len(current_word)) + "c", "insert")
            self.prompt_text.insert("insert", suggestion)
        else:
            # Find new suggestions
            self.current_suggestions = [word for word in self.word_list 
                                     if word.lower().startswith(current_word.lower())][:5]
            
            if self.current_suggestions:
                self.suggestion_index = 0
                suggestion = self.current_suggestions[0]
                
                # Replace the current word with the suggestion
                self.prompt_text.delete("insert-" + str(len(current_word)) + "c", "insert")
                self.prompt_text.insert("insert", suggestion)
                
                # Show a tooltip with all suggestions
                if len(self.current_suggestions) > 1:
                    self.show_suggestions_tooltip()
                    
            self.last_word = current_word
            
        return "break"  # Prevent the default Tab behavior

    def show_suggestions_tooltip(self):
        """Show a tooltip with autocomplete suggestions."""
        # This would be a simple implementation - for a real app, you'd want a custom tooltip widget
        if hasattr(self, 'tooltip') and self.tooltip:
            self.tooltip.destroy()
            
        x, y, _, h = self.prompt_text.bbox("insert")
        x, y = self.prompt_text.winfo_rootx() + x, self.prompt_text.winfo_rooty() + y + h
        
        self.tooltip = tk.Toplevel(self.master)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        suggestions_text = "\n".join(self.current_suggestions[1:])
        label = ttk.Label(self.tooltip, text=suggestions_text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()
        
        # Auto-hide tooltip after 3 seconds
        self.master.after(3000, lambda: self.tooltip.destroy() if hasattr(self, 'tooltip') else None)

    def browse_file(self):
        """Open file dialog to select a code file."""
        file_types = [
            ("All supported files", "*.py;*.js;*.html;*.css;*.txt;*.java;*.c;*.cpp;*.h;*.exe;*.dll;*.so;*.dylib;*.elf"),
            ("Python files", "*.py"),
            ("JavaScript files", "*.js"),
            ("HTML files", "*.html;*.htm"),
            ("CSS files", "*.css"),
            ("Java files", "*.java"),
            ("C/C++ files", "*.c;*.cpp;*.h;*.hpp"),
            ("Binary files", "*.exe;*.dll;*.so;*.dylib;*.elf;*.bin"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if file_path:
            self.file_path_var.set(file_path)
            # Update status bar
            file_name = os.path.basename(file_path)
            self.status_bar.config(text=f"File selected: {file_name}")

    def optimize(self):
        """Process the prompt and code file to generate optimized steps."""
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        file_path = self.file_path_var.get()
        
        if not prompt:
            messagebox.showerror("Error", "Please enter a prompt.")
            return
            
        # Disable UI during processing
        self.optimize_button.config(state="disabled")
        self.status_bar.config(text="Processing...")
        self.master.update()
        
        # Use threading to keep the UI responsive
        threading.Thread(target=self._optimize_thread, args=(prompt, file_path), daemon=True).start()
    
    def _optimize_thread(self, prompt, file_path):
        """Thread function for optimization to prevent UI freezing."""
        try:
            blocks = []
            parser_used = "Basic"
            
            # Extract keywords and filter blocks by relevance
            self.master.after(0, lambda: self.status_bar.config(text="Analyzing prompt keywords..."))
            keywords = extract_keywords(prompt)
            
            # Display what keywords were found
            keyword_info = f"Keywords found: {', '.join(keywords)}" if keywords else "No specific keywords found"
            self.master.after(0, lambda: self.status_bar.config(text=keyword_info))
            
            if file_path and os.path.exists(file_path):
                # Check if it's a binary file
                is_binary = False
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        f.read(1024)  # Try to read a bit of the file
                except UnicodeDecodeError:
                    is_binary = True
                
                if is_binary:
                    self.master.after(0, lambda: self.status_bar.config(text="Analyzing binary file... This may take a while."))
                    
                    # Update the status bar to show we're using Ghidra if available
                    if GHIDRA_HEADLESS_PATH:
                        self.master.after(0, lambda: self.status_bar.config(text="Running Ghidra decompilation... (this may take 1-2 minutes)"))
                    
                    blocks = analyze_binary_file(file_path)
                    parser_used = "Ghidra Decompiler" if GHIDRA_HEADLESS_PATH and blocks and "Ghidra Decompilation" in blocks[0] else "Binary Analysis"
                else:
                    # It's a text file, process normally
                    self.master.after(0, lambda: self.status_bar.config(text="Extracting code blocks..."))
                    blocks = extract_code_blocks(file_path)
                    
                    # Update parser_used based on file extension and what was used
                    ext = os.path.splitext(file_path)[1].lower()
                    parser_map = {
                        '.py': "AST" if "ast" in sys.modules else "Regex",
                        '.js': "Esprima" if "esprima" in sys.modules else "Regex",
                        '.html': "BeautifulSoup" if "bs4" in sys.modules else "Regex",
                        '.java': "Javalang" if "javalang" in sys.modules else "Regex",
                        '.c': "PyCParser" if "pycparser" in sys.modules else "Regex",
                        '.css': "CSSParser" if "cssparser" in sys.modules else "Regex"
                    }
                    
                    # Try to update parser used
                    parser_used = parser_map.get(ext, "Tree-sitter" if "tree_sitter" in sys.modules else "Regex")
                
                # Filter and score blocks based on keywords
                scored_blocks = filter_relevant_blocks(blocks, keywords)
                
                # If we have relevant blocks, show how many were selected
                if scored_blocks and any(score > 0 for _, score in scored_blocks):
                    relevant_count = sum(1 for _, score in scored_blocks if score > 0)
                    total_count = len(blocks)
                    self.master.after(0, lambda: self.status_bar.config(
                        text=f"Found {relevant_count} relevant code blocks out of {total_count} total blocks"))
                    
                    # Sort blocks by relevance and keep original blocks for reference
                    relevance_scores = [score for _, score in scored_blocks]
                    filtered_blocks = [block for block, _ in scored_blocks]
                else:
                    self.master.after(0, lambda: self.status_bar.config(
                        text=f"No keyword matches found. Processing all {len(blocks)} blocks."))
                    filtered_blocks = blocks
                    relevance_scores = [0.0] * len(blocks)
                
                # Generate final steps with relevance information
                self.master.after(0, lambda: self.status_bar.config(text="Generating optimized steps..."))
                steps = generate_steps(prompt, filtered_blocks, relevance_scores)
            else:
                # No file, just process the prompt
                steps = generate_steps(prompt)
            
            # Update UI in the main thread
            self.master.after(0, lambda: self._update_ui_after_optimize(steps, parser_used))
        
        except Exception as e:
            import traceback
            self.master.after(0, lambda: self._show_error(f"Error during optimization: {str(e)}\n{traceback.format_exc()}"))
        finally:
            self.master.after(0, lambda: self.optimize_button.config(state="normal"))

    def _update_ui_after_optimize(self, steps, parser_used):
        """Update the UI with optimization results."""
        self.output_text.delete("1.0", tk.END)
        
        # Add a header with info about the processor used
        header = f"=== OPTIMIZED OUTPUT (Processed with {parser_used}) ===\n\n"
        self.output_text.insert(tk.END, header)
        
        for i, step in enumerate(steps):
            step_header = f"--- STEP {i+1} ---\n"
            self.output_text.insert(tk.END, step_header)
            self.output_text.insert(tk.END, step + "\n\n")
        
        total_tokens = sum(tokenize(step) for step in steps)
        footer = f"\n=== TOTAL TOKENS: {total_tokens} ===\n"
        self.output_text.insert(tk.END, footer)
        
        self.status_bar.config(text=f"Optimization complete. Using {parser_used}. Total tokens: {total_tokens}")
        
        # Scroll to the top of the output
        self.output_text.see("1.0")

    def _show_error(self, error_msg):
        """Show error message and re-enable UI."""
        messagebox.showerror("Error", f"An error occurred: {error_msg}")
        self.status_bar.config(text="Error occurred")
        self.optimize_button.config(state="normal")

    def copy_to_clipboard(self):
        """Copy the optimized output to clipboard."""
        output = self.output_text.get("1.0", tk.END)
        if not output.strip():
            messagebox.showinfo("Info", "No content to copy.")
            return
            
        self.master.clipboard_clear()
        self.master.clipboard_append(output)
        self.status_bar.config(text="Copied to clipboard")

    def export_to_txt(self):
        """Export the optimized output to a text file"""
        output_text = self.output_text.get("1.0", tk.END).strip()
        if not output_text:
            self._show_error("No content to export")
            return
            
        # Ask user for file location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Output As"
        )
        
        if not file_path:
            return  # User cancelled
            
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(output_text)
            
            self.status_bar.config(text=f"Exported to {os.path.basename(file_path)}")
            
            # Ask if user wants to open the file
            if messagebox.askyesno("File Saved", 
                                 f"Output saved to {os.path.basename(file_path)}. Do you want to open it?"):
                # Open the file with the default application
                if platform.system() == 'Windows':
                    os.startfile(file_path)
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.call(('open', file_path))
                else:  # Linux and other Unix-like
                    subprocess.call(('xdg-open', file_path))
                    
        except Exception as e:
            self._show_error(f"Error exporting to file: {e}")

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        global THEME_BG, THEME_FG, THEME_BUTTON, THEME_HIGHLIGHT, THEME_ACCENT, THEME_MENUBAR
        
        # Toggle the dark mode flag
        self.is_dark_mode = not self.is_dark_mode
        
        # Set the appropriate theme variables
        if self.is_dark_mode:
            THEME_BG = DARK_THEME_BG
            THEME_FG = DARK_THEME_FG
            THEME_BUTTON = DARK_THEME_BUTTON
            THEME_HIGHLIGHT = DARK_THEME_HIGHLIGHT
            THEME_ACCENT = DARK_THEME_ACCENT
            THEME_MENUBAR = DARK_THEME_MENUBAR
            self.theme_button.config(text="☀️ Light Mode")
        else:
            THEME_BG = LIGHT_THEME_BG
            THEME_FG = LIGHT_THEME_FG
            THEME_BUTTON = LIGHT_THEME_BUTTON
            THEME_HIGHLIGHT = LIGHT_THEME_HIGHLIGHT
            THEME_ACCENT = LIGHT_THEME_ACCENT
            THEME_MENUBAR = LIGHT_THEME_MENUBAR
            self.theme_button.config(text="🌙 Dark Mode")
        
        # Update the window and all widgets
        self.master.configure(bg=THEME_BG)
        
        # Update ttk styles
        self.style.configure("TButton", background=THEME_BUTTON, foreground=THEME_FG)
        self.style.configure("TLabel", background=THEME_BG, foreground=THEME_FG)
        self.style.configure("TEntry", fieldbackground=THEME_HIGHLIGHT, foreground=THEME_FG)
        self.style.configure("TFrame", background=THEME_BG)
        
        # Update text widgets
        self.prompt_text.config(bg=THEME_HIGHLIGHT, fg=THEME_FG, insertbackground=THEME_FG)
        self.output_text.config(bg=THEME_HIGHLIGHT, fg=THEME_FG, insertbackground=THEME_FG)
        
        # Update window bar color if on Windows
        if platform.system() == "Windows":
            try:
                windll.dwmapi.DwmSetWindowAttribute(
                    windll.user32.GetParent(self.master.winfo_id()), 
                    20,  # DWMWA_CAPTION_COLOR
                    byref(c_int(int(THEME_MENUBAR.lstrip('#'), 16))), 
                    sizeof(c_int)
                )
            except Exception as e:
                print(f"Could not set window bar color: {e}")
                
        # Update status bar if it exists
        if hasattr(self, 'status_bar'):
            self.status_bar.config(background=THEME_BG, foreground=THEME_FG)

def main():
    # Check if running as bundled executable
    if getattr(sys, 'frozen', False):
        # If we're running as a PyInstaller bundle
        application_path = os.path.dirname(sys.executable)
    else:
        # If we're running as a script
        application_path = os.path.dirname(os.path.abspath(__file__))
        
    # Set up logging
    import logging
    log_file = os.path.join(application_path, 'tokenizer.log')
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Look for Ghidra if not already found
    if not GHIDRA_HEADLESS_PATH:
        find_ghidra()
    
    # Create main window
    root = tk.Tk()
    
    # Set window title with version number
    root.title("Code Prompt Optimizer v3 - Advanced")
    
    # Icon paths
    custom_icon_path = r"C:\Users\sethk\OneDrive\Documents\tokenizerv2-github\icon.ico"
    default_icon_path = os.path.join(application_path, "icon.ico")
    
    # Try to set the application icon using multiple approaches
    icons_set = False
    
    # First, try loading with PIL and setting with iconphoto
    icon_path = custom_icon_path if os.path.exists(custom_icon_path) else default_icon_path
    if os.path.exists(icon_path):
        try:
            # Create multiple sizes for better display across different contexts
            img = Image.open(icon_path)
            icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
            icons = []
            
            for size in icon_sizes:
                resized_img = img.resize(size, Image.LANCZOS)
                icons.append(ImageTk.PhotoImage(resized_img))
                
            # Set the window icon with the largest size
            root.iconphoto(True, icons[-1])
            
            # Store references to prevent garbage collection
            root.icons = icons
            
            print(f"Set icon using PIL and iconphoto from: {icon_path}")
            icons_set = True
        except Exception as e:
            print(f"Error setting icon with PIL: {e}")
    
    # Fallback to iconbitmap if PIL method failed
    if not icons_set:
        if os.path.exists(custom_icon_path):
            try:
                root.iconbitmap(custom_icon_path)
                print(f"Set icon using iconbitmap from: {custom_icon_path}")
                icons_set = True
            except Exception as e:
                print(f"Error setting icon with iconbitmap: {e}")
        
        if not icons_set and os.path.exists(default_icon_path):
            try:
                root.iconbitmap(default_icon_path)
                print(f"Set icon using iconbitmap from: {default_icon_path}")
                icons_set = True
            except Exception as e:
                print(f"Error setting icon with iconbitmap: {e}")
    
    # Last resort: try with tk.PhotoImage directly
    if not icons_set and os.path.exists(icon_path):
        try:
            icon = tk.PhotoImage(file=icon_path)
            root.iconphoto(True, icon)
            root.icon = icon  # Keep a reference
            print(f"Set icon using tk.PhotoImage from: {icon_path}")
        except Exception as e:
            print(f"Error setting icon with tk.PhotoImage: {e}")
    
    # Initialize the application
    app = TokenizerGUI(root)
    
    root.mainloop()

if __name__ == "__main__":
    main() 