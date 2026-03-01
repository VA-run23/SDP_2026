from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

class HireReadyEngine:
    def __init__(self, company, roundType, vectorStore):
        self.company = company
        self.roundType = roundType
        self.vectorStore = vectorStore
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
        self.history = []
        self.questionCount = 0
        self.maxQuestions = 5

    def get_context(self):
        if not self.vectorStore:
            return "No specific company data found."
            
        # FAISS search
        docs = self.vectorStore.similarity_search(f"{self.company} {self.roundType} interview", k=10)
        
        # Filter metadata manually for precision
        relevantContent = [
            d.page_content for d in docs 
            if d.metadata.get("company") == self.company and d.metadata.get("round") == self.roundType
        ]
        return "\n".join(relevantContent[:2])

    def generate_response(self, userInput=None):
        if self.questionCount >= self.maxQuestions:
            return self.generate_scorecard()

        context = self.get_context()
        
        systemPrompt = f"""
        You are a Senior Interviewer at {self.company} for a {self.roundType} round.
        Use this context for questions and rubrics: {context}

        RULES:
        1. Ask ONE specific question at a time.
        2. Stay in character: Professional, firm, and observant.
        3. Do NOT provide feedback or hints during the interview. 
        4. If the candidate is stuck, move to a related topic.
        5. Current Progress: {self.questionCount}/{self.maxQuestions} questions.
        """

        prompt = ChatPromptTemplate.from_messages([
            ("system", systemPrompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])

        chain = prompt | self.llm
        inputVal = userInput if userInput else "I am ready."
        response = chain.invoke({"input": inputVal, "history": self.history})
        
        self.history.append(HumanMessage(content=inputVal))
        self.history.append(AIMessage(content=response.content))
        self.questionCount += 1
        
        return response.content

    def generate_scorecard(self):
        evalPrompt = f"""
        Interview Complete. Analyze this transcript for {self.company}:
        {self.history}
        
        Provide a scorecard:
        - Communication Skills (1-10)
        - Technical/Role Fit (1-10)
        - Key Strengths
        - Critical Improvements
        - Decision: (Hired/Rejected)
        """
        return self.llm.invoke(evalPrompt).content