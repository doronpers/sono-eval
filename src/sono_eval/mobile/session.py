"""
Session management for mobile onboarding flow.

Handles server-side session persistence using MemUStorage, allowing
users to resume their assessment progress across devices or reloads.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from sono_eval.memory.memu import MemUStorage
from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)


class MobileSession(BaseModel):
    """
    Mobile assessment session state.

    Attributes:
        session_id: Unique session identifier
        candidate_id: Linked candidate ID (or 'guest')
        current_step: Current step in the onboarding flow (0-4)
        selected_paths: List of selected assessment paths
        answers: Dictionary of user answers/inputs
        created_at: Session creation timestamp
        last_active: Last activity timestamp
    """

    session_id: str
    candidate_id: str = "guest"
    current_step: int = 0
    selected_paths: List[str] = Field(default_factory=list)
    answers: Dict[str, str] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_active: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MobileSessionManager:
    """
    Manages persistent mobile sessions.

    Uses MemUStorage to persist session data, enabling recovery
    and state tracking throughout the assessment flow.
    """

    def __init__(self):
        self.storage = MemUStorage()

    def create_session(self, candidate_id: str = "guest") -> str:
        """
        Create a new mobile session.

        Args:
            candidate_id: Optional candidate ID to link

        Returns:
            New session ID
        """
        session_id = str(uuid.uuid4())
        session = MobileSession(session_id=session_id, candidate_id=candidate_id)

        # Store session as a "candidate" memory for persistence
        # We prefix with "session_" to distinguish from real candidates
        storage_id = f"session_{session_id}"

        self.storage.create_candidate_memory(
            candidate_id=storage_id, initial_data=session.model_dump(mode="json")
        )

        logger.info(f"Created mobile session {session_id} for {candidate_id}")
        return session_id

    def get_session(self, session_id: str) -> Optional[MobileSession]:
        """
        Retrieve a session by ID.

        Args:
            session_id: Session identifier

        Returns:
            MobileSession object or None if not found
        """
        if not session_id:
            return None

        storage_id = f"session_{session_id}"
        memory = self.storage.get_candidate_memory(storage_id)

        if not memory:
            return None

        try:
            data = memory.root_node.data
            return MobileSession(**data)
        except Exception as e:
            logger.error(f"Failed to parse session {session_id}: {e}")
            return None

    def update_session(self, session: MobileSession) -> bool:
        """
        Update session state.

        Args:
            session: Updated MobileSession object

        Returns:
            True if successful
        """
        if not session.session_id:
            return False

        session.last_active = datetime.now(timezone.utc)
        storage_id = f"session_{session.session_id}"
        root_node_id = f"{storage_id}_root"

        return bool(
            self.storage.update_memory_node(
                candidate_id=storage_id,
                node_id=root_node_id,
                data=session.model_dump(mode="json"),
            )
        )

    def update_step(self, session_id: str, step: int) -> bool:
        """
        Update current step in the flow.

        Args:
            session_id: Session identifier
            step: New step number

        Returns:
            True if successful
        """
        session = self.get_session(session_id)
        if not session:
            return False

        session.current_step = step
        return self.update_session(session)

    def link_candidate(self, session_id: str, candidate_id: str) -> bool:
        """
        Link a session to a specific candidate ID.

        Args:
            session_id: Session identifier
            candidate_id: Real candidate ID

        Returns:
            True if successful
        """
        session = self.get_session(session_id)
        if not session:
            return False

        session.candidate_id = candidate_id
        return self.update_session(session)
