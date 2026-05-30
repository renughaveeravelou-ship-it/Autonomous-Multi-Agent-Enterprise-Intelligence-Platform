# backend/rag.py

import os
import re

# Directory of the project workspace
WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class LocalRAGSystem:
    def __init__(self):
        self.documents = []
        self.build_index()

    def build_index(self):
        """Walks the workspace directory and indexes text-based description files."""
        # Folders we want to crawl
        folders_to_crawl = [
            "CUSTOMER SUPPORT AGENT",
            "EXECUTIVE CEO AGENT",
            "EXPLAINABLE AI LAYER",
            "FINANCE AGENT",
            "HR INTELLIGENCE AGENT",
            "KNOWLEDGE GRAPH",
            "MULTI AGENT COLLABORATION",
            "RAG SYSTEM",
            "RETAIL AGENT",
            "RISK AGENT",
            "SRC",
            "WHAT IF ANALYSIS"
        ]
        
        for folder in folders_to_crawl:
            folder_path = os.path.join(WORKSPACE_DIR, folder)
            if not os.path.exists(folder_path):
                continue
                
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                # Ensure it's a file and not a Python/Jupyter/hidden file
                if os.path.isfile(file_path) and not filename.endswith((".ipynb", ".py", ".sh", ".yml", ".yaml", ".conf", ".bat")):
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read().strip()
                        if content:
                            self.documents.append({
                                "folder": folder,
                                "title": filename,
                                "content": content,
                                "path": file_path
                            })
                    except Exception as e:
                        print(f"RAG indexing error on {file_path}: {e}")
                        
        print(f"RAG system indexed {len(self.documents)} local documents.")

    def retrieve(self, query: str, limit: int = 3):
        """Retrieves document snippets that contain terms matching the query."""
        words = re.findall(r"\w+", query.lower())
        if not words:
            return []
            
        scored_docs = []
        for doc in self.documents:
            score = 0
            doc_content_lower = doc["content"].lower()
            doc_title_lower = doc["title"].lower()
            
            for word in words:
                # Add score if matching title or content
                score += doc_title_lower.count(word) * 5
                score += doc_content_lower.count(word)
                
            if score > 0:
                scored_docs.append((score, doc))
                
        # Sort by score descending
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        
        results = []
        for score, doc in scored_docs[:limit]:
            results.append({
                "source": f"{doc['folder']} / {doc['title']}",
                "snippet": doc["content"],
                "score": score
            })
            
        return results

# Initialize a global instance
rag_engine = LocalRAGSystem()
