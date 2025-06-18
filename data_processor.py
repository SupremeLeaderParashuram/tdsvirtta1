import json
import re
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle

class TDSDataProcessor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.course_data = []
        self.discourse_data = []
        self.all_texts = []
        self.tfidf_matrix = None
        
    def process_course_html(self, html_file):
        """Process course HTML dump"""
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract course sections
        sections = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        content_blocks = soup.find_all(['p', 'div', 'li', 'td'])
        
        current_section = "General"
        
        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'li']):
            if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                current_section = element.get_text().strip()
            else:
                text = element.get_text().strip()
                if len(text) > 20:  # Filter out short snippets
                    self.course_data.append({
                        'type': 'course',
                        'section': current_section,
                        'content': text,
                        'source': 'TDS Course Content'
                    })
    
    def process_discourse_posts(self, json_file):
        """Process discourse posts JSON"""
        with open(json_file, 'r', encoding='utf-8') as f:
            posts = json.load(f)
        
        for post in posts:
            content = post.get('content', '') or post.get('title', '')
            if len(content) > 20:
                self.discourse_data.append({
                    'type': 'discourse',
                    'title': post.get('title', ''),
                    'content': content,
                    'url': post.get('url', ''),
                    'date': post.get('date', ''),
                    'source': 'Discourse Post'
                })
    
    def build_search_index(self):
        """Build TF-IDF search index"""
        all_data = self.course_data + self.discourse_data
        self.all_texts = [item['content'] for item in all_data]
        
        if self.all_texts:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.all_texts)
            return all_data
        return []
    
    def search(self, query, top_k=5):
        """Search for relevant content"""
        if self.tfidf_matrix is None or self.tfidf_matrix.shape[0] == 0:
            return []
        
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)[0]
        
        # Get top k most similar documents
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        all_data = self.course_data + self.discourse_data
        results = []
        
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                item = all_data[idx].copy()
                item['similarity'] = similarities[idx]
                results.append(item)
        
        return results

    
    def save_processed_data(self, filename):
        """Save processed data and search index"""
        data = {
            'course_data': self.course_data,
            'discourse_data': self.discourse_data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        # Save vectorizer and matrix
        with open('search_index.pkl', 'wb') as f:
            pickle.dump({
                'vectorizer': self.vectorizer,
                'tfidf_matrix': self.tfidf_matrix,
                'all_data': self.course_data + self.discourse_data
            }, f)
    
    def load_processed_data(self, filename):
        """Load processed data and search index"""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.course_data = data['course_data']
        self.discourse_data = data['discourse_data']
        
        try:
            with open('search_index.pkl', 'rb') as f:
                index_data = pickle.load(f)
                self.vectorizer = index_data['vectorizer']
                self.tfidf_matrix = index_data['tfidf_matrix']
        except FileNotFoundError:
            print("Search index not found, rebuilding...")
            self.build_search_index()

if __name__ == "__main__":
    processor = TDSDataProcessor()
    
    # Process data files
    try:
        processor.process_course_html('data/tds_course_dump.html')
        print("✅ Processed course HTML")
    except FileNotFoundError:
        print("⚠️ Course HTML file not found")
    
    try:
        processor.process_discourse_posts('data/tds_discourse_posts.json')
        print("✅ Processed discourse posts")
    except FileNotFoundError:
        print("⚠️ Discourse posts file not found")
    
    # Build search index
    all_data = processor.build_search_index()
    print(f"✅ Built search index with {len(all_data)} documents")
    
    # Save processed data
    processor.save_processed_data('data/processed_data.json')
    print("✅ Saved processed data")
