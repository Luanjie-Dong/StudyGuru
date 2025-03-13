# StudyGuru

## StudyGuru Model 

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
