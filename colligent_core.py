import os
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
import logging

# Import handling for both local and cloud deployment
import sys
import os

# Add current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from colligent_config import Config
    from colligent_document_processor import DocumentProcessor
    from colligent_vector_db import VectorStore
except ImportError as e:
    logger.error(f"Import Error: {e}")
    raise

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContextAwareChatbot:
    """Main chatbot class that handles document-based question answering"""
    
    def __init__(self, config: Config):
        self.config = config
        self.llm = None
        self.document_processor = DocumentProcessor(config)
        self.vector_store = VectorStore(config)
        self.conversation_history = []
        self.current_mode = "default"  # Default mode
        
        # Initialize LLM if API key is available
        if config.OPENAI_API_KEY:
            self.llm = ChatOpenAI(
                model_name=config.OPENAI_MODEL,
                temperature=config.TEMPERATURE,
                max_tokens=config.MAX_TOKENS,
                openai_api_key=config.OPENAI_API_KEY
            )
        else:
            logger.warning("OpenAI API key not found. Chatbot will use fallback responses.")
    
    def initialize_knowledge_base(self, force_rebuild: bool = False) -> bool:
        """Initialize the knowledge base from documents"""
        try:
            logger.info("Starting knowledge base initialization...")
            logger.info(f"Force rebuild: {force_rebuild}")
            
            # Try to load existing vector store
            if not force_rebuild:
                logger.info("Attempting to load existing vector store...")
                existing_store = self.vector_store.load_vector_store()
                if existing_store:
                    logger.info("Using existing knowledge base")
                    return True
                else:
                    logger.info("No existing vector store found, will create new one")
            
            # Process documents and create new vector store
            logger.info("Processing documents and creating knowledge base...")
            documents = self.document_processor.process_documents()
            
            logger.info(f"Document processing result: {len(documents)} documents")
            if documents:
                logger.info(f"First document sample: {documents[0] if documents else 'None'}")
            
            if not documents:
                logger.error("No documents found to process")
                logger.error("This means the data folder is empty or not accessible")
                return False
            
            # Create vector store
            logger.info("Creating vector store...")
            vector_store = self.vector_store.create_vector_store(documents)
            if vector_store:
                logger.info("Knowledge base initialized successfully")
                return True
            else:
                logger.error("Failed to create vector store")
                return False
                
        except Exception as e:
            logger.error(f"Error initializing knowledge base: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    def get_relevant_context(self, query: str, k: int = 5) -> str:
        """Get relevant context from documents based on query"""
        try:
            # Search for similar documents
            similar_docs = self.vector_store.search_similar(query, k=k)
            
            if not similar_docs:
                return "No relevant information found in the documents."
            
            # Combine relevant context
            context_parts = []
            for i, doc in enumerate(similar_docs, 1):
                source = doc.metadata.get('source', 'Unknown')
                content = doc.page_content.strip()
                context_parts.append(f"Source {i} ({source}):\n{content}\n")
            
            return "\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"Error getting relevant context: {str(e)}")
            return "Error retrieving relevant information."
    
    def create_prompt(self, query: str, context: str) -> str:
        """Create a prompt for the LLM with context and query"""
        prompt_template = f"""
{self.config.SYSTEM_PROMPT}

Context from documents:
{context}

User Question: {query}

Please answer the question based on the provided context. If the context doesn't contain enough information to answer the question, respond with: "I do not have available information yet."

Answer:"""
        return prompt_template
    
    def get_llm_response(self, query: str, context: str) -> str:
        """Get response from LLM"""
        # Check if context is insufficient first
        if not context or context == "No relevant information found in the documents." or context == "Error retrieving relevant information.":
            return "I do not have available information yet."
        
        if not self.llm:
            return self.get_fallback_response(query, context)
        
        try:
            prompt = self.create_prompt(query, context)
            messages = [
                SystemMessage(content=self.config.SYSTEM_PROMPT),
                HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}")
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"Error getting LLM response: {str(e)}")
            return self.get_fallback_response(query, context)
    
    def get_fallback_response(self, query: str, context: str) -> str:
        """Fallback response when LLM is not available"""
        if not context or context == "No relevant information found in the documents.":
            return "I do not have available information yet."
        
        # Extract key information from context
        query_lower = query.lower()
        context_lower = context.lower()
        
        # Define question patterns and their response strategies
        response_patterns = {
            'engineer': self._extract_engineering_info,
            'technical': self._extract_technical_skills,
            'skills': self._extract_technical_skills,
            'project': self._extract_projects,
            'experience': self._extract_projects,
            'proud': self._extract_projects,
            'culture': self._extract_culture_values,
            'team': self._extract_culture_values,
            'value': self._extract_culture_values,
            'learning': self._extract_learning_approach,
            'debug': self._extract_learning_approach,
            'research': self._extract_research_info,
            'astrophysics': self._extract_research_info,
            'data scientist': self._extract_research_info,
            'background': self._extract_background_info,
            'education': self._extract_background_info,
            # Self-reflective patterns
            'energize': self._extract_energy_preferences,
            'drain': self._extract_energy_preferences,
            'collaborate': self._extract_collaboration_style,
            'collaboration': self._extract_collaboration_style,
            'teamwork': self._extract_collaboration_style,
            'grow': self._extract_growth_areas,
            'growth': self._extract_growth_areas,
            'improve': self._extract_growth_areas,
            'develop': self._extract_growth_areas,
            'reflection': self._extract_self_reflection,
            'self': self._extract_self_reflection,
            'personal': self._extract_self_reflection
        }
        
        # Find the best matching pattern
        for keyword, response_func in response_patterns.items():
            if keyword in query_lower:
                response = response_func(context)
                if response:
                    return response
        
        # If no specific pattern matches, provide a general response
        general_response = self._extract_general_info(context, query)
        if general_response == "I do not have available information yet.":
            return general_response
        
        # If we have some general info but it's not specific to the query, 
        # check if the context actually contains relevant information
        if not self._context_contains_relevant_info(context, query):
            return "I do not have available information yet."
        
        return general_response
    
    def _context_contains_relevant_info(self, context: str, query: str) -> bool:
        """Check if the context contains information relevant to the query"""
        if not context or context == "No relevant information found in the documents.":
            return False
        
        # Convert to lowercase for comparison
        context_lower = context.lower()
        query_lower = query.lower()
        
        # Extract key words from the query
        query_words = query_lower.split()
        
        # Check if any query words appear in the context
        for word in query_words:
            if len(word) > 3 and word in context_lower:  # Only check words longer than 3 characters
                return True
        
        # Check for common question patterns
        question_patterns = [
            'what', 'how', 'when', 'where', 'why', 'who', 'which',
            'experience', 'skills', 'background', 'education', 'work',
            'project', 'research', 'study', 'degree', 'university'
        ]
        
        for pattern in question_patterns:
            if pattern in query_lower and pattern in context_lower:
                return True
        
        return False
    
    def _extract_engineering_info(self, context: str) -> str:
        """Extract engineering background information"""
        if 'data scientist' in context.lower() or 'astrophysics' in context.lower():
            return "I'm a Data Scientist and Astrophysics Researcher. I work at the intersection of machine learning and cosmology, specializing in predicting universe seeing conditions, emulating cosmic structures with AI, and solving theoretical puzzles in astrophysics."
        return None
    
    def _extract_technical_skills(self, context: str) -> str:
        """Extract technical skills information"""
        skills = []
        context_lower = context.lower()
        
        # Look for technical skills in the context
        if 'machine learning' in context_lower:
            skills.append("Machine Learning")
        if 'python' in context_lower:
            skills.append("Python")
        if 'data science' in context_lower:
            skills.append("Data Science")
        if 'astrophysics' in context_lower:
            skills.append("Astrophysics")
        if 'cosmology' in context_lower:
            skills.append("Cosmology")
        if 'diffusion' in context_lower:
            skills.append("Diffusion Models")
        if '21cm' in context_lower:
            skills.append("21cm Cosmology")
        if 'neutral hydrogen' in context_lower:
            skills.append("Neutral Hydrogen Analysis")
        
        if skills:
            return f"My strongest technical skills include: {', '.join(skills)}. I specialize in applying machine learning to astrophysical problems, particularly in cosmology and neutral hydrogen analysis."
        return None
    
    def _extract_projects(self, context: str) -> str:
        """Extract project and experience information"""
        projects = []
        context_lower = context.lower()
        
        if 'diffusion models' in context_lower:
            projects.append("Research on Diffusion Models for Emulating Neutral Hydrogen Maps")
        if '21cm cosmology' in context_lower:
            projects.append("21cm Cosmology research")
        if 'neutral hydrogen' in context_lower:
            projects.append("Neutral Hydrogen analysis and mapping")
        if 'cosmic structures' in context_lower:
            projects.append("AI emulation of cosmic structures")
        if 'universe seeing conditions' in context_lower:
            projects.append("Predicting universe seeing conditions")
        
        if projects:
            return f"I'm most proud of my work in: {', '.join(projects)}. My research focuses on innovative approaches to understanding cosmic evolution through machine learning and astrophysics."
        return None
    
    def _extract_culture_values(self, context: str) -> str:
        """Extract culture and team values"""
        if 'hard-working team player' in context.lower() or 'collabora' in context.lower():
            return "I value being a hard-working team player who thrives in collaboration. I'm driven by curiosity and powered by machine learning, pushing boundaries with ambition and precision."
        return None
    
    def _extract_learning_approach(self, context: str) -> str:
        """Extract learning and debugging approach"""
        if 'curiosity' in context.lower() or 'theoretical puzzles' in context.lower():
            return "My approach to learning involves curiosity-driven exploration and solving theoretical puzzles. I push boundaries with ambition and precision, whether it's predicting universe conditions or emulating cosmic structures with AI."
        return None
    
    def _extract_research_info(self, context: str) -> str:
        """Extract research information"""
        if 'diffusion models' in context.lower() and 'neutral hydrogen' in context.lower():
            return "My research focuses on Diffusion Models for Emulating Neutral Hydrogen Maps, representing a novel approach to 21cm cosmology. I work on detecting and analyzing neutral hydrogen through its characteristic 21cm emission line to understand cosmic evolution."
        return None
    
    def _extract_background_info(self, context: str) -> str:
        """Extract background and education information"""
        if 'data scientist' in context.lower() and 'astrophysics' in context.lower():
            return "I'm Collins Maripane, a Data Scientist and Astrophysics Researcher. I'm an aspiring data scientist, astrophysicist, and creative innovator driven by curiosity and powered by machine learning."
        return None
    
    def _extract_general_info(self, context: str, query: str) -> str:
        """Extract general information when no specific pattern matches"""
        # Look for key phrases in the context
        key_phrases = []
        context_lower = context.lower()
        
        if 'collins maripane' in context_lower:
            key_phrases.append("Collins Maripane")
        if 'data scientist' in context_lower:
            key_phrases.append("Data Scientist")
        if 'astrophysics' in context_lower:
            key_phrases.append("Astrophysics Researcher")
        if 'machine learning' in context_lower:
            key_phrases.append("Machine Learning specialist")
        
        if key_phrases:
            return f"I can tell you about {', '.join(key_phrases)}. I work at the intersection of data science and astrophysics, applying machine learning to solve complex cosmological problems."
        
        # If no relevant information is found in the context, return the standard response
        return "I do not have available information yet."
    
    def ask_question(self, query: str, include_context: bool = False) -> Dict[str, Any]:
        """Main method to ask a question and get a response"""
        try:
            # Get relevant context
            context = self.get_relevant_context(query)
            
            # Get LLM response
            response = self.get_llm_response(query, context)
            
            # Apply Power Agent mode transformation
            transformed_response = self.apply_mode_transformation(response)
            
            # Store in conversation history
            self.conversation_history.append({
                "query": query,
                "context": context if include_context else None,
                "response": transformed_response,
                "timestamp": None  # Could add datetime here
            })
            
            result = {
                "query": query,
                "response": transformed_response,
                "sources": self._extract_sources(context)
            }
            
            if include_context:
                result["context"] = context
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing question: {str(e)}")
            return {
                "query": query,
                "response": "I do not have available information yet.",
                "error": str(e)
            }
    
    def _extract_sources(self, context: str) -> List[str]:
        """Extract source documents from context"""
        sources = []
        lines = context.split('\n')
        for line in lines:
            if line.startswith('Source') and '(' in line and ')' in line:
                source = line.split('(')[1].split(')')[0]
                if source not in sources:
                    sources.append(source)
        return sources
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history"""
        return self.conversation_history
    
    def clear_conversation_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_knowledge_base_info(self) -> Dict[str, Any]:
        """Get information about the knowledge base"""
        try:
            logger.info("Getting knowledge base info...")
            info = self.vector_store.get_collection_info()
            logger.info(f"Knowledge base info: {info}")
            return info
        except Exception as e:
            logger.error(f"Error getting knowledge base info: {e}")
            return {"error": str(e)}
    
    # Self-Reflective Agent Methods
    
    def _extract_energy_preferences(self, context: str) -> str:
        """Extract information about what energizes or drains Collins"""
        context_lower = context.lower()
        
        energizing_activities = []
        draining_activities = []
        
        # Look for energizing activities
        if 'curiosity' in context_lower or 'theoretical puzzles' in context_lower:
            energizing_activities.append("solving complex theoretical puzzles")
        if 'machine learning' in context_lower and 'cosmology' in context_lower:
            energizing_activities.append("applying machine learning to cosmological problems")
        if 'research' in context_lower and 'innovation' in context_lower:
            energizing_activities.append("innovative research projects")
        if 'collaboration' in context_lower and 'team' in context_lower:
            energizing_activities.append("collaborative team environments")
        if 'diffusion models' in context_lower or '21cm cosmology' in context_lower:
            energizing_activities.append("working on cutting-edge astrophysics research")
        
        # Look for potentially draining activities
        if 'hard-working' in context_lower:
            draining_activities.append("repetitive tasks without intellectual challenge")
        if 'precision' in context_lower and 'ambition' in context_lower:
            draining_activities.append("work that doesn't push boundaries")
        
        response = "Based on my background and work patterns, "
        
        if energizing_activities:
            response += f"I find myself most energized by {', '.join(energizing_activities)}. "
        
        if draining_activities:
            response += f"I tend to feel drained by {', '.join(draining_activities)}. "
        
        response += "I thrive when I can combine my curiosity with technical challenges and collaborative problem-solving."
        
        return response
    
    def _extract_collaboration_style(self, context: str) -> str:
        """Extract information about Collins' collaboration preferences"""
        context_lower = context.lower()
        
        collaboration_traits = []
        
        if 'hard-working team player' in context_lower:
            collaboration_traits.append("I'm a dedicated team player who puts in the effort")
        if 'collaboration' in context_lower:
            collaboration_traits.append("I thrive in collaborative environments")
        if 'curiosity' in context_lower:
            collaboration_traits.append("I bring curiosity and intellectual engagement to team projects")
        if 'machine learning' in context_lower and 'astrophysics' in context_lower:
            collaboration_traits.append("I excel at bridging technical and scientific domains")
        if 'precision' in context_lower and 'ambition' in context_lower:
            collaboration_traits.append("I balance precision with ambitious goals in team settings")
        
        if collaboration_traits:
            response = f"I collaborate best when {', '.join(collaboration_traits)}. "
            response += "I value environments where I can contribute my technical expertise while learning from others' perspectives. "
            response += "I work well in teams that appreciate both analytical rigor and creative problem-solving."
        else:
            response = "I collaborate best in environments that value technical expertise, curiosity, and innovative thinking. I work well with teams that appreciate both precision and ambition in problem-solving."
        
        return response
    
    def _extract_growth_areas(self, context: str) -> str:
        """Extract information about areas where Collins needs to grow"""
        context_lower = context.lower()
        
        growth_areas = []
        strengths = []
        
        # Identify potential growth areas based on background
        if 'data scientist' in context_lower and 'astrophysics' in context_lower:
            growth_areas.append("expanding my knowledge beyond astrophysics into other domains")
        if 'research' in context_lower and 'diffusion models' in context_lower:
            growth_areas.append("staying current with rapidly evolving AI/ML technologies")
        if 'theoretical' in context_lower:
            growth_areas.append("developing more practical implementation skills")
        if 'cosmology' in context_lower:
            growth_areas.append("building broader industry experience")
        
        # Identify current strengths
        if 'machine learning' in context_lower:
            strengths.append("strong technical foundation in ML")
        if 'curiosity' in context_lower:
            strengths.append("intellectual curiosity and drive")
        if 'precision' in context_lower:
            strengths.append("attention to detail and precision")
        
        response = "Areas where I need to grow include "
        
        if growth_areas:
            response += f"{', '.join(growth_areas)}. "
        else:
            response += "expanding my practical experience and staying current with emerging technologies. "
        
        if strengths:
            response += f"My strengths in {', '.join(strengths)} provide a solid foundation for this growth. "
        
        response += "I'm committed to continuous learning and development in both technical and professional areas."
        
        return response
    
    def _extract_self_reflection(self, context: str) -> str:
        """Extract general self-reflection insights"""
        context_lower = context.lower()
        
        insights = []
        
        if 'curiosity' in context_lower and 'machine learning' in context_lower:
            insights.append("I'm driven by intellectual curiosity and technical innovation")
        if 'hard-working' in context_lower and 'team player' in context_lower:
            insights.append("I value dedication and collaboration in my work")
        if 'precision' in context_lower and 'ambition' in context_lower:
            insights.append("I balance attention to detail with ambitious goals")
        if 'astrophysics' in context_lower and 'data science' in context_lower:
            insights.append("I thrive at the intersection of multiple disciplines")
        
        if insights:
            response = f"Through self-reflection, I recognize that {', '.join(insights)}. "
            response += "I'm constantly learning about my work preferences, collaboration style, and areas for growth. "
            response += "This self-awareness helps me make better decisions about projects, teams, and career development."
        else:
            response = "Self-reflection is an important part of my growth process. I regularly assess my strengths, preferences, and areas for improvement to make informed decisions about my career and personal development."
        
        return response
    
    # Power Agent - Tone/Mode Switcher Methods
    
    def set_mode(self, mode: str) -> str:
        """Set the current response mode"""
        available_modes = {
            "default": "Default conversational mode",
            "interview": "Professional interview mode",
            "storytelling": "Personal storytelling mode", 
            "fast_facts": "Quick bullet-point mode",
            "humble_brag": "Confident self-promotion mode",
            "code_style": "Technical implementation-focused mode"
        }
        
        if mode.lower() in available_modes:
            self.current_mode = mode.lower()
            return f"✅ Mode switched to: {available_modes[mode.lower()]}"
        else:
            return f"❌ Invalid mode. Available modes: {', '.join(available_modes.keys())}"
    
    def get_current_mode(self) -> str:
        """Get the current response mode"""
        return self.current_mode
    
    def get_available_modes(self) -> Dict[str, str]:
        """Get all available modes and their descriptions"""
        return {
            "default": "Default conversational mode",
            "interview": "Professional interview mode - concise, professional, informative",
            "storytelling": "Personal storytelling mode - longer, reflective, narrative",
            "fast_facts": "Fast facts mode - bullet points, TL;DR format",
            "humble_brag": "Humble brag mode - confident self-promotion, still grounded in truth",
            "code_style": "Code style mode - technical implementation details, code examples, and architectural insights"
        }
    
    def apply_mode_transformation(self, response: str) -> str:
        """Apply the current mode transformation to a response"""
        if self.current_mode == "default":
            return response
        
        elif self.current_mode == "interview":
            return self._transform_to_interview_mode(response)
        
        elif self.current_mode == "storytelling":
            return self._transform_to_storytelling_mode(response)
        
        elif self.current_mode == "fast_facts":
            return self._transform_to_fast_facts_mode(response)
        
        elif self.current_mode == "humble_brag":
            return self._transform_to_humble_brag_mode(response)
        
        elif self.current_mode == "code_style":
            return self._transform_to_code_style_mode(response)
        
        return response
    
    def _transform_to_interview_mode(self, response: str) -> str:
        """Transform response to professional interview mode"""
        # Make it concise and professional
        response = response.replace("I'm", "I am")
        response = response.replace("I've", "I have")
        response = response.replace("I'll", "I will")
        
        # Add professional framing
        if "I am" in response and "data scientist" in response.lower():
            response = f"Professionally, {response}"
        
        # Make it more structured
        if len(response) > 200:
            # Split into key points
            sentences = response.split('. ')
            if len(sentences) > 2:
                key_points = sentences[:2]
                response = '. '.join(key_points) + '.'
        
        return response
    
    def _transform_to_storytelling_mode(self, response: str) -> str:
        """Transform response to personal storytelling mode"""
        # Add narrative elements
        if "I am" in response:
            response = response.replace("I am", "Let me tell you about how I became")
        
        # Add reflection
        if "research" in response.lower() or "project" in response.lower():
            response += " Looking back on this journey, I realize how much I've grown through these experiences."
        
        # Add personal connection
        if "curiosity" in response.lower():
            response += " This curiosity has been my driving force, pushing me to explore the unknown and challenge conventional thinking."
        
        return response
    
    def _transform_to_fast_facts_mode(self, response: str) -> str:
        """Transform response to fast facts/bullet point mode"""
        # Extract key information and create bullet points
        facts = []
        
        if "data scientist" in response.lower():
            facts.append("🎯 **Role**: Data Scientist & Astrophysics Researcher")
        
        if "machine learning" in response.lower():
            facts.append("🤖 **Specialty**: Machine Learning applied to cosmology")
        
        if "diffusion models" in response.lower():
            facts.append("🔬 **Research**: Diffusion Models for Neutral Hydrogen Maps")
        
        if "21cm cosmology" in response.lower():
            facts.append("🌌 **Domain**: 21cm Cosmology & Neutral Hydrogen Analysis")
        
        if "curiosity" in response.lower():
            facts.append("💡 **Drive**: Curiosity-driven problem solving")
        
        if "collaboration" in response.lower():
            facts.append("🤝 **Style**: Collaborative team player")
        
        if facts:
            return "**Fast Facts About Collins:**\n\n" + "\n".join(facts)
        else:
            # Fallback to bullet points from original response
            sentences = response.split('. ')
            bullet_points = [f"• {sentence.strip()}" for sentence in sentences if sentence.strip()]
            return "**Quick Summary:**\n\n" + "\n".join(bullet_points)
    
    def _transform_to_humble_brag_mode(self, response: str) -> str:
        """Transform response to confident self-promotion mode"""
        # Add confidence markers
        response = response.replace("I am", "I'm proud to be")
        response = response.replace("I work", "I excel at")
        response = response.replace("I specialize", "I'm recognized for my expertise in")
        
        # Add achievement language
        if "research" in response.lower():
            response = response.replace("research", "groundbreaking research")
        
        if "machine learning" in response.lower():
            response = response.replace("machine learning", "cutting-edge machine learning")
        
        if "cosmology" in response.lower():
            response = response.replace("cosmology", "advanced cosmology")
        
        # Add impact statements
        if "diffusion models" in response.lower():
            response += " This work represents a significant advancement in our understanding of cosmic structures."
        
        if "curiosity" in response.lower():
            response += " This intellectual curiosity has consistently led me to innovative solutions and breakthrough discoveries."
        
        return response
    
    def _transform_to_code_style_mode(self, response: str) -> str:
        """Transform response to technical implementation-focused mode"""
        # Add technical framing
        if "I am" in response:
            response = response.replace("I am", "From a technical implementation perspective, I am")
        
        # Add code-specific language
        if "diffusion models" in response.lower():
            response += " In my implementation, I use a ContextU-Net architecture with residual connections, designed for conditional image generation using diffusion processes. The model is specifically tailored for processing 64x64 pixel astronomical images."
        
        # Add technical details
        if "machine learning" in response.lower():
            response += " My approach involves implementing residual convolutional blocks with batch normalization and ReLU activation, supporting both residual and non-residual modes with dynamic channel adjustment."
        
        # Add architectural insights
        if "research" in response.lower():
            response += " The architecture includes a downsampling path with 4 levels (UnetDown blocks), upsampling path with skip connections (UnetUp blocks), context embedding for conditional generation, and time embedding for diffusion timesteps."
        
        # Add implementation details
        if "cosmology" in response.lower():
            response += " For the training process, I implement noise perturbation using a diffusion schedule with beta values from 1e-4 to 0.02, MSE loss between predicted and true noise, and learning rate decay over 200 epochs with batch size 128."
        
        # Add evaluation approach
        if "analysis" in response.lower():
            response += " My evaluation pipeline includes pixel intensity histograms for comparing real vs generated image distributions, power spectrum analysis for spatial frequency characteristics, and PDF analysis for probability density function comparison."
        
        return response
