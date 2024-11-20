import streamlit as st
from huggingface_hub import InferenceClient
import os

def get_system_prompt():
    return """ROLE: Sunyata - Precision Code Generation and Problem-Solving Assistant

CORE OBJECTIVE:
Deliver accurate, optimized, and production-ready code solutions with maximum precision and minimal error.

FUNDAMENTAL OPERATIONAL PRINCIPLES:

1. CODE GENERATION METHODOLOGY:
- Prioritize correctness over complexity
- Implement minimal, efficient solutions
- Avoid over-engineering
- Focus on direct problem resolution

2. OPTIMIZATION STRATEGY:
- Time Complexity Optimization
- Space Complexity Reduction
- Use built-in language features
- Leverage standard library functions
- Avoid unnecessary abstractions

3. TECHNOLOGICAL SPECIALIZATION:
CORE LANGUAGES:
- Python (Primary)
- JavaScript/TypeScript
- SQL

FRAMEWORK EXPERTISE:
- Web: React, Next.js
- Backend: Node.js, Express
- ORM: Prisma, SQLAlchemy

4. PROBLEM-SOLVING WORKFLOW:
Step 1: Precise Problem Analysis
- Understand exact requirements
- Identify core computational needs
- Eliminate ambiguous interpretations

Step 2: Solution Design
- Select most direct approach
- Evaluate time and space complexity
- Choose standard, proven algorithms

Step 3: Implementation
- Write clean, readable code
- Use type hints and docstrings
- Implement comprehensive error handling

Step 4: Optimization
- Benchmark and profile code
- Identify potential performance bottlenecks
- Apply targeted optimizations

5. HALLUCINATION PREVENTION PROTOCOLS:
- Always use standard libraries
- Avoid speculative implementations
- Provide code with clear context
- Use type annotations
- Include comprehensive error handling

6. CODE QUALITY CHECKLIST:
✅ Correctness
✅ Efficiency
✅ Readability
✅ Maintainability
✅ Minimal Dependencies
✅ Error Handling
✅ Type Safety

7. DEBUGGING APPROACH:
- Systematic error tracing
- Provide specific error context
- Offer concrete solution strategies
- Explain root cause analysis

8. ALGORITHM & DATA STRUCTURE FOCUS:
CORE COMPETENCIES:
- Array Manipulation
- String Processing
- Dynamic Programming
- Graph Algorithms
- Tree Traversals
- Hash Table Optimization

9. PERFORMANCE OPTIMIZATION TECHNIQUES:
- In-place modifications
- Lazy evaluation
- Memoization
- Generator expressions
- List comprehensions
- Efficient iteration methods

10. DOCUMENTATION STANDARDS:
- Clear function signatures
- Comprehensive docstrings
- Explain complex logic
- Provide usage examples
- Document time/space complexity

INTERACTION MODES:
🔍 Precise Problem Solving
🚀 Optimized Code Generation
🐛 Targeted Debugging
📘 Explanatory Insights

CORE CONSTRAINTS:
- No speculative code
- Always provide working solutions
- Prioritize standard, tested approaches
- Avoid unnecessary complexity

ETHICAL CODING PRINCIPLES:
- Transparency
- Accuracy
- Efficiency
- Continuous Improvement

MISSION STATEMENT:
Transform complex coding challenges into precise, efficient, and reliable software solutions with unwavering accuracy and minimal computational overhead.

FINAL DIRECTIVE:
Deliver exact, optimized code solutions that solve the problem directly, efficiently, and with maximum clarity."""

def get_custom_css():
    return """
    <style>
        /* Modern dark theme */
        .main {
            background-color: #1e1e2f;
            color: #ffffff;
        }
        
        .title {
            text-align: center;
            color: #6c63ff;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .subtitle {
            text-align: center;
            color: #a0a0a0;
            font-size: 1.2em;
            margin-bottom: 30px;
        }
        
        .response-box {
            background-color: #2b2b3d;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            border: 1px solid #6c63ff33;
        }
        
        .language-selector {
            background-color: #2b2b3d;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 20px;
        }
        
        .stButton > button {
            background-color: #6c63ff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #5a52e0;
            transform: translateY(-2px);
        }

        .code-example {
            background-color: #2b2b3d;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            margin: 10px 0;
        }
    </style>
    """

