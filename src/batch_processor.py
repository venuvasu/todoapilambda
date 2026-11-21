import math
import statistics
from typing import List, Dict, Any, Iterator, Tuple
from datetime import UTC, datetime, timedelta
from collections import Counter

class TodoBatchProcessor:
    def __init__(self, batch_size: int = 10):
        self.batch_size = batch_size
    
    def process_completion_metrics(self, todos: List[Dict[str, Any]], /) -> Dict[str, float]:
        """Calculate completion metrics using Python 3.8 math.prod and statistics."""
        if not todos:
            return {}
        
        # Extract completion times
        completion_times = []
        title_lengths = []
        
        for todo in todos:
            if todo.get('completed') and (updated := todo.get('updated_at')):
                try:
                    created = datetime.fromisoformat(todo['created_at'].replace('Z', '+00:00'))
                    updated_dt = datetime.fromisoformat(updated.replace('Z', '+00:00'))
                    completion_times.append((updated_dt - created).total_seconds() / 3600)  # hours
                except (ValueError, KeyError):
                    continue
            
            if title := todo.get('title'):
                title_lengths.append(len(title))
        
        metrics = {}
        
        # Statistics module functions (Python 3.8)
        if completion_times:
            metrics.update({
                'avg_completion_time': statistics.mean(completion_times),
                'median_completion_time': statistics.median(completion_times),
                'completion_time_stdev': statistics.stdev(completion_times) if len(completion_times) > 1 else 0.0
            })
        
        if title_lengths:
            metrics.update({
                'avg_title_length': statistics.mean(title_lengths),
                'title_length_mode': statistics.mode(title_lengths) if title_lengths else 0
            })
        
        # Math.prod for compound calculations (Python 3.8)
        if len(todos) >= 3:
            recent_completion_rates = [
                1.0 if todo.get('completed') else 0.1 
                for todo in todos[-3:]
            ]
            metrics['compound_completion_factor'] = math.prod(recent_completion_rates)
        
        return metrics
    
    def batch_validate_titles(self, todos: List[Dict[str, Any]], /) -> Iterator[Tuple[int, Dict[str, Any]]]:
        """Process todos in batches for validation."""
        for i in range(0, len(todos), self.batch_size):
            batch = todos[i:i + self.batch_size]
            
            # Calculate batch statistics
            batch_stats = {
                'batch_index': i // self.batch_size,
                'batch_size': len(batch),
                'title_lengths': [len(todo.get('title', '')) for todo in batch],
                'completion_rate': sum(1 for todo in batch if todo.get('completed')) / len(batch)
            }
            
            # Use math functions for analysis
            if batch_stats['title_lengths']:
                lengths = batch_stats['title_lengths']
                batch_stats.update({
                    'length_variance': statistics.variance(lengths) if len(lengths) > 1 else 0.0,
                    'length_geometric_mean': math.prod(lengths) ** (1/len(lengths)) if all(l > 0 for l in lengths) else 0.0
                })
            
            yield i, batch_stats
    
    def calculate_priority_scores(self, todos: List[Dict[str, Any]], /) -> List[Tuple[str, float]]:
        """Calculate priority scores using mathematical functions."""
        scores = []
        
        for todo in todos:
            if not (todo_id := todo.get('id')):
                continue
            
            # Base score factors
            title_length = len(todo.get('title', ''))
            is_completed = todo.get('completed', False)
            
            try:
                created = datetime.fromisoformat(todo['created_at'].replace('Z', '+00:00'))
                age_hours = (datetime.now(UTC).replace(tzinfo=None) - created).total_seconds() / 3600
            except (ValueError, KeyError):
                age_hours = 0
            
            # Priority calculation using math functions
            if title_length > 0 and age_hours > 0:
                # Logarithmic decay for age, exponential for length
                age_factor = math.log(age_hours + 1)
                length_factor = math.exp(title_length / 100)  # Normalize
                completion_penalty = 0.1 if is_completed else 1.0
                
                score = (age_factor * length_factor * completion_penalty)
                scores.append((todo_id, score))
        
        return sorted(scores, key=lambda x: x[1], reverse=True)
    
    def analyze_completion_patterns(self, todos: List[Dict[str, Any]], /) -> Dict[str, Any]:
        """Analyze patterns using statistical functions."""
        if not todos:
            return {}
        
        # Group by completion status and day of week
        completion_by_day = Counter()
        completion_times_by_day = {}
        
        for todo in todos:
            if todo.get('completed') and (updated := todo.get('updated_at')):
                try:
                    dt = datetime.fromisoformat(updated.replace('Z', '+00:00'))
                    day_name = dt.strftime('%A')
                    completion_by_day[day_name] += 1
                    
                    if day_name not in completion_times_by_day:
                        completion_times_by_day[day_name] = []
                    completion_times_by_day[day_name].append(dt.hour)
                except ValueError:
                    continue
        
        # Statistical analysis
        patterns = {
            'completions_by_day': dict(completion_by_day),
            'most_productive_day': completion_by_day.most_common(1)[0] if completion_by_day else None
        }
        
        # Average completion hour by day
        for day, hours in completion_times_by_day.items():
            if hours:
                patterns[f'{day.lower()}_avg_hour'] = statistics.mean(hours)
                if len(hours) > 1:
                    patterns[f'{day.lower()}_hour_stdev'] = statistics.stdev(hours)
        
        return patterns
