# CSE 535 : Information_Retrieval
This repository is made for CSE 535 Information Retrieval project.
### Multi-topic Information Retrieval Chatbot
We present our Multi-Topic Information Retrieval chatbot that caters to requests about information available on various subreddits on Reddit. The chatbot is designed to respond to general user queries on the whole knowledge base and focused queries that are directed to a restricted scope in the knowledge base. Restricting the scope of search serves two purposes; First, It can lead to more relevant information retrieved for the user since user’s intent is inherently captured when a particular topic is chosen. Second, it serves as an evaluation measure of the chatbot by allowing to capture the global statistics on the efficiency of the model. It creates the foundation for analytics. Healthcare, Environment, Education, Politics and Technology are the topics that are made available for the user to choose from while interacting with the chatbot. Inferring context and tracking is a major challenge and is a necessary component for building a robust chatbot. Our chatbot includes reasonable heuristics to detect context, track and flush context through the chain of conversation. The chatbot is made available as a web application hosted on the cloud.

## Usage
Within a virtual env, nstall the requirements from req.txt using <br>
`pip install -r req.txt` <br>

Run the app using <br>
`uvicorn run:app` <br>
