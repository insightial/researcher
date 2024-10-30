from langgraph.graph import END, START, StateGraph

from researcher.checkpoint import BaseCheckpointManager
from researcher.llm import LLMProvider
from researcher.retriever import TavilyRetriever
from researcher.state import GraphState
from researcher.store.vectorstore import Store


class Researcher:
    def __init__(self, vector_store: Store, **kwargs):
        """
        Initialize the synchronous Researcher class.
        """
        checkpoint_manager = BaseCheckpointManager()

        # Initialize the StateGraph for processing
        self.graph = StateGraph(GraphState)
        self.checkpointer = checkpoint_manager
        # Initialize the LLM
        self.llm = LLMProvider.create_provider(
            "openai", model="gpt-3.5-turbo", **kwargs
        )

        # Configure and initialize the Tavily Retriever
        default_tavily_params = {
            "max_results": 2,
            "search_depth": "advanced",
            "include_images": False,
            "include_answer": False,
        }
        tavily_params = {**default_tavily_params, **kwargs}
        self.retriever = TavilyRetriever(**tavily_params)

        # Set maximum iterations from kwargs, defaulting to 3 if not provided
        self.max_iterations = kwargs.get("max_iterations", 3)
        self.iterations = 0

        self.store = vector_store

        # Add nodes and edges to the graph
        self.add_graph_nodes_and_edges()

    @classmethod
    async def create_researcher(cls, vector_store: Store, **kwargs):
        """
        Create a researcher with the specified checkpointer manager and settings.
        """
        self = cls(vector_store)
        checkpoint_manager = kwargs.pop("checkpoint_manager", None)
        if checkpoint_manager is None:
            checkpoint_manager = BaseCheckpointManager()

        # Initialize the StateGraph for processing
        self.graph = StateGraph(GraphState)
        self.checkpointer = checkpoint_manager
        # Initialize the LLM
        self.llm = LLMProvider.create_provider("openai", model="gpt-3.5-turbo")

        # Configure and initialize the Tavily Retriever
        default_tavily_params = {
            "max_results": 2,
            "search_depth": "advanced",
            "include_images": False,
            "include_answer": False,
        }
        tavily_params = {**default_tavily_params, **kwargs}
        self.retriever = TavilyRetriever(**tavily_params)

        # Set maximum iterations from kwargs, defaulting to 4 if not provided
        self.max_iterations = kwargs.get("max_iterations", 4)
        self.iterations = 1

        # Add nodes and edges to the graph
        self.add_graph_nodes_and_edges()

        return self

    def get_graph(self):
        return self.graph

    def add_graph_nodes_and_edges(self):
        """
        Define the states and conditional transitions in the StateGraph.
        """
        # Define nodes
        self.graph.add_node("generate_query", self.generate_query)
        self.graph.add_node("query_tavily", self.query_tavily)
        self.graph.add_node("query_vector_store", self.query_vector_store)
        self.graph.add_node("generate_response", self.generate_response)
        self.graph.add_node("generate_new_query", self.generate_new_query)
        self.graph.add_node("final_response", self.final_response)

        # Define transitions
        self.graph.add_conditional_edges(
            START,
            self.check_iteration_limit,
            {
                "within_limit": "generate_query",
                "limit_reached": "final_response",
            },
        )

        # After generate_query, go to both query_tavily and query_vector_store
        self.graph.add_edge("generate_query", "query_tavily")
        self.graph.add_edge("generate_query", "query_vector_store")

        # After both queries, merge results
        self.graph.add_edge("query_tavily", "generate_response")
        self.graph.add_edge("query_vector_store", "generate_response")

        self.graph.add_conditional_edges(
            "generate_response",
            self.validate_response,
            {
                "validation_passes": "final_response",
                "validation_fails": "generate_new_query",
            },
        )
        self.graph.add_edge("generate_new_query", "query_tavily")
        self.graph.add_edge("generate_new_query", "query_vector_store")
        self.graph.add_edge("final_response", END)

    async def generate_query(self, state: GraphState):
        """
        Generate an initial search query using the user's question and chat history.
        """
        question = state["question"]
        chat_history = "\n".join(state["chat_history"])
        prompt = f"Conversation History:\n{chat_history}\n\nCurrent Question: {question}\nGenerate an optimized search query."

        # Generate a refined query based on history and question
        generated_query = await self.llm.agenerate([prompt])
        return {"question": generated_query.strip()}

    async def query_tavily(self, state: GraphState):
        """
        Query Tavily using the generated or refined query.
        """
        question = state["question"]
        search_results = await self.retriever.search(question)
        return {"search_results": search_results}

    def query_vector_store(self, state: GraphState):
        """
        Query the vector store using the generated or refined query.
        """
        vector_store_results = []
        if state["files"] and len(state["files"]) > 0:
            question = state["question"]
            vector_store_results = self.store.similarity_search(
                question,
                k=self.iterations * 5,
                filter={"source": {"in": state["files"]}},
            )
        return {"vector_store_results": vector_store_results}

    async def generate_response(self, state: GraphState):
        """
        Generate a response based on Tavily search results, vector store results, the question, and the chat history.
        """
        search_results = state["search_results"]
        vector_store_results = (
            state["vector_store_results"] if "vector_store_results" in state else []
        )
        question = state["question"]

        # Include chat history and search results in the prompt
        prompt = (
            f"Web Search Results:\n{search_results}\n\n"
            f"File Search Results:\n{vector_store_results}\n\n"
            f"Question: {question}\nProvide a comprehensive answer."
        )
        response = await self.llm.agenerate([prompt])
        return {"response": response.strip()}

    async def validate_response(self, state: GraphState):
        """
        Validate if the generated response is satisfactory.
        """
        response = state["response"]
        question = state["question"]
        prompt = f"Response: {response}\n\nQuestion: {question}\nIs this response accurate? Answer 'yes' or 'no'."
        validation = await self.llm.agenerate([prompt])
        return (
            "validation_passes"
            if validation.strip().lower() == "yes"
            else "validation_fails"
        )

    async def generate_new_query(self, state: GraphState):
        """
        Generate a refined query if the response validation fails.
        """
        question = state["question"]
        response = state["response"]
        prompt = (
            f"Original Query: {question}\nResponse: {response}\n"
            f"The response did not meet expectations. Suggest a new query for more accurate results."
        )
        new_query = await self.llm.agenerate([prompt])
        return {"question": new_query.strip()}

    async def check_iteration_limit(self, _: GraphState):
        """
        Check if the iteration limit is reached.
        """
        self.iterations += 1
        return (
            "within_limit" if self.iterations < self.max_iterations else "limit_reached"
        )

    async def final_response(self, state: GraphState):
        """
        Return the final validated response.
        """
        return {"response": state["response"]}
