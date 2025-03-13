# StudyGURU

StudyGURU is an ***AI-powered educational platform*** designed to democratize access to personalized education. By leveraging Generative AI, we aim to provide high-quality, adaptive learning experiences at a fraction of the cost of traditional tuition, making quality education accessible to students from all socioeconomic backgrounds.

---

## Problem Statement
StudyGURU seeks to address the ***inequitable access to personalized education*** in today's society. While tuition has become a core part of the education system, its high costs make it primarily accessible to affluent households. StudyGURU bridges this gap by offering AI-driven personalized learning that is both scalable and affordable.

## Key Features
### 1. Gamified Learning Roadmap
- Interactive learning paths that incentivize consistent practice
- Progress tracking to build familiarity and mastery over lesson content
- Addictive, short-form challenges to maintain student engagement

### 2. AI Quiz Generation
- Dynamically generated quizzes tailored to individual learning needs
- Built on user-uploaded notes
- Diverse question formats to enhance engagement and comprehension through greater dimension and depth

### 3. AI Review and Feedback
- Immediate, thorough feedback on incorrect answers
- Detailed explanations to help rectify misconceptions
- Encourages self-directed learning through contextual guidance

## System Requirements

## Installation
```
docker compose -up
```

## Future Development
The roadmap for StudyGURU includes expanding question formats through multi-modal generation, providing various flavors of feedback and explanation to suit different learning styles, and providing classroom integration to support out-of-class learning in traditional education instituitions.

<<<<<<< HEAD
=======
1. **`rag.py`**
   - Implements the **Retrieval-Augmented Generation (RAG)** pipeline.
   - Handles **document ingestion**, **indexing**, **retrieval**, and **topic extraction**.
   - Ensures high-quality contextual chunks by organizing content into semantically meaningful segments with **topic headers** for improved readability and relevance.

2. **`StudyGuru.py`**
   - Contains modules for **Question Generation (QG)** and **Review**.
   - Leverages **Gemini** to generate diverse, challenging, and context-aware questions based on the ingested content.
   - Provides tools for self-assessment and performance tracking to enhance learning outcomes.

3. **`endpoints.py`**
   - Manages API interactions with the database.
   - Extracts relevant content such as **challenge notes** and **module-specific data**.
   - Facilitates seamless integration with external systems for real-time updates and synchronization.

4. **`extractor.py`**
   - Offers helper functions for **multimodal document processing**.
   - Supports parsing and extracting text, images, and metadata from **PDFs**, **PPTX files**, and **PNG images**.
   - Ensures compatibility with a wide range of document formats for maximum flexibility, enabling users to work with diverse learning materials.

5. **`Dockerfile.model`**
   - Defines the Docker image for building and deploying the application.
   - Ensures consistent and reproducible environments across **development**, **testing**, and **production stages**, simplifying deployment and scalability.

6. **`requirements.txt`**
   - Lists all Python dependencies required for the project.
   - Includes libraries for **AI model integration**, **document processing**, **API management**, and other essential functionalities, ensuring smooth setup and operation.
>>>>>>> ab8e2a48df3f195ec479f10f4c63f71cc1c3944d
