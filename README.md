# StudyGuru

## StudyGuru Model 

This repository contains the core components of the **StudyGuru** model, designed to streamline document ingestion, retrieval, topic extraction, and question generation for educational purposes. Below is a detailed breakdown of the files and their functionalities.

---

### File Structure

#### 1. `rag.py`
- **Purpose**: Implements the Retrieval-Augmented Generation (RAG) pipeline for **StudyGuru**.
- **Functionality**:
  - Handles document ingestion from various formats.
  - Performs retrieval of relevant information based on user queries.
  - Extracts key topics and concepts from ingested documents.
- **Usage**: This module serves as the backbone for processing and understanding unstructured data in the form of documents.

---

#### 2. `StudyGuru.py`
- **Purpose**: Contains the **Question Generation (QG)** and **Review** functionalities of StudyGuru.
- **Functionality**:
  - **QG Module**: Automatically generates questions from processed documents or extracted topics to aid in learning and assessment.
  - **Review Module**: Provides feedback and insights on the ingested content, helping users identify areas for improvement.
- **Usage**: Ideal for generating quizzes, study guides, and personalized feedback based on the content.

---

#### 3. `endpoints.py`
- **Purpose**: Manages API endpoints for database interactions.
- **Functionality**:
  - Connects to the database to extract relevant challenge notes or module-specific content.
  - Processes the retrieved data for further use in the RAG pipeline or other modules.
- **Usage**: Acts as the bridge between the backend database and the model's processing modules.

---

#### 4. `extractor.py`
- **Purpose**: Provides helper functions for multimodal document processing.
- **Functionality**:
  - Supports multiple input formats such as PDF, PPTX, and PNG.
  - Extracts text, images, and metadata from documents using specialized libraries.
  - Prepares the extracted content for downstream tasks like topic extraction and question generation.
- **Usage**: Essential for handling diverse input types and ensuring compatibility with the RAG pipeline.

---

#### 5. `Dockerfile.model`
- **Purpose**: Defines the Docker image for building and deploying the **StudyGuru** model.
- **Functionality**:
  - Specifies the environment setup, including dependencies and configurations.
  - Ensures reproducibility and portability of the model across different platforms.
- **Usage**: Use this file to containerize the application for deployment in production environments.

---

#### 6. `requirements.txt`
- **Purpose**: Lists all the required Python libraries and dependencies.
- **Functionality**:
  - Includes libraries for NLP (e.g., transformers, spacy), document processing (e.g., PyPDF2, python-pptx), and other utilities.
  - Ensures consistent installation of dependencies across development and production environments.
- **Usage**: Run `pip install -r requirements.txt` to install all necessary packages.

---
