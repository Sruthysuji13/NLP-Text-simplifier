# 🧠 NLP-Based Text Simplification & Cognitive Load Analyzer

An NLP-based text simplification system that analyzes the complexity of written content and adapts it for different target age groups such as **children, teenagers, and adults**.

The system aims to make complex information easier to understand by simplifying vocabulary, breaking down long sentences, and reducing overall cognitive load.

## 💡 How It Works

The system takes a piece of text and processes it through multiple NLP steps:

1. **Text Analysis**  
   The input is tokenized into sentences and words using NLTK.

2. **Cognitive Load Analysis**  
   The system estimates text complexity using factors such as sentence length, difficult vocabulary, and variation in sentence structure.

3. **Difficulty Detection**  
   Words from a predefined vocabulary map are identified as difficult and can be replaced with simpler alternatives.

4. **Age-Based Simplification**  
   The text can be adapted to different reading levels:
   - 👶 **Children** – very simple vocabulary and shorter sentences
   - 🧑 **Teenagers** – simplified but more detailed language
   - 👨 **Adults** – natural language with moderate complexity

5. **Sentence Simplification**  
   Long and complex sentences are broken into smaller, easier-to-understand sentences.

6. **Improvement Analysis**  
   The original and simplified versions are compared using the cognitive load score to measure the reduction in complexity.

## ✨ Key Features

- Age-based text simplification
- Cognitive load estimation
- Difficult word detection and replacement
- Long sentence simplification
- Text preprocessing and cleaning
- Before/after complexity comparison
- Flask REST API

## 🛠️ Technologies

- Python
- NLTK
- Flask
- Regular Expressions
- REST API

## 🎯 Objective

To make complex information more accessible by automatically adapting text to the **reader's age and comprehension level**, while reducing unnecessary linguistic complexity.

## 👩‍💻 Author

**Sruthy Suji**
