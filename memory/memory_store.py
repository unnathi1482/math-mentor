"""
Memory Store - Saves and retrieves all interactions.

This module:
1. Stores every problem solved (input, solution, feedback)
2. Uses SQLite database for structured storage
3. Allows retrieval of past interactions
4. Tracks user feedback for learning
"""

import sqlite3
import json
import uuid
from datetime import datetime
from pathlib import Path

# Import our config
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import MEMORY_DB_PATH


class MemoryStore:
    """
    Stores and retrieves all math problem interactions.
    """
    
    def __init__(self, db_path: str = None):
        """
        Initialize the memory store.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path or MEMORY_DB_PATH
        self.name = "Memory Store"
        self._ensure_db_directory()
        self._create_tables()
    
    def _ensure_db_directory(self):
        """Create the directory for the database if it doesn't exist."""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
    
    def _create_tables(self):
        """Create the database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main interactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                input_type TEXT NOT NULL,
                raw_input TEXT NOT NULL,
                parsed_question TEXT,
                topic TEXT,
                retrieved_context TEXT,
                solution_steps TEXT,
                final_answer TEXT,
                confidence REAL,
                is_correct INTEGER,
                user_feedback TEXT,
                user_correction TEXT,
                explanation TEXT,
                agent_trace TEXT
            )
        """)
        
        # OCR corrections table (for learning OCR patterns)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ocr_corrections (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                original_ocr_text TEXT NOT NULL,
                corrected_text TEXT NOT NULL,
                image_description TEXT
            )
        """)
        
        # Audio corrections table (for learning audio patterns)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audio_corrections (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                original_transcript TEXT NOT NULL,
                corrected_text TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_interaction(self, interaction_data: dict) -> str:
        """
        Save a complete interaction to the database.
        
        Args:
            interaction_data: Dictionary with all interaction details
        
        Returns:
            The ID of the saved interaction
        """
        interaction_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO interactions (
                    id, timestamp, input_type, raw_input,
                    parsed_question, topic, retrieved_context,
                    solution_steps, final_answer, confidence,
                    is_correct, user_feedback, user_correction,
                    explanation, agent_trace
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                interaction_id,
                timestamp,
                interaction_data.get("input_type", "text"),
                interaction_data.get("raw_input", ""),
                json.dumps(interaction_data.get("parsed_question", {})),
                interaction_data.get("topic", ""),
                json.dumps(interaction_data.get("retrieved_context", [])),
                json.dumps(interaction_data.get("solution_steps", [])),
                interaction_data.get("final_answer", ""),
                interaction_data.get("confidence", 0.0),
                1 if interaction_data.get("is_correct", False) else 0,
                interaction_data.get("user_feedback", ""),
                interaction_data.get("user_correction", ""),
                interaction_data.get("explanation", ""),
                json.dumps(interaction_data.get("agent_trace", []))
            ))
            
            conn.commit()
            return interaction_id
            
        except Exception as e:
            print(f"❌ Error saving interaction: {e}")
            return None
        finally:
            conn.close()
    
    def update_feedback(self, interaction_id: str, feedback: str, correction: str = None):
        """
        Update the feedback for an existing interaction.
        
        Args:
            interaction_id: ID of the interaction
            feedback: "correct" or "incorrect"
            correction: User's correction if feedback is "incorrect"
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE interactions
                SET user_feedback = ?,
                    user_correction = ?,
                    is_correct = ?
                WHERE id = ?
            """, (
                feedback,
                correction or "",
                1 if feedback == "correct" else 0,
                interaction_id
            ))
            
            conn.commit()
            
        except Exception as e:
            print(f"❌ Error updating feedback: {e}")
        finally:
            conn.close()
    
    def get_interaction(self, interaction_id: str) -> dict:
        """
        Get a specific interaction by ID.
        
        Args:
            interaction_id: ID of the interaction
        
        Returns:
            Dictionary with interaction details
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM interactions WHERE id = ?", (interaction_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_dict(row, cursor.description)
            return None
            
        except Exception as e:
            print(f"❌ Error getting interaction: {e}")
            return None
        finally:
            conn.close()
    
    def get_recent_interactions(self, limit: int = 10) -> list:
        """
        Get the most recent interactions.
        
        Args:
            limit: Maximum number of interactions to return
        
        Returns:
            List of interaction dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT * FROM interactions ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
            
            return [self._row_to_dict(row, cursor.description) for row in rows]
            
        except Exception as e:
            print(f"❌ Error getting recent interactions: {e}")
            return []
        finally:
            conn.close()
    
    def get_interactions_by_topic(self, topic: str, limit: int = 10) -> list:
        """
        Get interactions filtered by topic.
        
        Args:
            topic: Topic to filter by
            limit: Maximum number of interactions to return
        
        Returns:
            List of interaction dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT * FROM interactions WHERE topic = ? ORDER BY timestamp DESC LIMIT ?",
                (topic, limit)
            )
            rows = cursor.fetchall()
            
            return [self._row_to_dict(row, cursor.description) for row in rows]
            
        except Exception as e:
            print(f"❌ Error getting interactions by topic: {e}")
            return []
        finally:
            conn.close()
    
    def get_correct_interactions(self, limit: int = 10) -> list:
        """
        Get interactions that were marked as correct.
        
        Args:
            limit: Maximum number to return
        
        Returns:
            List of correct interaction dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT * FROM interactions WHERE is_correct = 1 ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
            
            return [self._row_to_dict(row, cursor.description) for row in rows]
            
        except Exception as e:
            print(f"❌ Error getting correct interactions: {e}")
            return []
        finally:
            conn.close()
    
    def save_ocr_correction(self, original_text: str, corrected_text: str, image_description: str = ""):
        """
        Save an OCR correction for future learning.
        
        Args:
            original_text: What OCR produced
            corrected_text: What the user corrected it to
            image_description: Optional description of the image
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO ocr_corrections (id, timestamp, original_ocr_text, corrected_text, image_description)
                VALUES (?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()),
                datetime.now().isoformat(),
                original_text,
                corrected_text,
                image_description
            ))
            
            conn.commit()
            
        except Exception as e:
            print(f"❌ Error saving OCR correction: {e}")
        finally:
            conn.close()
    
    def save_audio_correction(self, original_transcript: str, corrected_text: str):
        """
        Save an audio transcription correction for future learning.
        
        Args:
            original_transcript: What Whisper produced
            corrected_text: What the user corrected it to
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO audio_corrections (id, timestamp, original_transcript, corrected_text)
                VALUES (?, ?, ?, ?)
            """, (
                str(uuid.uuid4()),
                datetime.now().isoformat(),
                original_transcript,
                corrected_text
            ))
            
            conn.commit()
            
        except Exception as e:
            print(f"❌ Error saving audio correction: {e}")
        finally:
            conn.close()
    
    def get_ocr_corrections(self) -> list:
        """Get all stored OCR corrections for learning."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM ocr_corrections ORDER BY timestamp DESC")
            rows = cursor.fetchall()
            
            return [self._row_to_dict(row, cursor.description) for row in rows]
            
        except Exception as e:
            print(f"❌ Error getting OCR corrections: {e}")
            return []
        finally:
            conn.close()
    
    def get_audio_corrections(self) -> list:
        """Get all stored audio corrections for learning."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM audio_corrections ORDER BY timestamp DESC")
            rows = cursor.fetchall()
            
            return [self._row_to_dict(row, cursor.description) for row in rows]
            
        except Exception as e:
            print(f"❌ Error getting audio corrections: {e}")
            return []
        finally:
            conn.close()
    
    def get_stats(self) -> dict:
        """
        Get statistics about stored interactions.
        
        Returns:
            Dictionary with various statistics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Total interactions
            cursor.execute("SELECT COUNT(*) FROM interactions")
            total = cursor.fetchone()[0]
            
            # Correct interactions
            cursor.execute("SELECT COUNT(*) FROM interactions WHERE is_correct = 1")
            correct = cursor.fetchone()[0]
            
            # By topic
            cursor.execute("SELECT topic, COUNT(*) FROM interactions GROUP BY topic")
            by_topic = dict(cursor.fetchall())
            
            # Average confidence
            cursor.execute("SELECT AVG(confidence) FROM interactions")
            avg_confidence = cursor.fetchone()[0] or 0.0
            
            # OCR corrections count
            cursor.execute("SELECT COUNT(*) FROM ocr_corrections")
            ocr_corrections = cursor.fetchone()[0]
            
            # Audio corrections count
            cursor.execute("SELECT COUNT(*) FROM audio_corrections")
            audio_corrections = cursor.fetchone()[0]
            
            return {
                "total_interactions": total,
                "correct_interactions": correct,
                "accuracy_rate": round(correct / total * 100, 1) if total > 0 else 0,
                "by_topic": by_topic,
                "average_confidence": round(avg_confidence, 3),
                "ocr_corrections": ocr_corrections,
                "audio_corrections": audio_corrections
            }
            
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            return {}
        finally:
            conn.close()
    
    def _row_to_dict(self, row, description) -> dict:
        """
        Convert a database row to a dictionary.
        
        Args:
            row: Database row tuple
            description: Column description from cursor
        
        Returns:
            Dictionary with column names as keys
        """
        columns = [col[0] for col in description]
        result = dict(zip(columns, row))
        
        # Parse JSON fields
        json_fields = ["parsed_question", "retrieved_context", "solution_steps", "agent_trace"]
        for field in json_fields:
            if field in result and result[field]:
                try:
                    result[field] = json.loads(result[field])
                except (json.JSONDecodeError, TypeError):
                    pass
        
        return result