"""Session Recording Service"""

import json
import time
import asyncio
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
import uuid

@dataclass
class SessionEvent:
    """Recorded session event"""
    timestamp: float
    event_type: str  # 'task', 'action', 'result', 'error'
    data: Dict[str, Any]

class SessionRecorder:
    """Record and playback agent sessions"""
    
    def __init__(self, session_dir: Path = None):
        self.session_dir = session_dir or Path.home() / ".linux-use" / "sessions"
        self.session_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_session_id = None
        self.events: List[SessionEvent] = []
        self.is_recording = False
    
    def start_recording(self, session_name: str = None) -> str:
        """Start recording a new session"""
        self.current_session_id = session_name or f"session_{int(time.time())}"
        self.events = []
        self.is_recording = True
        
        self.record_event('session_start', {
            'session_id': self.current_session_id,
            'timestamp': time.time()
        })
        
        return self.current_session_id
    
    def stop_recording(self) -> str:
        """Stop recording and save session"""
        if not self.is_recording:
            return None
        
        self.record_event('session_end', {
            'session_id': self.current_session_id,
            'timestamp': time.time(),
            'duration': time.time() - self.events[0].timestamp
        })
        
        self.is_recording = False
        
        # Save to file
        return self.save_session()
    
    def record_event(self, event_type: str, data: Dict[str, Any]):
        """Record an event"""
        if not self.is_recording:
            return
        
        event = SessionEvent(
            timestamp=time.time(),
            event_type=event_type,
            data=data
        )
        self.events.append(event)
    
    def save_session(self) -> str:
        """Save session to file"""
        if not self.current_session_id:
            return None
        
        session_file = self.session_dir / f"{self.current_session_id}.json"
        
        session_data = {
            'session_id': self.current_session_id,
            'events': [asdict(event) for event in self.events]
        }
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        return str(session_file)
    
    def load_session(self, session_id: str) -> List[SessionEvent]:
        """Load a recorded session"""
        session_file = self.session_dir / f"{session_id}.json"
        
        if not session_file.exists():
            raise FileNotFoundError(f"Session {session_id} not found")
        
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        
        events = [
            SessionEvent(**event)
            for event in session_data['events']
        ]
        
        return events
    
    def list_sessions(self) -> List[str]:
        """List all recorded sessions"""
        sessions = []
        for session_file in self.session_dir.glob("*.json"):
            sessions.append(session_file.stem)
        return sorted(sessions, reverse=True)
    
    async def playback_session(self, session_id: str, callback=None):
        """Playback a recorded session"""
        events = self.load_session(session_id)
        
        start_time = events[0].timestamp
        
        for event in events:
            # Wait for relative time
            relative_time = event.timestamp - start_time
            await asyncio.sleep(relative_time)
            
            if callback:
                callback(event)
