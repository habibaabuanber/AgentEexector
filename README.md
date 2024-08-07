# Lead With AI: AI-Powered Chatbot for Software Development

Lead With AI is an innovative AI-powered chatbot designed to enhance and expedite the software development process. Utilizing advanced AI frameworks and technologies such as Python, Langchain, Streamlit, Pinecone Vector Database, and Upstash, DevBot aids in automating several stages of the software development lifecycle. This includes uploading BRD (Business Requirements Document) files, generating user stories, creating a structured file tree based on these stories, and generating starter code for each file in the tree.

## Features

- **BRD Page Uploader**: Allows users to upload BRD files directly into the system.
- **User Story Generation**: Automatically generates user stories from the uploaded BRD files.
- **File Tree Structure Creation**: Organizes the generated user stories into a logical file tree structure.
- **Code Generation**: Automatically generates boilerplate code for each file in the tree.

## Getting Started

### Prerequisites

Before setting up DevBot, ensure you have the following installed:
- Python (version 3.8 or higher)
- Pip (Python package installer)
- Git (for cloning the repository)
- Langchain: For handling AI and natural language processing functionalities.
- Streamlit: For deploying and managing the web interface of the chatbot.

### Installation

1. **Clone the Repository**

   Start by cloning the DevBot repository to your local machine by running:

   ```bash
   git clone https://github.com/opex-sa/LeadWithAi.git
   cd Lead With AI
   ```

2. **Install Required Packages**

   Install all the required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```

3. **Setup External Services**

   - **Pinecone Setup**: Create an account at [Pinecone](https://www.pinecone.io/) and set up a new vector database. Note the API key and the environment ID.
   - **Upstash Setup**: Register at [Upstash](https://upstash.com/) for managing message memory and follow the instructions to configure Redis.

4. **Environment Variables**

   Set up the required environment variables. Create a `.env` file in the root directory of the project and update it with the necessary credentials:

   ```plaintext
   PINECONE_API_KEY='2784afd9-3bd4-4047-bc20-6c5941263c7b'
   UPSTASH_REDIS_URL='z_1dWlkIjoiNGVjOGUwNTctZGI0Mi00ZGM5LTlkNjktZGIwMzQzYjI5YzdhIn0.2JlvUT-kCWIDBgTJPDPJb-DV8g0AB-HLi8c3W0GY0pBCZQkaHr3BB00j8DNq73OkCRmlqhWDIchBvjwXqgGRKQ'
   OPENAI_API_KEY ='sk-proj-WLRRciVfHnmCyu0YGOdYT3BlbkFJXzCtlD8Gk5x4yGmjiqwo'
   TAVILY_API_KEY= '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'
   ```

5. **Run the Application**

   Use Streamlit to run the web application:

   ```bash
   streamlit run app.py
   ```

   Navigate to `http://localhost:8501` in your web browser to see the application running.

### Usage

1. **Upload BRD File**: On the homepage, click on the "Upload BRD File" section to upload your document.
2. **Generate User Stories**: Once the BRD is uploaded, click on "Generate User Stories" to process the contents of the BRD.
3. **View File Tree Structure**: After user stories are generated, view the suggested file tree structure.
4. **Generate Code**: Select the required nodes in the file tree to generate and view the starter code.



## License

This project only licensed for internal developers
