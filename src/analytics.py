from functools import cached_property
from typing import TypedDict, Literal, List, Dict, Any
from datetime import UTC, datetime
import json

# Python 3.8 TypedDict for structured data
class TodoStats(TypedDict):
    total_count: int
    completed_count: int
    pending_count: int
    completion_rate: float
    avg_title_length: float

# Python 3.8 Literal types for status
TodoStatus = Literal['completed', 'pending', 'all']

class TodoAnalytics:
    def __init__(self, todos: List[Dict[str, Any]]):
        self._todos = todos
        self._last_updated = datetime.now(UTC).replace(tzinfo=None)
    
    @cached_property  # Python 3.8 cached_property
    def stats(self) -> TodoStats:
        """Calculate comprehensive todo statistics."""
        total = len(self._todos)
        completed = sum(1 for todo in self._todos if todo.get('completed', False))
        
        return TodoStats(
            total_count=total,
            completed_count=completed,
            pending_count=total - completed,
            completion_rate=completed / total if total > 0 else 0.0,
            avg_title_length=sum(len(todo.get('title', '')) for todo in self._todos) / total if total > 0 else 0.0
        )
    
    @cached_property
    def completion_trend(self) -> Dict[str, int]:
        """Analyze completion patterns by hour."""
        trends = {}
        for todo in self._todos:
            if todo.get('completed') and (updated := todo.get('updated_at')):
                try:
                    hour = datetime.fromisoformat(updated.replace('Z', '+00:00')).hour
                    trends[f"{hour:02d}:00"] = trends.get(f"{hour:02d}:00", 0) + 1
                except ValueError:
                    continue
        return trends
    
    def filter_by_status(self, status: TodoStatus, /) -> List[Dict[str, Any]]:
        """Filter todos by status using Literal type."""
        if status == 'completed':
            return [t for t in self._todos if t.get('completed', False)]
        elif status == 'pending':
            return [t for t in self._todos if not t.get('completed', False)]
        return self._todos
    
    def generate_report(self, /, *, format_type: Literal['json', 'summary'] = 'summary') -> str:
        """Generate analytics report in specified format."""
        stats = self.stats
        
        if format_type == 'json':
            return json.dumps({
                'stats': stats,
                'trends': self.completion_trend,
                'generated_at': self._last_updated.isoformat()
            }, indent=2)
        
        # Summary format with f-string debugging (Python 3.8)
        return f"""Todo Analytics Report
Generated: {self._last_updated.isoformat()}

Statistics:
- Total todos: {stats['total_count']=}
- Completed: {stats['completed_count']=}
- Pending: {stats['pending_count']=}
- Completion rate: {stats['completion_rate']:.1%}
- Average title length: {stats['avg_title_length']:.1f} chars

Completion Trends: {len(self.completion_trend)} active hours
"""
