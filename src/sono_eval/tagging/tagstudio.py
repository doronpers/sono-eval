"""
TagStudio integration for file management and automated tagging.

Provides interface for organizing and tagging assessment artifacts.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from sono_eval.tagging.generator import SemanticTag, TagGenerator
from sono_eval.utils.config import get_config
from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)


class TagStudioManager:
    """
    TagStudio integration for file management and tagging.
    
    Features:
    - Automated file organization
    - Semantic tagging of code files
    - Tag-based search and retrieval
    - Integration with TagGenerator
    """

    def __init__(self, root_path: Optional[Path] = None):
        """Initialize TagStudio manager."""
        self.config = get_config()
        self.root_path = root_path or self.config.get_tagstudio_root()
        self.auto_tag = self.config.tagstudio_auto_tag
        self.tag_generator = TagGenerator()
        
        # Create directory structure
        self.files_dir = self.root_path / "files"
        self.tags_dir = self.root_path / "tags"
        self.index_file = self.root_path / "index.json"
        
        self.files_dir.mkdir(parents=True, exist_ok=True)
        self.tags_dir.mkdir(parents=True, exist_ok=True)
        
        self._index = self._load_index()
        
        logger.info(f"Initialized TagStudio at {self.root_path}")

    def add_file(
        self,
        file_path: Path,
        content: Optional[str] = None,
        auto_tag: Optional[bool] = None,
        custom_tags: Optional[List[str]] = None,
    ) -> str:
        """
        Add a file to TagStudio with optional auto-tagging.

        Args:
            file_path: Path to the file
            content: File content (if not provided, will read from file_path)
            auto_tag: Override auto-tagging setting
            custom_tags: Additional custom tags

        Returns:
            File ID
        """
        if content is None and file_path.exists():
            content = file_path.read_text()
        
        if content is None:
            logger.error(f"No content available for {file_path}")
            return ""

        # Generate file ID
        file_id = f"file_{len(self._index)}"
        
        # Store file
        stored_path = self.files_dir / f"{file_id}_{file_path.name}"
        stored_path.write_text(content)
        
        # Generate tags
        tags = []
        if auto_tag if auto_tag is not None else self.auto_tag:
            semantic_tags = self.tag_generator.generate_tags(content)
            tags.extend([t.tag for t in semantic_tags])
        
        if custom_tags:
            tags.extend(custom_tags)
        
        # Update index
        self._index[file_id] = {
            "file_id": file_id,
            "original_name": file_path.name,
            "stored_path": str(stored_path),
            "tags": tags,
            "metadata": {
                "size": len(content),
                "extension": file_path.suffix,
            },
        }
        
        self._save_index()
        
        # Store tags
        self._update_tag_index(file_id, tags)
        
        logger.info(f"Added file {file_path.name} with ID {file_id} and {len(tags)} tags")
        return file_id

    def get_file(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Get file metadata by ID."""
        return self._index.get(file_id)

    def search_by_tags(self, tags: List[str]) -> List[Dict[str, Any]]:
        """
        Search for files by tags.

        Args:
            tags: List of tags to search for

        Returns:
            List of matching file entries
        """
        results = []
        for file_id, file_data in self._index.items():
            file_tags = set(file_data.get("tags", []))
            if any(tag in file_tags for tag in tags):
                results.append(file_data)
        return results

    def add_tags(self, file_id: str, new_tags: List[str]) -> bool:
        """Add tags to an existing file."""
        if file_id not in self._index:
            return False
        
        self._index[file_id]["tags"].extend(new_tags)
        self._save_index()
        self._update_tag_index(file_id, new_tags)
        return True

    def remove_tags(self, file_id: str, tags_to_remove: List[str]) -> bool:
        """Remove tags from a file."""
        if file_id not in self._index:
            return False
        
        current_tags = self._index[file_id]["tags"]
        self._index[file_id]["tags"] = [
            t for t in current_tags if t not in tags_to_remove
        ]
        self._save_index()
        return True

    def list_all_tags(self) -> List[str]:
        """List all unique tags in the system."""
        all_tags = set()
        for file_data in self._index.values():
            all_tags.update(file_data.get("tags", []))
        return sorted(all_tags)

    def get_tag_statistics(self) -> Dict[str, int]:
        """Get statistics about tag usage."""
        tag_counts = {}
        for file_data in self._index.values():
            for tag in file_data.get("tags", []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        return dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True))

    def _update_tag_index(self, file_id: str, tags: List[str]) -> None:
        """Update the reverse tag index."""
        for tag in tags:
            tag_file = self.tags_dir / f"{tag}.json"
            
            if tag_file.exists():
                with open(tag_file, "r") as f:
                    tag_data = json.load(f)
            else:
                tag_data = {"tag": tag, "files": []}
            
            if file_id not in tag_data["files"]:
                tag_data["files"].append(file_id)
            
            with open(tag_file, "w") as f:
                json.dump(tag_data, f, indent=2)

    def _load_index(self) -> Dict[str, Any]:
        """Load the main index file."""
        if self.index_file.exists():
            with open(self.index_file, "r") as f:
                return json.load(f)
        return {}

    def _save_index(self) -> None:
        """Save the main index file."""
        with open(self.index_file, "w") as f:
            json.dump(self._index, f, indent=2)
