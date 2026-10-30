import os
import chromadb
from pathlib import Path
from src.slicer.ast_parser import CodeSlicer

class LocalRepositoryRAG:
    """
    Lightweight local vector index over AST structure and project context.
    """
    def __init__(self, persist_directory: str = "./.CodeShield_chroma"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="codebase_slices")
        self.slicer = CodeSlicer()

    def index_slice(self, slice_id: str, code_content: str, metadata: dict = None):
        """
        Indexes a specific method/class slice.
        """
        self.collection.upsert(
            documents=[code_content],
            metadatas=[metadata or {}],
            ids=[slice_id]
        )

    def retrieve_context(self, query: str, n_results: int = 3) -> list[str]:
        """
        Retrieves relevant codebase slices for a given natural language query.
        """
        if self.collection.count() == 0:
            return []
            
        results = self.collection.query(
            query_texts=[query],
            n_results=min(n_results, self.collection.count())
        )
        return results["documents"][0] if results and "documents" in results and results["documents"] else []

    def index_directory(self, root_dir: str):
        """
        Walks through a directory, parses Python files, extracts function/class slices,
        and indexes them in ChromaDB.
        """
        root_path = Path(root_dir)
        count = 0
        for py_file in root_path.rglob("*.py"):
            if ".venv" in py_file.parts or "venv" in py_file.parts or "__pycache__" in py_file.parts:
                continue
                
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    source_code = f.read()
            except Exception:
                continue
                
            # Extract slices line by line (this is naive for prototyping. 
            # A true AST traversal would extract all nodes of type 'function_definition')
            # For this prototype, we'll extract slices for every 10th line to ensure some coverage
            lines = source_code.splitlines()
            seen_slices = set()
            
            for line_idx in range(0, len(lines), 10):
                slice_content = self.slicer.get_slice_for_line(source_code, line_idx + 1)
                
                if slice_content and slice_content not in seen_slices and len(slice_content) > 10:
                    seen_slices.add(slice_content)
                    slice_id = f"{py_file.relative_to(root_path)}:{line_idx + 1}"
                    
                    self.index_slice(
                        slice_id=slice_id,
                        code_content=slice_content,
                        metadata={"file": str(py_file), "line": line_idx + 1}
                    )
                    count += 1
                    
        return count


