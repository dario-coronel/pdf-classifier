import os
import joblib
import numpy as np
from typing import Dict, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import re
from config import Config
from services.rules import apply_rule_boost


class DocumentClassifier:
    """Machine Learning classifier for document types"""
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.label_encoder = {}
        self.reverse_label_encoder = {}
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize or load the ML model"""
        if os.path.exists(Config.MODEL_PATH) and os.path.exists(Config.VECTORIZER_PATH):
            self.load_model()
        else:
            self.create_new_model()
    
    def create_new_model(self):
        """Create a new ML model with default training data"""
        print("Creating new ML model...")
        
        # Create vectorizer with optimized parameters for Spanish documents
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 3),
            min_df=1,
            max_df=0.95,
            strip_accents=None,  # Keep accents for Spanish
            lowercase=True
        )
        
        # Create MLP Neural Network classifier
        # hidden_layer_sizes=(100, 50) means 2 hidden layers with 100 and 50 neurons
        self.model = MLPClassifier(
            hidden_layer_sizes=(100, 50),
            activation='relu',
            solver='adam',
            max_iter=300,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1,
            n_iter_no_change=10
        )
        
        # Initialize with basic training data
        self._train_with_default_data()
    
    def _train_with_default_data(self):
        """Train model with basic keyword-based examples"""
        # Training data with typical keywords for each document type
        training_data = [
            # Facturas
            ("factura tipo a original importe total iva inscripto cuit", "Factura"),
            ("factura b consumidor final comprobante fiscal punto venta", "Factura"),
            ("factura c monotributo fecha emisión razón social", "Factura"),
            ("factura electronica afip cae comprobante autorizado", "Factura"),
            ("comprobante venta detalle productos subtotal impuestos", "Factura"),
            
            # Notas de Débito
            ("nota debito ajuste cargo adicional factura original", "Nota de Debito"),
            ("debito incremento importe diferencia factura rectificativa", "Nota de Debito"),
            ("nota de debito tipo a intereses recargo mora", "Nota de Debito"),
            
            # Notas de Crédito
            ("nota credito devolucion descuento anulacion factura", "Nota de Credito"),
            ("credito ajuste favor cliente bonificacion rectificativa", "Nota de Credito"),
            ("nota de credito tipo rectifica comprobante original", "Nota de Credito"),
            
            # Remitos
            ("remito entrega mercaderia bultos transporte destinatario", "Remito"),
            ("remito envio cantidad articulos descripcion productos", "Remito"),
            ("comprobante entrega recibido conformidad firma sello", "Remito"),
            ("remito transporte destinatario receptor mercaderia", "Remito"),
            
            # Desconocidos
            ("documento generico texto aleatorio sin formato especifico", "Desconocido"),
        ]
        
        texts = [text for text, _ in training_data]
        labels = [label for _, label in training_data]
        
        # Encode labels
        unique_labels = list(set(labels))
        self.label_encoder = {label: idx for idx, label in enumerate(unique_labels)}
        self.reverse_label_encoder = {idx: label for label, idx in self.label_encoder.items()}
        
        # Transform data
        X = self.vectorizer.fit_transform(texts)
        y = np.array([self.label_encoder[label] for label in labels])
        
        # Train model
        self.model.fit(X, y)
        
        print(f"Model trained with {len(training_data)} examples")
        print(f"Classes: {list(self.label_encoder.keys())}")
    
    def classify(self, text: str) -> Tuple[str, float]:
        """
        Classify document text
        Returns: (predicted_type, confidence_score)
        """
        if not text or len(text.strip()) < 10:
            return "Desconocido", 0.0
        
        # Preprocess text
        processed_text = self._preprocess_text(text)
        
        # Rule-based classification (fallback)
        rule_based_type, rule_confidence = self._rule_based_classification(processed_text)
        
        # ML-based classification
        try:
            X = self.vectorizer.transform([processed_text])
            probabilities = self.model.predict_proba(X)[0]
            predicted_idx = np.argmax(probabilities)
            confidence = float(probabilities[predicted_idx])
            predicted_type = self.reverse_label_encoder.get(predicted_idx, "Desconocido")
            
            # Build probability mapping label -> prob
            probs = {self.reverse_label_encoder.get(i, 'Desconocido'): float(p)
                     for i, p in enumerate(probabilities)}

            # Apply rule-based boost/override (post-process)
            final_label, reason = apply_rule_boost(predicted_type, probs, text)

            # If reason indicates a rule override/boost, we may want to log it (print for now)
            if reason != 'no_rule' and final_label != predicted_type:
                # prefer returning a confidence consistent with probs
                final_conf = probs.get(final_label, confidence)
                print(f"Rule applied: {reason} -> {final_label} (from {predicted_type})")
                return final_label, float(final_conf)

            # If ML confidence is low, use rule-based fallback computed earlier
            if confidence < Config.MIN_CONFIDENCE and rule_confidence > confidence:
                return rule_based_type, rule_confidence

            return predicted_type, confidence
            
        except Exception as e:
            print(f"ML classification error: {e}")
            return rule_based_type, rule_confidence
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for classification"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove excess whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Keep only relevant characters
        text = re.sub(r'[^\w\sáéíóúñü]', ' ', text)
        
        return text.strip()
    
    def _rule_based_classification(self, text: str) -> Tuple[str, float]:
        """Rule-based classification using keywords"""
        text_lower = text.lower()
        
        # Define keywords for each type
        keywords = {
            'Factura': [
                'factura', 'invoice', 'tipo a', 'tipo b', 'tipo c',
                'iva', 'inscripto', 'responsable inscripto', 'consumidor final',
                'punto de venta', 'comprobante', 'cae', 'afip'
            ],
            'Nota de Debito': [
                'nota de debito', 'nota debito', 'débito', 'debito',
                'cargo', 'ajuste debito', 'incremento'
            ],
            'Nota de Credito': [
                'nota de credito', 'nota credito', 'crédito', 'credito',
                'devolucion', 'devolución', 'anulacion', 'anulación',
                'bonificacion', 'bonificación', 'descuento'
            ],
            'Remito': [
                'remito', 'entrega', 'mercaderia', 'mercadería',
                'bultos', 'destinatario', 'transporte', 'envio', 'envío'
            ]
        }
        
        # Score each type
        scores = {}
        for doc_type, words in keywords.items():
            score = sum(1 for word in words if word in text_lower)
            scores[doc_type] = score
        
        # Get best match
        if scores:
            max_score = max(scores.values())
            if max_score > 0:
                best_type = max(scores, key=scores.get)
                # Calculate confidence based on keyword matches
                total_keywords = len(keywords[best_type])
                confidence = min(0.9, max_score / total_keywords)
                return best_type, confidence
        
        return "Desconocido", 0.0
    
    def retrain(self, documents_data):
        """Retrain model with validated documents"""
        if len(documents_data) < 10:
            print("Not enough training data for retraining")
            return False
        
        texts = [doc['text'] for doc in documents_data]
        labels = [doc['type'] for doc in documents_data]
        
        # Check class distribution
        from collections import Counter
        label_counts = Counter(labels)
        print(f"Class distribution: {dict(label_counts)}")
        
        # Check if each class has at least 2 examples (required for stratified split)
        min_samples_per_class = min(label_counts.values())
        if min_samples_per_class < 2:
            print(f"Error: Some classes have less than 2 examples. Cannot perform stratified split.")
            print(f"Classes with insufficient data: {[label for label, count in label_counts.items() if count < 2]}")
            return False
        
        # Update label encoder
        unique_labels = list(set(labels))
        self.label_encoder = {label: idx for idx, label in enumerate(unique_labels)}
        self.reverse_label_encoder = {idx: label for label, idx in self.label_encoder.items()}
        
        # Vectorize
        X = self.vectorizer.fit_transform(texts)
        y = np.array([self.label_encoder[label] for label in labels])
        
        # Only use train_test_split if we have enough data for meaningful evaluation
        # For small datasets, train on all data
        if len(documents_data) >= 20:
            try:
                # Split data with stratification
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42, stratify=y
                )
                
                # Train
                self.model.fit(X_train, y_train)
                
                # Evaluate
                y_pred = self.model.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                
                print(f"Model retrained with {len(documents_data)} documents")
                print(f"Test accuracy: {accuracy:.2%}")
                
            except ValueError as e:
                # Fallback: train on all data if stratification fails
                print(f"Stratification failed: {e}. Training on all data.")
                self.model.fit(X, y)
                print(f"Model retrained with {len(documents_data)} documents (no test split)")
        else:
            # For small datasets, train on all data
            self.model.fit(X, y)
            print(f"Model retrained with {len(documents_data)} documents (too few for test split)")
        
        return True
    
    def save_model(self):
        """Save model and vectorizer to disk"""
        try:
            joblib.dump(self.model, Config.MODEL_PATH)
            joblib.dump(self.vectorizer, Config.VECTORIZER_PATH)
            
            # Save label encoders
            label_encoder_path = Config.MODEL_PATH.replace('.pkl', '_labels.pkl')
            joblib.dump({
                'label_encoder': self.label_encoder,
                'reverse_label_encoder': self.reverse_label_encoder
            }, label_encoder_path)
            
            print(f"Model saved to {Config.MODEL_PATH}")
            return True
        except Exception as e:
            print(f"Error saving model: {e}")
            return False
    
    def load_model(self):
        """Load model and vectorizer from disk"""
        try:
            self.model = joblib.load(Config.MODEL_PATH)
            self.vectorizer = joblib.load(Config.VECTORIZER_PATH)
            
            # Load label encoders
            label_encoder_path = Config.MODEL_PATH.replace('.pkl', '_labels.pkl')
            if os.path.exists(label_encoder_path):
                encoders = joblib.load(label_encoder_path)
                self.label_encoder = encoders['label_encoder']
                self.reverse_label_encoder = encoders['reverse_label_encoder']
            
            print("Model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
