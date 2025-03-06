
# Code Prompt Optimizer Upgrade Plan

**Objective**: Transform the app into an all-purpose code optimizer supporting a wide range of languages, binary files, and an enhanced GUI with predictive text (Tab selection) and a sleek, modern design, while maintaining existing functionality. Compile the final app into a standalone executable that doesn’t require a Python installation.

**Current Date**: March 05, 2025  
**Target Completion**: TBD (adjust based on your timeline)

---

## Full Library List
These libraries will be integrated and bundled into the executable:

1. **`tiktoken`** - AI-compatible tokenization
2. **`nltk`** - Natural language processing and predictive text corpus
3. **`ast`** - Python parsing (built-in)
4. **`BeautifulSoup`** - HTML/XML parsing (`bs4`)
5. **`esprima-python`** - JavaScript parsing
6. **`pycparser`** - C/C++ parsing
7. **`tree-sitter`** - Multi-language parsing (via bindings)
8. **`css-parser`** - CSS parsing
9. **`javalang`** - Java parsing
10. **`black`** - Python code formatting
11. **`prettier`** - Web language formatting (via subprocess)
12. **`pyflakes`** - Python semantic optimization
13. **`chardet`** - File encoding detection
14. **`pathlib`** - Modern file path handling (built-in)
15. **`construct`** - Binary structure parsing
16. **`pefile`** - Windows PE binary analysis
17. **`pyelftools`** - ELF binary analysis
18. **`capstone`** - Binary disassembly
19. **`r2pipe`** - Advanced binary analysis (radare2 bindings)
20. **`ghidra`** - Binary decompilation (optional, via scripting)

---

## Phase 1: Library Integration and Core Enhancements

### 1. Replace Tokenization with `tiktoken`
- [ ] **Task**: Update `tokenize()` to use `tiktoken` for accurate token counting.
- **Description**: Replace `len(text.split())` with `tiktoken.get_encoding("cl100k_base").encode(text)`.
- **Maintain Functionality**: Verify `MAX_TOKEN_LIMIT` (2500) and `MAX_TOKENS_PER_STEP` (500) still enforce limits.
- **Dependencies**: `pip install tiktoken`

### 2. Implement Multi-Language Parsing with `tree-sitter`
- [ ] **Task**: Replace regex in `extract_code_blocks()` with `tree-sitter` for broad language support.
- **Description**: Use `tree_sitter` bindings and grammars (e.g., Python, JavaScript, C) to extract code blocks.
- **Maintain Functionality**: Fallback to regex for unsupported languages; return list of strings.
- **Dependencies**: `pip install tree_sitter`, plus language grammars.

### 3. Add Specific Language Parsers
- [ ] **Task**: Integrate `ast`, `BeautifulSoup`, `esprima-python`, `pycparser`, `css-parser`, and `javalang`.
- **Description**: Dispatch parsing in `extract_code_blocks()` based on file extension (e.g., `.py` → `ast`, `.html` → `BeautifulSoup`).
- **Maintain Functionality**: Ensure output integrates with `generate_steps()`.
- **Dependencies**: `pip install beautifulsoup4 esprima-python pycparser css-parser javalang`

### 4. Binary Handling with `construct`, `pefile`, `pyelftools`, `capstone`, `r2pipe`, and `ghidra`
- [ ] **Task**: Add binary file support to `extract_code_blocks()`.
- **Description**: Use `construct` for structures, `pefile`/`pyelftools` for PE/ELF metadata, `capstone` for disassembly, `r2pipe` for advanced analysis, and `ghidra` (optional) for decompilation.
- **Maintain Functionality**: Extract text or assembly as strings; handle errors gracefully.
- **Dependencies**: `pip install construct pefile pyelftools capstone r2pipe` (Ghidra requires external setup).

### 5. Enhance Code Optimization with `black`, `prettier`, and `pyflakes`
- [ ] **Task**: Upgrade `optimize_text()` with formatting and semantic cleanup.
- **Description**: Use `black` for Python, `prettier` (subprocess) for web languages, and `pyflakes` for unused code removal.
- **Maintain Functionality**: Preserve comment removal and whitespace normalization.
- **Dependencies**: `pip install black pyflakes` (Prettier requires Node.js).

### 6. Add Utility Libraries: `chardet` and `pathlib`
- [ ] **Task**: Integrate `chardet` for encoding detection and `pathlib` for file handling.
- **Description**: Wrap file reading in `extract_code_blocks()` with `chardet`; replace `os.path` with `pathlib`.
- **Maintain Functionality**: Ensure file reading remains robust across platforms.
- **Dependencies**: `pip install chardet`

---

## Phase 2: GUI Modernization and Predictive Text

### 7. Redesign GUI for Sleek, Modern Look
- [ ] **Task**: Update `TokenizerGUI` with `ttk` widgets and a dark theme.
- **Description**: Use `ttk` for buttons, labels, and entries; set background to `#2d2d2d`, text to white, buttons to `#4a4a4a`; improve layout with padding.
- **Maintain Functionality**: Retain prompt input, file selection, and output display; ensure `optimize()` works.
- **Dependencies**: None (uses `tkinter.ttk`).

### 8. Add Predictive Text with Tab Selection
- [ ] **Task**: Implement auto-completion in the prompt `Text` widget using `nltk` and Tab key binding.
- **Description**: Use `nltk.corpus.words` for suggestions; bind `<Tab>` to cycle through matches; display inline or in a dropdown.
- **Maintain Functionality**: Ensure prompt text feeds into `optimize()` unchanged.
- **Dependencies**: `pip install nltk` (run `nltk.download('words')`).

