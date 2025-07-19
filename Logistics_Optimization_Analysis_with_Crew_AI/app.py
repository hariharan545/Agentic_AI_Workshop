import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set page configuration
st.set_page_config(
    page_title="Logistics Optimizer", 
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.375rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e7f3ff;
        border: 1px solid #b3d9ff;
        border-radius: 0.375rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main UI
st.markdown('<h1 class="main-header">🚚 Advanced Logistics Optimizer using CrewAI</h1>', unsafe_allow_html=True)
st.markdown("**Leverage AI agents to analyze logistics operations and generate optimization strategies**")

# Sidebar with information
with st.sidebar:
    st.header("📋 About This App")
    st.markdown("""
    **Multi-Agent System:**
    - 🔍 **Logistics Analyst**: Identifies inefficiencies
    - 🎯 **Optimization Strategist**: Creates actionable plans
    
    **Powered by:**
    - CrewAI Framework
    - Google Gemini AI
    - Advanced logistics algorithms
    """)
    
    st.header("⚙️ Setup Required")
    st.markdown("""
    1. Create `.env` file
    2. Add: `GOOGLE_API_KEY=your_key`
    3. Install requirements
    4. Run the app
    """)
    
    if st.button("🔄 Clear Analysis", type="secondary"):
        if 'analysis_complete' in st.session_state:
            del st.session_state.analysis_complete
        if 'last_result' in st.session_state:
            del st.session_state.last_result
        st.rerun()

# Input section
st.subheader("📦 Product Input")
col1, col2 = st.columns([3, 1])

with col1:
    product_input = st.text_input(
        "Enter product names separated by commas",
        "TV, Laptops, Headphones, Smartphones, Tablets",
        help="Add products you want to analyze for logistics optimization"
    )

with col2:
    st.markdown("**Examples:**")
    if st.button("Electronics", type="secondary"):
        st.session_state.product_input = "TV, Laptops, Smartphones, Tablets"
    if st.button("Furniture", type="secondary"):
        st.session_state.product_input = "Sofa, Table, Chair, Bed"
    if st.button("Clothing", type="secondary"):
        st.session_state.product_input = "Shirts, Pants, Shoes, Jackets"

# Advanced options
with st.expander("🔧 Advanced Options", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        temperature = st.slider("AI Creativity Level", 0.0, 1.0, 0.3, 0.1, help="Higher values = more creative responses")
        focus_area = st.selectbox(
            "Primary Focus Area",
            ["Overall Optimization", "Cost Reduction", "Speed Improvement", "Route Optimization", "Inventory Management"]
        )
    with col2:
        region = st.selectbox(
            "Geographic Region",
            ["Global", "North America", "Europe", "Asia-Pacific", "Latin America", "Africa"]
        )
        company_size = st.selectbox(
            "Company Size",
            ["Startup", "Small Business", "Medium Enterprise", "Large Corporation"]
        )

# Main analysis button
analyze_button = st.button("🚀 Start Logistics Analysis", type="primary", use_container_width=True)

# Analysis execution
if analyze_button:
    # Validation
    if not GOOGLE_API_KEY:
        st.error("❌ **Google API Key Missing!** Please add your GOOGLE_API_KEY to the .env file.")
        st.info("Get your API key from [Google AI Studio](https://makersuite.google.com/)")
        st.stop()
    
    if not product_input.strip():
        st.error("❌ Please enter at least one product name.")
        st.stop()
    
    # Parse products
    products = [p.strip() for p in product_input.split(",") if p.strip()]
    
    if len(products) == 0:
        st.error("❌ No valid products found. Please check your input.")
        st.stop()
    
    # Main analysis
    with st.spinner("🤖 CrewAI agents are analyzing your logistics..."):
        try:
            # Initialize LLM with CrewAI's LLM wrapper
            llm = LLM(
                model="gemini/gemini-1.5-flash",
                temperature=temperature,
                api_key=GOOGLE_API_KEY
            )
            
            # Create specialized agents
            logistics_analyst = Agent(
                role="Senior Logistics Analyst",
                goal=f"Conduct comprehensive analysis of logistics operations for {', '.join(products)} with focus on {focus_area.lower()}",
                backstory=f"""You are a seasoned logistics analyst with 15+ years of experience in supply chain optimization. 
                You specialize in analyzing {company_size.lower()} operations in the {region} region. 
                Your expertise includes identifying bottlenecks, analyzing delivery routes, inventory turnover patterns, 
                and cost optimization opportunities. You provide data-driven insights with specific metrics and recommendations.""",
                verbose=True,
                allow_delegation=False,
                llm=llm,
                max_iter=3,
                max_rpm=10
            )
            
            optimization_strategist = Agent(
                role="Logistics Optimization Strategist", 
                goal=f"Design and implement cutting-edge optimization strategies for {company_size.lower()} logistics operations",
                backstory=f"""You are a world-renowned logistics optimization expert known for transforming 
                {company_size.lower()} supply chains in the {region} market. You specialize in implementing 
                AI-driven solutions, route optimization algorithms, and inventory management systems. 
                Your strategies have saved companies millions in operational costs while improving delivery times by 30-50%. 
                You focus on practical, implementable solutions with clear ROI projections.""",
                verbose=True,
                allow_delegation=False,
                llm=llm,
                max_iter=3,
                max_rpm=10
            )
            
            # Create detailed tasks
            analysis_task = Task(
                description=f"""Perform a comprehensive logistics analysis for the following products: {products}
                
                **Analysis Requirements:**
                1. **Current State Assessment:**
                   - Identify delivery route inefficiencies and bottlenecks
                   - Analyze inventory turnover rates and storage challenges
                   - Evaluate transportation costs and time delays
                   - Assess warehouse operations and distribution patterns
                
                2. **Geographic Considerations:**
                   - Focus on {region} market dynamics
                   - Consider regional shipping challenges and opportunities
                   - Analyze local distribution networks
                
                3. **Company Size Context:**
                   - Tailor analysis for {company_size.lower()} operational scale
                   - Consider resource constraints and growth potential
                
                4. **Primary Focus:**
                   - Prioritize {focus_area.lower()} in your analysis
                   - Provide specific metrics and benchmarks
                
                **Deliverables:**
                - Detailed current state assessment
                - Key performance indicators (KPIs) analysis
                - Critical bottlenecks and pain points
                - Quantified improvement opportunities
                - Risk assessment and mitigation factors""",
                expected_output="""A comprehensive logistics analysis report containing:
                1. Executive summary of current logistics performance
                2. Detailed breakdown of inefficiencies with quantified impacts
                3. Benchmark comparisons and industry standards
                4. Priority improvement areas with potential ROI
                5. Risk factors and operational challenges""",
                agent=logistics_analyst
            )
            
            strategy_task = Task(
                description=f"""Based on the logistics analyst's findings, develop a comprehensive optimization strategy.
                
                **Strategy Development Requirements:**
                1. **Actionable Solutions:**
                   - Specific recommendations for each identified inefficiency
                   - Implementation timeline with phases and milestones
                   - Resource requirements and budget estimates
                
                2. **Technology Integration:**
                   - AI/ML solutions for route optimization
                   - Inventory management system recommendations
                   - Automation opportunities and IoT integration
                
                3. **Focus Area Optimization:**
                   - Detailed strategies for {focus_area.lower()}
                   - Expected improvements and success metrics
                
                4. **Implementation Plan:**
                   - Phase-wise rollout strategy
                   - Change management considerations
                   - Training and adoption requirements
                
                **Deliverables:**
                - Strategic optimization roadmap
                - Technology implementation plan
                - Cost-benefit analysis with ROI projections
                - Success metrics and KPI framework
                - Risk mitigation strategies""",
                expected_output="""A detailed optimization strategy document including:
                1. Strategic roadmap with clear phases and timelines
                2. Technology solutions with implementation costs
                3. Expected benefits and ROI calculations
                4. Success metrics and monitoring framework
                5. Risk mitigation and contingency plans
                6. Practical next steps and quick wins""",
                agent=optimization_strategist,
                context=[analysis_task]
            )
            
            # Create and execute crew - DISABLED MEMORY to avoid ChromaDB/OpenAI dependency
            logistics_crew = Crew(
                agents=[logistics_analyst, optimization_strategist],
                tasks=[analysis_task, strategy_task],
                process=Process.sequential,
                verbose=True,
                memory=False  # Changed from True to False to avoid ChromaDB dependency
            )
            
            # Execute the crew
            result = logistics_crew.kickoff()
            
            # Store results
            st.session_state.analysis_complete = True
            st.session_state.last_result = result
            st.session_state.last_products = products  # Store products for later use
            
        except Exception as e:
            st.error(f"❌ **Analysis Failed:** {str(e)}")
            st.info("**Troubleshooting Tips:**")
            st.markdown("""
            - Check your Google API key is valid and active
            - Ensure stable internet connection
            - Verify API quota limits haven't been exceeded
            - Try reducing the number of products or simplifying input
            """)
            st.stop()

# Display results
if st.session_state.get('analysis_complete', False) and st.session_state.get('last_result'):
    st.success("✅ **Analysis Complete!** Your logistics optimization strategy is ready.")
    
    # Results section
    st.subheader("📊 Complete Logistics Analysis & Strategy")
    
    # Create tabs for better organization
    tab1, tab2, tab3 = st.tabs(["📋 Full Report", "📈 Key Insights", "🎯 Action Items"])
    
    with tab1:
        st.markdown("### 📄 Complete Analysis Report")
        st.markdown(st.session_state.last_result)
    
    with tab2:
        st.markdown("### 🔍 Key Performance Insights")
        st.info("**AI-Generated Summary:** Key metrics and improvement opportunities identified by our logistics experts.")
        # You could add additional processing here to extract key metrics
    
    with tab3:
        st.markdown("### ✅ Recommended Action Items")
        st.info("**Implementation Roadmap:** Prioritized steps for logistics optimization.")
        # You could add additional processing here to extract action items
    
    # Download option
    # Get products from session state or parse from current input
    current_products = []
    if 'last_products' in st.session_state:
        current_products = st.session_state.last_products
    else:
        # Fallback: parse from current input
        if product_input.strip():
            current_products = [p.strip() for p in product_input.split(",") if p.strip()]
    
    filename = f"logistics_optimization_report_{'-'.join(current_products[:3])}.txt" if current_products else "logistics_optimization_report.txt"
    
    st.download_button(
        label="💾 Download Complete Report",
        data=str(st.session_state.last_result),
        file_name=filename,
        mime="text/plain",
        type="secondary"
    )

# Footer
st.markdown("---")
st.markdown("**Powered by CrewAI + Google Gemini** | Built for advanced logistics optimization")