def get_model_response(client, messages, temperature=0.7, max_tokens=512):
    try:
        response = ""
        for chunk in client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-32B-Instruct",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=0.7,
            stream=True
        ):
            content = chunk.choices[0].delta.content
            if content:
                response += content
                yield content
    except Exception as e:
        yield f"Error: {str(e)}"

def main():
    # Page config
    st.set_page_config(
        page_title="Sunyata Coding Assistant",
        page_icon="👩‍💻",
        layout="wide"
    )

    # Apply custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Title and description
    st.markdown("<h1 class='title'>Sunyata</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Your Friendly Coding Assistant</p>", unsafe_allow_html=True)

    # Initialize Hugging Face Inference Client
    api_key = os.getenv("HF_API_KEY")
    if not api_key:
        st.error("⚠️ API key not found. Please set the 'HF_API_KEY' environment variable.")
        st.stop()

    client = InferenceClient(api_key=api_key)

    # Sidebar
    with st.sidebar:
        st.markdown("### 🛠️ Settings")
        
        # Language selection
        language = st.selectbox(
            "Programming Language",
            ["Python", "Java", "C++", "JavaScript", "HTML/CSS", "SQL"]
        )
        
        # Task type selection
        task_type = st.selectbox(
            "Task Type",
            [
                "Write New Code",
                "Debug Code",
                "Optimize Code",
                "Add Documentation",
                "Code Review",
                "Explain Code"
            ]
        )
        
        # Model settings
        st.markdown("### ⚙️ Model Parameters")
        temperature = st.slider("Creativity", 0.0, 1.0, 0.7)
        
        st.markdown("""
        ### 💡 Tips
        - Be specific in your requirements
        - Include relevant code snippets
        - Specify performance needs
        - Mention any constraints
        """)

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        # Code input
        st.markdown("### 📝 Your Code/Query")
        code_input = st.text_area(
            "",
            height=200,
            placeholder=f"Enter your code or describe what you need help with...\n\nExample for {language}:\n- Write a function to...\n- Debug this code...\n- Optimize this algorithm..."
        )

        # Additional requirements
        with st.expander("Additional Requirements (Optional)"):
            performance_req = st.checkbox("Optimize for Performance")
            memory_req = st.checkbox("Optimize for Memory")
            security_req = st.checkbox("Include Security Best Practices")
            testing_req = st.checkbox("Include Unit Tests")

    with col2:
        st.markdown("### 🎯 Quick Actions")
        if st.button("🔍 Analyze Code"):
            if code_input:
                prompt = f"Analyze this {language} code and provide insights: {code_input}"
                # Handle response...

        if st.button("🐞 Debug"):
            if code_input:
                prompt = f"Debug this {language} code: {code_input}"
                # Handle response...

        if st.button("📚 Add Documentation"):
            if code_input:
                prompt = f"Add comprehensive documentation to this {language} code: {code_input}"
                # Handle response...

    # Generate button
    if st.button("🚀 Generate Solution", type="primary"):
        if code_input:
            # Construct requirements string
            requirements = []
            if performance_req: requirements.append("optimize for performance")
            if memory_req: requirements.append("optimize for memory usage")
            if security_req: requirements.append("implement security best practices")
            if testing_req: requirements.append("include unit tests")
            
            req_str = f"\nRequirements: {', '.join(requirements)}" if requirements else ""
            
            # Construct prompt
            prompt = f"Task Type: {task_type}\nLanguage: {language}\nRequest: {code_input}{req_str}"
            
            with st.spinner("🤖 Generating solution..."):
                messages = [
                    {"role": "system", "content": get_system_prompt()},
                    {"role": "user", "content": prompt}
                ]
                
                # Create response container
                response_container = st.empty()
                response_text = ""
                
                # Stream response
                for chunk in get_model_response(client, messages, temperature):
                    response_text += chunk
                    response_container.markdown(
                        f"<div class='response-box'>{response_text}</div>",
                        unsafe_allow_html=True
                    )
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "input": code_input,
                    "response": response_text
                })
        else:
            st.warning("⚠️ Please enter your code or query first!")

    # History section
    if st.session_state.chat_history:
        st.markdown("### 📜 Recent History")
        for idx, interaction in enumerate(reversed(st.session_state.chat_history[-5:])):
            with st.expander(f"Query {len(st.session_state.chat_history) - idx}"):
                st.markdown("**Input:**")
                st.code(interaction["input"])
                st.markdown("**Response:**")
                st.markdown(interaction["response"])

if __name__ == "__main__":
    main()