### 9. Enhance Output Feedback
- [ ] **Task**: Add a status bar to `TokenizerGUI` for processing details.
- **Description**: Use a `ttk.Label` to show “Parsed with AST”, “Tokens Saved: X”, etc., updated in `optimize()`.
- **Maintain Functionality**: Keep scrolled text output intact.
- **Dependencies**: None.

---

## Phase 3: Testing and Polish

### 10. Test Existing Functionality
- [ ] **Task**: Verify original features work with new libraries and GUI.
- **Description**: Test `.py`, `.js`, `.html`, `.css`, `.txt` files; check prompt splitting and token limits.
- **Maintain Functionality**: Fix regressions (e.g., file reading, step generation).

### 11. Test New Features
- [ ] **Task**: Validate language support, binary handling, and GUI enhancements.
- **Description**: Test Java, C, binaries (`.exe`), predictive text, and modern design.
- **Maintain Functionality**: Ensure new features integrate seamlessly.

### 12. Optimize Performance
- [ ] **Task**: Profile and optimize for large inputs.
- **Description**: Use `cProfile` to find bottlenecks (e.g., `tree-sitter` parsing); cache results if needed.
- **Maintain Functionality**: Ensure GUI responsiveness and output accuracy.

---

## Phase 4: Deployment

### 13. Compile Code into Standalone Executable with `PyInstaller`
- [ ] **Task**: Bundle the app and all dependencies into a single executable using `PyInstaller`.
- **Description**: 
  - Install `PyInstaller` (`pip install pyinstaller`).
  - Run `pyinstaller --onefile --add-data "path/to/tree-sitter-grammars;tree_sitter" main.py` (adjust for your script name and grammar paths).
  - Include `nltk` data: Download `words` corpus locally and add with `--add-data "path/to/nltk_data;nltk_data"`.
  - Handle `prettier` by embedding a Node.js runtime or excluding it (use Python-only alternatives if possible).
  - Test the executable on a clean machine without Python installed.
- **Maintain Functionality**: Ensure GUI, file handling, and optimization work without external dependencies; handle `tree-sitter` grammar files and `nltk` data explicitly.
- **Dependencies**: `pip install pyinstaller`
- **Notes**: 
  - Exclude `ghidra` from the bundle (too large; make it optional via external call).
  - Resulting executable size may be large (50-200 MB) due to library dependencies.

---

## Sample Implementation Snippets

### Updated `tokenize()` with `tiktoken`
```python
import tiktoken

def tokenize(text: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))
```

### Multi-Language Parsing with `tree-sitter`
```python
from tree_sitter import Language, Parser

PY_LANG = Language('build/python.so', 'python')
JS_LANG = Language('build/javascript.so', 'javascript')
PARSER = Parser()

def extract_code_blocks(file_path: str) -> List[str]:
    ext = os.path.splitext(file_path)[1].lower()
    lang_map = {'.py': PY_LANG, '.js': JS_LANG}  # Add more
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if ext in lang_map:
        PARSER.set_language(lang_map[ext])
        tree = PARSER.parse(content.encode())
        return [content[node.start_byte:node.end_byte] for node in tree.root_node.children if node.type in ('function_definition', 'class_definition')]
    return [content.strip()]  # Fallback
```

### Modern GUI with Predictive Text
```python
import tkinter as tk
from tkinter import ttk
import nltk
from nltk.corpus import words

nltk.download('words')
WORD_LIST = set(words.words())

class TokenizerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Code Prompt Optimizer")
        master.geometry("600x400")
        master.configure(bg="#2d2d2d")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", padding=5, background="#4a4a4a", foreground="white")
        style.configure("TLabel", background="#2d2d2d", foreground="white")

        ttk.Label(master, text="Enter Your Prompt:").pack(pady=5)
        self.prompt_text = tk.Text(master, height=4, width=60, bg="#3c3c3c", fg="white", insertbackground="white")
        self.prompt_text.pack(pady=5)
        self.prompt_text.bind("<Tab>", self.autocomplete)

        # File input and rest of GUI...

        self.status_bar = ttk.Label(master, text="Ready", anchor="w")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10)

    def autocomplete(self, event):
        current = self.prompt_text.get("insert linestart", "insert").split()[-1]
        suggestions = [w for w in WORD_LIST if w.startswith(current)][:5]
        if suggestions:
            self.prompt_text.delete("insert -1c wordstart", "insert")
            self.prompt_text.insert("insert", suggestions[0])  # Add dropdown later
        return "break"
```

### Compilation Command Example
```bash
# After installing dependencies and downloading nltk data
pyinstaller --onefile \
    --add-data "path/to/tree-sitter-grammars;tree_sitter" \
    --add-data "path/to/nltk_data;nltk_data" \
    main.py
```

---

## Notes
- **Dependencies**: Install via `pip` as listed; `tree-sitter` requires grammar builds; `prettier` needs Node.js (consider excluding or embedding); `ghidra` is optional.
- **GUI Design**: Dark theme (`#2d2d2d` background, `#4a4a4a` buttons) for modern look; predictive text uses `nltk`.
- **Compilation**: 
  - Use `--onefile` for a single executable; `--add-data` for `tree-sitter` grammars and `nltk` data.
  - Test on Windows, macOS, or Linux to ensure cross-platform compatibility.
  - Exclude large tools like `ghidra` from the bundle to keep size manageable.

This updated plan now includes compiling the code into a standalone executable with `PyInstaller`. Let me know if you’d like a detailed guide for the compilation step or help with any specific phase!