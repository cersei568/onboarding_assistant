import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Smart Onboarding Platform", 
    layout="wide", 
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    /* Main styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 600;
    }
    
    /* Card styling */
    .status-card {
        padding: 1.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .info-card {
        padding: 1.5rem;
        border-radius: 10px;
        background: white;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Success/Warning/Error boxes */
    .element-container div[data-testid="stNotificationContentSuccess"] {
        background-color: #d4edda;
        border-color: #c3e6cb;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        border-radius: 6px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 6px 6px 0 0;
        font-weight: 500;
    }
    
    /* Header styling */
    h1 {
        color: #1e293b;
        font-weight: 700;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
        margin-bottom: 2rem;
    }
    
    h2 {
        color: #334155;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    h3 {
        color: #475569;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'employees' not in st.session_state:
    st.session_state.employees = {}
if 'current_employee' not in st.session_state:
    st.session_state.current_employee = None
if 'notifications' not in st.session_state:
    st.session_state.notifications = []

# Sample data structure for a new employee
def create_employee(name, email, department, start_date, role):
    return {
        'name': name,
        'email': email,
        'department': department,
        'role': role,
        'start_date': start_date,
        'created_at': datetime.now(),
        'documents': {
            'Government ID': {'status': 'Pending', 'uploaded': None, 'verified_by': None, 'priority': 'High'},
            'Tax Forms (W-4/W-9)': {'status': 'Pending', 'uploaded': None, 'verified_by': None, 'priority': 'High'},
            'Direct Deposit Form': {'status': 'Pending', 'uploaded': None, 'verified_by': None, 'priority': 'High'},
            'Emergency Contact Info': {'status': 'Pending', 'uploaded': None, 'verified_by': None, 'priority': 'High'},
            'Signed Offer Letter': {'status': 'Pending', 'uploaded': None, 'verified_by': None, 'priority': 'High'},
            'I-9 Employment Eligibility': {'status': 'Pending', 'uploaded': None, 'verified_by': None, 'priority': 'Critical'},
            'Background Check Consent': {'status': 'Pending', 'uploaded': None, 'verified_by': None, 'priority': 'Medium'},
            'NDA Agreement': {'status': 'Pending', 'uploaded': None, 'verified_by': None, 'priority': 'High'}
        },
        'tasks': [
            {'name': 'Complete Employee Profile', 'status': 'Not Started', 'dependency': None, 'due_date': start_date + timedelta(days=1), 'category': 'Administrative', 'progress': 0},
            {'name': 'Review Company Handbook', 'status': 'Locked', 'dependency': 'Complete Employee Profile', 'due_date': start_date + timedelta(days=2), 'category': 'Orientation', 'progress': 0},
            {'name': 'Setup Work Email & Accounts', 'status': 'Locked', 'dependency': 'Complete Employee Profile', 'due_date': start_date + timedelta(days=1), 'category': 'IT Setup', 'progress': 0},
            {'name': 'Attend Welcome Orientation', 'status': 'Locked', 'dependency': 'Setup Work Email & Accounts', 'due_date': start_date + timedelta(days=2), 'category': 'Orientation', 'progress': 0},
            {'name': 'Meet Team Members', 'status': 'Locked', 'dependency': 'Attend Welcome Orientation', 'due_date': start_date + timedelta(days=3), 'category': 'Social', 'progress': 0},
            {'name': 'Setup Development Environment', 'status': 'Locked', 'dependency': 'Setup Work Email & Accounts', 'due_date': start_date + timedelta(days=3), 'category': 'IT Setup', 'progress': 0},
            {'name': 'Shadow Team Member', 'status': 'Locked', 'dependency': 'Meet Team Members', 'due_date': start_date + timedelta(days=5), 'category': 'Training', 'progress': 0},
            {'name': 'Review First Assignment', 'status': 'Locked', 'dependency': 'Shadow Team Member', 'due_date': start_date + timedelta(days=7), 'category': 'Work', 'progress': 0},
            {'name': '30-Day Check-in with Manager', 'status': 'Locked', 'dependency': 'Review First Assignment', 'due_date': start_date + timedelta(days=30), 'category': 'Review', 'progress': 0}
        ],
        'meetings': [],
        'equipment': {
            'MacBook Pro / Windows Laptop': {'status': 'Pending', 'assigned_date': None, 'serial_number': '', 'assigned_by': None},
            'External Monitor(s)': {'status': 'Pending', 'assigned_date': None, 'serial_number': '', 'assigned_by': None},
            'Keyboard & Mouse': {'status': 'Pending', 'assigned_date': None, 'serial_number': '', 'assigned_by': None},
            'Access Card/Badge': {'status': 'Pending', 'assigned_date': None, 'serial_number': '', 'assigned_by': None},
            'Mobile Phone': {'status': 'Pending', 'assigned_date': None, 'serial_number': '', 'assigned_by': None},
            'Headset': {'status': 'Pending', 'assigned_date': None, 'serial_number': '', 'assigned_by': None},
            'Desk & Chair': {'status': 'Pending', 'assigned_date': None, 'serial_number': '', 'assigned_by': None}
        },
        'compliance': {
            'Data Protection & Privacy (GDPR)': {'status': 'Not Started', 'due_date': start_date + timedelta(days=5), 'completed': None, 'duration': '45 min', 'priority': 'Critical'},
            'Information Security Awareness': {'status': 'Not Started', 'due_date': start_date + timedelta(days=7), 'completed': None, 'duration': '30 min', 'priority': 'Critical'},
            'Workplace Health & Safety': {'status': 'Not Started', 'due_date': start_date + timedelta(days=3), 'completed': None, 'duration': '20 min', 'priority': 'High'},
            'Code of Conduct & Ethics': {'status': 'Not Started', 'due_date': start_date + timedelta(days=2), 'completed': None, 'duration': '25 min', 'priority': 'High'},
            'Anti-Harassment Policy': {'status': 'Not Started', 'due_date': start_date + timedelta(days=5), 'completed': None, 'duration': '30 min', 'priority': 'High'},
            'Cybersecurity Best Practices': {'status': 'Not Started', 'due_date': start_date + timedelta(days=10), 'completed': None, 'duration': '40 min', 'priority': 'Medium'}
        },
        'surveys': [],
        'notes': []
    }

def get_completion_percentage(emp_data):
    """Calculate overall onboarding completion percentage"""
    total_items = 0
    completed_items = 0
    
    # Documents
    total_items += len(emp_data['documents'])
    completed_items += sum(1 for d in emp_data['documents'].values() if d['status'] == 'Verified')
    
    # Tasks
    total_items += len(emp_data['tasks'])
    completed_items += sum(1 for t in emp_data['tasks'] if t['status'] == 'Completed')
    
    # Equipment
    total_items += len(emp_data['equipment'])
    completed_items += sum(1 for e in emp_data['equipment'].values() if e['status'] == 'Assigned')
    
    # Compliance
    total_items += len(emp_data['compliance'])
    completed_items += sum(1 for c in emp_data['compliance'].values() if c['status'] == 'Completed')
    
    return int((completed_items / total_items * 100)) if total_items > 0 else 0

def get_status_color(status):
    """Return color code for status"""
    colors = {
        'Pending': '#fbbf24',
        'Uploaded': '#60a5fa',
        'Verified': '#34d399',
        'Rejected': '#f87171',
        'Not Started': '#94a3b8',
        'In Progress': '#60a5fa',
        'Completed': '#34d399',
        'Locked': '#cbd5e1',
        'Assigned': '#34d399',
        'Scheduled': '#60a5fa',
        'Overdue': '#ef4444',
        'Critical': '#dc2626',
        'High': '#f59e0b',
        'Medium': '#3b82f6',
        'Low': '#6b7280'
    }
    return colors.get(status, '#6b7280')

# Sidebar
with st.sidebar:
    st.markdown("### 🚀 Smart Onboarding Platform")
    st.markdown("---")
    
    # Navigation
    page = st.radio("Navigation", 
                    ["📊 Dashboard", 
                     "👥 Employee Management", 
                     "📄 Documents", 
                     "✅ Tasks & Workflow", 
                     "📅 Meetings", 
                     "💻 Equipment", 
                     "📚 Compliance Training", 
                     "📊 Surveys & Analytics"],
                    label_visibility="collapsed")
    
    # Employee selector
    if st.session_state.employees:
        st.markdown("---")
        st.markdown("**Select Employee**")
        employee_names = list(st.session_state.employees.keys())
        selected = st.selectbox("", ["All Employees"] + employee_names, label_visibility="collapsed")
        st.session_state.current_employee = None if selected == "All Employees" else selected
        
        if st.session_state.current_employee:
            emp_data = st.session_state.employees[st.session_state.current_employee]
            completion = get_completion_percentage(emp_data)
            st.metric("Onboarding Progress", f"{completion}%")
            st.progress(completion / 100)
    
    st.markdown("---")
    st.caption("v2.0 Professional Edition")
    st.caption("© 2025 Smart Onboarding")

# Main content
if page == "📊 Dashboard":
    st.title("📊 Onboarding Dashboard")
    
    if not st.session_state.employees:
        st.markdown("""
        <div class="info-card">
            <h3>👋 Welcome to Smart Onboarding Platform</h3>
            <p>Get started by adding your first employee in the <strong>Employee Management</strong> section.</p>
            <ul>
                <li>Automate document collection and verification</li>
                <li>Track progressive task completion</li>
                <li>Schedule orientation meetings</li>
                <li>Manage equipment provisioning</li>
                <li>Monitor compliance training</li>
                <li>Analyze employee sentiment</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Key metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        total_employees = len(st.session_state.employees)
        pending_docs = sum(1 for emp in st.session_state.employees.values() 
                          for doc in emp['documents'].values() if doc['status'] in ['Pending', 'Uploaded'])
        pending_equipment = sum(1 for emp in st.session_state.employees.values() 
                               for eq in emp['equipment'].values() if eq['status'] == 'Pending')
        overdue_compliance = sum(1 for emp in st.session_state.employees.values() 
                                for comp in emp['compliance'].values() 
                                if comp['status'] != 'Completed' and comp['due_date'] < datetime.now())
        avg_completion = int(sum(get_completion_percentage(emp) for emp in st.session_state.employees.values()) / total_employees)
        
        col1.metric("Active Employees", total_employees, delta=None)
        col2.metric("Pending Documents", pending_docs, delta=None, delta_color="inverse")
        col3.metric("Equipment Requests", pending_equipment, delta=None, delta_color="inverse")
        col4.metric("Overdue Training", overdue_compliance, delta=None, delta_color="inverse")
        col5.metric("Avg. Completion", f"{avg_completion}%", delta=None)
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Onboarding Progress by Employee")
            
            # Progress chart
            emp_names = []
            completions = []
            for emp_name, emp_data in st.session_state.employees.items():
                emp_names.append(emp_name)
                completions.append(get_completion_percentage(emp_data))
            
            fig = go.Figure(data=[
                go.Bar(x=emp_names, y=completions, 
                       marker_color='#667eea',
                       text=completions,
                       texttemplate='%{text}%',
                       textposition='outside')
            ])
            fig.update_layout(
                yaxis_title="Completion %",
                yaxis_range=[0, 110],
                height=300,
                margin=dict(l=20, r=20, t=20, b=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Task Status Distribution")
            
            # Task status pie chart
            status_counts = {'Not Started': 0, 'In Progress': 0, 'Completed': 0, 'Locked': 0}
            for emp_data in st.session_state.employees.values():
                for task in emp_data['tasks']:
                    status_counts[task['status']] = status_counts.get(task['status'], 0) + 1
            
            fig = go.Figure(data=[go.Pie(
                labels=list(status_counts.keys()),
                values=list(status_counts.values()),
                hole=.4,
                marker_colors=['#94a3b8', '#60a5fa', '#34d399', '#cbd5e1']
            )])
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=20, b=20),
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Employee cards
        st.markdown("### 👥 Employee Overview")
        
        for emp_name, emp_data in st.session_state.employees.items():
            with st.expander(f"**{emp_name}** - {emp_data['role']} | {emp_data['department']}", expanded=False):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    docs_complete = sum(1 for d in emp_data['documents'].values() if d['status'] == 'Verified')
                    st.metric("Documents", f"{docs_complete}/{len(emp_data['documents'])}")
                
                with col2:
                    tasks_complete = sum(1 for t in emp_data['tasks'] if t['status'] == 'Completed')
                    st.metric("Tasks", f"{tasks_complete}/{len(emp_data['tasks'])}")
                
                with col3:
                    equipment_assigned = sum(1 for e in emp_data['equipment'].values() if e['status'] == 'Assigned')
                    st.metric("Equipment", f"{equipment_assigned}/{len(emp_data['equipment'])}")
                
                with col4:
                    compliance_done = sum(1 for c in emp_data['compliance'].values() if c['status'] == 'Completed')
                    st.metric("Training", f"{compliance_done}/{len(emp_data['compliance'])}")
                
                # Progress bar
                completion = get_completion_percentage(emp_data)
                st.markdown(f"**Overall Progress:** {completion}%")
                st.progress(completion / 100)
                
                # Quick actions
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📄 View Documents", key=f"docs_{emp_name}"):
                        st.session_state.current_employee = emp_name
                        st.rerun()
                with col2:
                    if st.button("✅ View Tasks", key=f"tasks_{emp_name}"):
                        st.session_state.current_employee = emp_name
                        st.rerun()
                with col3:
                    if st.button("📊 View Analytics", key=f"analytics_{emp_name}"):
                        st.session_state.current_employee = emp_name
                        st.rerun()

elif page == "👥 Employee Management":
    st.title("👥 Employee Management")
    
    tab1, tab2 = st.tabs(["➕ Add New Employee", "📋 View All Employees"])
    
    with tab1:
        st.markdown("### Add New Hire to Onboarding")
        
        with st.form("new_employee", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name *", placeholder="John Doe")
                email = st.text_input("Email Address *", placeholder="john.doe@company.com")
                role = st.text_input("Job Title *", placeholder="Senior Software Engineer")
            
            with col2:
                department = st.selectbox("Department *", 
                    ["Engineering", "Product", "Design", "Sales", "Marketing", 
                     "Customer Success", "HR", "Finance", "Operations", "Legal"])
                start_date = st.date_input("Start Date *", min_value=datetime.now())
                manager = st.text_input("Direct Manager", placeholder="Jane Smith")
            
            submitted = st.form_submit_button("🚀 Create Onboarding Plan", use_container_width=True)
            
            if submitted:
                if name and email and role:
                    if name not in st.session_state.employees:
                        st.session_state.employees[name] = create_employee(
                            name, email, department, 
                            datetime.combine(start_date, datetime.min.time()), role
                        )
                        st.success(f"✅ Successfully created onboarding plan for **{name}**!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ An employee with this name already exists!")
                else:
                    st.error("❌ Please fill in all required fields!")
    
    with tab2:
        if st.session_state.employees:
            st.markdown("### All Employees")
            
            # Create DataFrame
            emp_list = []
            for emp_name, emp_data in st.session_state.employees.items():
                emp_list.append({
                    'Name': emp_name,
                    'Role': emp_data['role'],
                    'Department': emp_data['department'],
                    'Start Date': emp_data['start_date'].strftime('%Y-%m-%d'),
                    'Progress': f"{get_completion_percentage(emp_data)}%",
                    'Email': emp_data['email']
                })
            
            df = pd.DataFrame(emp_list)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Individual employee management
            st.markdown("### Manage Individual Employees")
            for emp_name, emp_data in st.session_state.employees.items():
                with st.expander(f"{emp_name} - {emp_data['role']}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Email:** {emp_data['email']}")
                        st.write(f"**Department:** {emp_data['department']}")
                        st.write(f"**Start Date:** {emp_data['start_date'].strftime('%B %d, %Y')}")
                        st.write(f"**Days Since Start:** {(datetime.now() - emp_data['start_date']).days} days")
                    
                    with col2:
                        if st.button("🗑️ Remove", key=f"remove_{emp_name}", type="secondary"):
                            del st.session_state.employees[emp_name]
                            st.success(f"Removed {emp_name}")
                            st.rerun()
        else:
            st.info("👆 No employees added yet. Use the form above to add your first employee.")

elif page == "📄 Documents":
    st.title("📄 Document Collection & Verification")
    
    if not st.session_state.current_employee:
        st.warning("⚠️ Please select an employee from the sidebar to manage their documents.")
    else:
        emp_name = st.session_state.current_employee
        emp_data = st.session_state.employees[emp_name]
        
        st.markdown(f"### Documents for **{emp_name}**")
        
        # Document stats
        col1, col2, col3, col4 = st.columns(4)
        total_docs = len(emp_data['documents'])
        verified = sum(1 for d in emp_data['documents'].values() if d['status'] == 'Verified')
        uploaded = sum(1 for d in emp_data['documents'].values() if d['status'] == 'Uploaded')
        pending = sum(1 for d in emp_data['documents'].values() if d['status'] == 'Pending')
        
        col1.metric("Total Documents", total_docs)
        col2.metric("✅ Verified", verified)
        col3.metric("📤 Uploaded", uploaded)
        col4.metric("⏳ Pending", pending)
        
        st.markdown("---")
        
        # Filter
        filter_status = st.multiselect("Filter by Status", 
                                       ["Pending", "Uploaded", "Verified", "Rejected"],
                                       default=["Pending", "Uploaded"])
        
        # Documents table
        for doc_name, doc_info in emp_data['documents'].items():
            if doc_info['status'] in filter_status or not filter_status:
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([3, 1.5, 1, 1.5, 1.5])
                    
                    with col1:
                        priority_emoji = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "⚪"}
                        st.markdown(f"{priority_emoji.get(doc_info['priority'], '⚪')} **{doc_name}**")
                        st.caption(f"Priority: {doc_info['priority']}")
                    
                    with col2:
                        status_colors = {
                            'Pending': ('⏳', '#fbbf24'),
                            'Uploaded': ('📤', '#60a5fa'),
                            'Verified': ('✅', '#34d399'),
                            'Rejected': ('❌', '#f87171')
                        }
                        emoji, color = status_colors.get(doc_info['status'], ('⚪', '#6b7280'))
                        st.markdown(f"<span style='color: {color}; font-weight: 600;'>{emoji} {doc_info['status']}</span>", 
                                  unsafe_allow_html=True)
                    
                    with col3:
                        if doc_info['uploaded']:
                            st.caption(f"📅 {doc_info['uploaded'].strftime('%m/%d/%y')}")
                    
                    with col4:
                        uploaded_file = st.file_uploader("Upload", 
                                                        key=f"upload_{doc_name}_{emp_name}",
                                                        label_visibility="collapsed",
                                                        accept_multiple_files=False)
                        if uploaded_file:
                            emp_data['documents'][doc_name]['status'] = 'Uploaded'
                            emp_data['documents'][doc_name]['uploaded'] = datetime.now()
                            st.rerun()
                    
                    with col5:
                        if doc_info['status'] == 'Uploaded':
                            col_a, col_b = st.columns(2)
                            if col_a.button("✓", key=f"verify_{doc_name}_{emp_name}", type="primary"):
                                emp_data['documents'][doc_name]['status'] = 'Verified'
                                emp_data['documents'][doc_name]['verified_by'] = 'Admin'
                                st.rerun()
                            if col_b.button("✗", key=f"reject_{doc_name}_{emp_name}", type="secondary"):
                                emp_data['documents'][doc_name]['status'] = 'Rejected'
                                st.rerun()
                    
                    st.divider()

elif page == "✅ Tasks & Workflow":
    st.title("✅ Progressive Task Management")
    
    if not st.session_state.current_employee:
        st.warning("⚠️ Please select an employee from the sidebar to manage their tasks.")
    else:
        emp_name = st.session_state.current_employee
        emp_data = st.session_state.employees[emp_name]
        
        st.markdown(f"### Task Workflow for **{emp_name}**")
        
        # Task stats
        col1, col2, col3, col4 = st.columns(4)
        total_tasks = len(emp_data['tasks'])
        completed = sum(1 for t in emp_data['tasks'] if t['status'] == 'Completed')
        in_progress = sum(1 for t in emp_data['tasks'] if t['status'] == 'In Progress')
        locked = sum(1 for t in emp_data['tasks'] if t['status'] == 'Locked')
        
        col1.metric("Total Tasks", total_tasks)
        col2.metric("✅ Completed", completed)
        col3.metric("🔄 In Progress", in_progress)
        col4.metric("🔒 Locked", locked)
        
        st.markdown("---")
        
        # Category filter
        categories = list(set(task['category'] for task in emp_data['tasks']))
        selected_category = st.selectbox("Filter by Category", ["All Categories"] + categories)
        
        # Tasks with dependency chain visualization
        for idx, task in enumerate(emp_data['tasks']):
            if selected_category == "All Categories" or task['category'] == selected_category:
                with st.container():
                    col1, col2, col3, col4 = st.columns([4, 1.5, 1.5, 2])
                    
                    with col1:
                        # Task icon based on status
                        icons = {
                            'Locked': '🔒',
                            'Not Started': '⭕',
                            'In Progress': '🔄',
                            'Completed': '✅'
                        }
                        icon = icons.get(task['status'], '⭕')
                        
                        st.markdown(f"{icon} **{task['name']}**")
                        
                        if task['dependency']:
                            st.caption(f"🔗 Requires: *{task['dependency']}*")
                        
                        st.caption(f"📂 {task['category']}")
                    
                    with col2:
                        due_date = task['due_date']
                        days_left = (due_date - datetime.now()).days
                        
                        if days_left < 0 and task['status'] != 'Completed':
                            st.markdown(f"<span style='color: #ef4444; font-weight: 600;'>⚠️ Overdue</span>", unsafe_allow_html=True)
                        else:
                            st.write(f"📅 {due_date.strftime('%m/%d/%y')}")
                            if days_left <= 3 and task['status'] != 'Completed':
                                st.caption(f"⏰ {days_left} days left")
                    
                    with col3:
                        status_colors = {
                            'Locked': '#cbd5e1',
                            'Not Started': '#94a3b8',
                            'In Progress': '#60a5fa',
                            'Completed': '#34d399'
                        }
                        color = status_colors.get(task['status'], '#6b7280')
                        st.markdown(f"<span style='color: {color}; font-weight: 600;'>{task['status']}</span>", 
                                  unsafe_allow_html=True)
                    
                    with col4:
                        if task['status'] == 'Locked':
                            st.button("🔒 Locked", disabled=True, key=f"task_{idx}_{emp_name}")
                        elif task['status'] == 'Completed':
                            st.success("✅ Done!")
                        elif task['status'] == 'Not Started':
                            if st.button("▶️ Start Task", key=f"task_{idx}_{emp_name}", type="primary"):
                                task['status'] = 'In Progress'
                                st.rerun()
                        else:  # In Progress
                            if st.button("✓ Complete", key=f"task_{idx}_{emp_name}", type="primary"):
                                task['status'] = 'Completed'
                                task['progress'] = 100
                                # Unlock dependent tasks
                                for t in emp_data['tasks']:
                                    if t['dependency'] == task['name'] and t['status'] == 'Locked':
                                        t['status'] = 'Not Started'
                                st.rerun()
                    
                    st.divider()

elif page == "📅 Meetings":
    st.title("📅 Orientation Meeting Scheduler")
    
    if not st.session_state.current_employee:
        st.warning("⚠️ Please select an employee from the sidebar to schedule meetings.")
    else:
        emp_name = st.session_state.current_employee
        emp_data = st.session_state.employees[emp_name]
        
        st.markdown(f"### Meeting Schedule for **{emp_name}**")
        
        tab1, tab2 = st.tabs(["📅 Schedule New Meeting", "📋 Upcoming Meetings"])
        
        with tab1:
            departments = [
                "HR Orientation",
                "IT Setup & Security",
                "Direct Manager 1:1",
                "Team Introduction",
                "Finance & Benefits",
                "Facilities Tour",
                "Legal & Compliance",
                "Product Training",
                "Engineering Team",
                "Customer Success Team"
            ]
            
            with st.form("schedule_meeting"):
                col1, col2 = st.columns(2)
                
                with col1:
                    dept = st.selectbox("Meeting Type", departments)
                    meeting_date = st.date_input("Date", min_value=datetime.now())
                    attendees = st.text_input("Attendees (optional)", placeholder="john@company.com, jane@company.com")
                
                with col2:
                    meeting_time = st.time_input("Time", value=datetime.now().replace(hour=10, minute=0))
                    duration = st.selectbox("Duration", ["15 min", "30 min", "45 min", "1 hour", "1.5 hours", "2 hours"])
                    location = st.text_input("Location/Link", placeholder="Conference Room A or Zoom link")
                
                notes = st.text_area("Meeting Notes/Agenda")
                
                submitted = st.form_submit_button("📅 Schedule Meeting", use_container_width=True, type="primary")
                
                if submitted:
                    meeting = {
                        'department': dept,
                        'datetime': datetime.combine(meeting_date, meeting_time),
                        'duration': duration,
                        'location': location,
                        'attendees': attendees,
                        'notes': notes,
                        'status': 'Scheduled',
                        'created_at': datetime.now()
                    }
                    emp_data['meetings'].append(meeting)
                    st.success(f"✅ Meeting '{dept}' scheduled successfully!")
                    st.rerun()
        
        with tab2:
            if emp_data['meetings']:
                # Sort meetings by datetime
                sorted_meetings = sorted(emp_data['meetings'], key=lambda x: x['datetime'])
                
                # Stats
                scheduled = sum(1 for m in emp_data['meetings'] if m['status'] == 'Scheduled')
                completed = sum(1 for m in emp_data['meetings'] if m['status'] == 'Completed')
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Meetings", len(emp_data['meetings']))
                col2.metric("📅 Scheduled", scheduled)
                col3.metric("✅ Completed", completed)
                
                st.markdown("---")
                
                for idx, meeting in enumerate(sorted_meetings):
                    meeting_dt = meeting['datetime']
                    is_upcoming = meeting_dt > datetime.now()
                    
                    with st.expander(
                        f"{'📅' if is_upcoming else '✅'} {meeting['department']} - {meeting_dt.strftime('%b %d, %Y at %I:%M %p')}",
                        expanded=is_upcoming and meeting['status'] == 'Scheduled'
                    ):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.write(f"**Duration:** {meeting['duration']}")
                            if meeting['location']:
                                st.write(f"**Location:** {meeting['location']}")
                            if meeting['attendees']:
                                st.write(f"**Attendees:** {meeting['attendees']}")
                            if meeting['notes']:
                                st.write(f"**Notes:** {meeting['notes']}")
                        
                        with col2:
                            if meeting['status'] == 'Scheduled':
                                if st.button("✓ Mark Complete", key=f"meeting_{idx}", type="primary"):
                                    emp_data['meetings'][idx]['status'] = 'Completed'
                                    st.rerun()
                                if st.button("🗑️ Cancel", key=f"cancel_meeting_{idx}"):
                                    emp_data['meetings'].pop(idx)
                                    st.rerun()
                            else:
                                st.success("✅ Completed")
            else:
                st.info("📅 No meetings scheduled yet. Use the form above to schedule orientation meetings.")

elif page == "💻 Equipment":
    st.title("💻 Equipment Provisioning Workflow")
    
    if not st.session_state.current_employee:
        st.warning("⚠️ Please select an employee from the sidebar to manage equipment.")
    else:
        emp_name = st.session_state.current_employee
        emp_data = st.session_state.employees[emp_name]
        
        st.markdown(f"### Equipment for **{emp_name}**")
        
        # Equipment stats
        col1, col2, col3 = st.columns(3)
        total_items = len(emp_data['equipment'])
        assigned = sum(1 for e in emp_data['equipment'].values() if e['status'] == 'Assigned')
        pending = total_items - assigned
        
        col1.metric("Total Items", total_items)
        col2.metric("✅ Assigned", assigned)
        col3.metric("⏳ Pending", pending)
        
        st.markdown("---")
        
        # Equipment table
        for eq_name, eq_info in emp_data['equipment'].items():
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                
                with col1:
                    st.markdown(f"**{eq_name}**")
                    if eq_info.get('serial_number'):
                        st.caption(f"S/N: {eq_info['serial_number']}")
                
                with col2:
                    if eq_info['status'] == 'Assigned':
                        st.success(f"✅ Assigned")
                        if eq_info['assigned_date']:
                            st.caption(f"{eq_info['assigned_date'].strftime('%m/%d/%y')}")
                    else:
                        st.warning("⏳ Pending")
                
                with col3:
                    if eq_info['status'] == 'Pending':
                        serial = st.text_input("Serial #", key=f"serial_{eq_name}_{emp_name}", 
                                             placeholder="Optional", label_visibility="collapsed")
                
                with col4:
                    if eq_info['status'] == 'Pending':
                        if st.button("✓ Assign", key=f"eq_{eq_name}_{emp_name}", type="primary"):
                            emp_data['equipment'][eq_name]['status'] = 'Assigned'
                            emp_data['equipment'][eq_name]['assigned_date'] = datetime.now()
                            emp_data['equipment'][eq_name]['assigned_by'] = 'Admin'
                            if f"serial_{eq_name}_{emp_name}" in st.session_state:
                                serial_val = st.session_state[f"serial_{eq_name}_{emp_name}"]
                                if serial_val:
                                    emp_data['equipment'][eq_name]['serial_number'] = serial_val
                            st.rerun()
                    else:
                        if eq_info.get('assigned_by'):
                            st.caption(f"By: {eq_info['assigned_by']}")
                
                st.divider()

elif page == "📚 Compliance Training":
    st.title("📚 Compliance Training Tracker")
    
    if not st.session_state.current_employee:
        st.warning("⚠️ Please select an employee from the sidebar to manage training.")
    else:
        emp_name = st.session_state.current_employee
        emp_data = st.session_state.employees[emp_name]
        
        st.markdown(f"### Compliance Training for **{emp_name}**")
        
        # Training stats
        col1, col2, col3, col4 = st.columns(4)
        total_training = len(emp_data['compliance'])
        completed = sum(1 for c in emp_data['compliance'].values() if c['status'] == 'Completed')
        overdue = sum(1 for c in emp_data['compliance'].values() 
                     if c['status'] != 'Completed' and c['due_date'] < datetime.now())
        in_progress = sum(1 for c in emp_data['compliance'].values() if c['status'] == 'In Progress')
        
        col1.metric("Total Modules", total_training)
        col2.metric("✅ Completed", completed)
        col3.metric("⚠️ Overdue", overdue, delta_color="inverse")
        col4.metric("🔄 In Progress", in_progress)
        
        st.markdown("---")
        
        # Training modules
        for training_name, training_info in emp_data['compliance'].items():
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([3, 1, 1.5, 1, 1.5])
                
                with col1:
                    priority_colors = {
                        'Critical': '🔴',
                        'High': '🟠',
                        'Medium': '🟡',
                        'Low': '⚪'
                    }
                    priority_icon = priority_colors.get(training_info['priority'], '⚪')
                    
                    st.markdown(f"{priority_icon} **{training_name}**")
                    st.caption(f"⏱️ Duration: {training_info['duration']} | Priority: {training_info['priority']}")
                
                with col2:
                    due_date = training_info['due_date']
                    days_left = (due_date - datetime.now()).days
                    
                    if training_info['status'] == 'Completed':
                        st.success("✅ Done")
                    elif days_left < 0:
                        st.error("⚠️ Overdue")
                    else:
                        st.write(f"📅 {due_date.strftime('%m/%d')}")
                
                with col3:
                    if training_info['status'] == 'Completed':
                        st.caption(f"✓ {training_info['completed'].strftime('%m/%d/%y')}")
                    elif days_left < 0:
                        st.caption(f"{abs(days_left)} days overdue")
                    else:
                        st.caption(f"{days_left} days left")
                
                with col4:
                    status_colors = {
                        'Not Started': '#94a3b8',
                        'In Progress': '#60a5fa',
                        'Completed': '#34d399'
                    }
                    color = status_colors.get(training_info['status'], '#6b7280')
                    st.markdown(f"<span style='color: {color}; font-weight: 600;'>{training_info['status']}</span>", 
                              unsafe_allow_html=True)
                
                with col5:
                    if training_info['status'] == 'Not Started':
                        if st.button("▶️ Start", key=f"start_{training_name}_{emp_name}", type="primary"):
                            emp_data['compliance'][training_name]['status'] = 'In Progress'
                            st.rerun()
                    elif training_info['status'] == 'In Progress':
                        if st.button("✓ Complete", key=f"comp_{training_name}_{emp_name}", type="primary"):
                            emp_data['compliance'][training_name]['status'] = 'Completed'
                            emp_data['compliance'][training_name]['completed'] = datetime.now()
                            st.rerun()
                
                st.divider()
        
        # Automatic reminders section
        st.markdown("---")
        st.markdown("### 📧 Automatic Reminders")
        
        reminders = []
        for training_name, training_info in emp_data['compliance'].items():
            if training_info['status'] != 'Completed':
                days_until_due = (training_info['due_date'] - datetime.now()).days
                if days_until_due <= 7:
                    reminders.append((training_name, training_info, days_until_due))
        
        if reminders:
            for training_name, training_info, days_left in sorted(reminders, key=lambda x: x[2]):
                if days_left < 0:
                    st.error(f"🚨 **Urgent:** {training_name} is {abs(days_left)} days overdue!")
                elif days_left <= 3:
                    st.warning(f"⚠️ **Reminder:** {training_name} due in {days_left} days")
                else:
                    st.info(f"📧 Reminder sent for {training_name} (due in {days_left} days)")
        else:
            st.success("✅ All trainings are on track!")

elif page == "📊 Surveys & Analytics":
    st.title("📊 Check-in Surveys & Sentiment Analysis")
    
    if not st.session_state.current_employee:
        st.warning("⚠️ Please select an employee from the sidebar.")
    else:
        emp_name = st.session_state.current_employee
        emp_data = st.session_state.employees[emp_name]
        
        tab1, tab2, tab3 = st.tabs(["📝 Submit Survey", "📈 View Analytics", "💬 Survey History"])
        
        with tab1:
            st.markdown(f"### Weekly Check-in for **{emp_name}**")
            
            with st.form("survey_form"):
                st.markdown("#### Rate Your Experience")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    satisfaction = st.slider("Overall Satisfaction", 1, 10, 5, 
                                           help="How satisfied are you with your onboarding experience?")
                    onboarding_clarity = st.slider("Onboarding Process Clarity", 1, 10, 5,
                                                  help="How clear and organized is the onboarding process?")
                    support = st.slider("Team Support", 1, 10, 5,
                                      help="How supported do you feel by your team?")
                
                with col2:
                    resources = st.slider("Resource Availability", 1, 10, 5,
                                        help="Do you have the tools and resources you need?")
                    workload = st.slider("Workload Balance", 1, 10, 5,
                                       help="Is your workload manageable?")
                    culture_fit = st.slider("Cultural Alignment", 1, 10, 5,
                                          help="How well do you feel you fit with company culture?")
                
                st.markdown("#### Open Feedback")
                
                col1, col2 = st.columns(2)
                with col1:
                    challenges = st.text_area("What challenges are you facing?", 
                                             placeholder="Share any difficulties or concerns...")
                    wins = st.text_area("What's going well?",
                                      placeholder="Share your positive experiences...")
                
                with col2:
                    suggestions = st.text_area("Suggestions for improvement",
                                             placeholder="How can we improve the onboarding process?")
                    needs = st.text_area("What do you need help with?",
                                       placeholder="What support or resources would help you?")
                
                submitted = st.form_submit_button("📤 Submit Survey", use_container_width=True, type="primary")
                
                if submitted:
                    avg_score = (satisfaction + onboarding_clarity + support + resources + workload + culture_fit) / 6
                    
                    survey = {
                        'date': datetime.now(),
                        'satisfaction': satisfaction,
                        'onboarding_clarity': onboarding_clarity,
                        'support': support,
                        'resources': resources,
                        'workload': workload,
                        'culture_fit': culture_fit,
                        'avg_score': avg_score,
                        'challenges': challenges,
                        'wins': wins,
                        'suggestions': suggestions,
                        'needs': needs,
                        'sentiment': 'Positive' if avg_score >= 7 else 'Neutral' if avg_score >= 4 else 'Negative'
                    }
                    emp_data['surveys'].append(survey)
                    st.success("✅ Survey submitted successfully! Thank you for your feedback.")
                    st.balloons()
                    st.rerun()
        
        with tab2:
            if emp_data['surveys']:
                st.markdown(f"### Analytics Dashboard for **{emp_name}**")
                
                # Calculate comprehensive metrics
                surveys = emp_data['surveys']
                avg_satisfaction = sum(s['satisfaction'] for s in surveys) / len(surveys)
                avg_clarity = sum(s['onboarding_clarity'] for s in surveys) / len(surveys)
                avg_support = sum(s['support'] for s in surveys) / len(surveys)
                avg_resources = sum(s['resources'] for s in surveys) / len(surveys)
                avg_workload = sum(s['workload'] for s in surveys) / len(surveys)
                avg_culture = sum(s['culture_fit'] for s in surveys) / len(surveys)
                overall_avg = sum(s['avg_score'] for s in surveys) / len(surveys)
                
                # Key metrics
                col1, col2, col3, col4 = st.columns(4)
                
                def get_metric_color(score):
                    if score >= 8:
                        return "🟢"
                    elif score >= 6:
                        return "🟡"
                    else:
                        return "🔴"
                
                col1.metric("Overall Score", f"{overall_avg:.1f}/10", 
                          delta=f"{get_metric_color(overall_avg)}")
                col2.metric("Satisfaction", f"{avg_satisfaction:.1f}/10",
                          delta=f"{get_metric_color(avg_satisfaction)}")
                col3.metric("Team Support", f"{avg_support:.1f}/10",
                          delta=f"{get_metric_color(avg_support)}")
                col4.metric("Total Surveys", len(surveys))
                
                st.markdown("---")
                
                # Sentiment distribution
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 😊 Sentiment Distribution")
                    sentiment_counts = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
                    for survey in surveys:
                        sentiment_counts[survey['sentiment']] += 1
                    
                    fig = go.Figure(data=[go.Pie(
                        labels=list(sentiment_counts.keys()),
                        values=list(sentiment_counts.values()),
                        hole=.4,
                        marker_colors=['#34d399', '#fbbf24', '#f87171']
                    )])
                    fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                    
                    col_a, col_b, col_c = st.columns(3)
                    col_a.success(f"😊 {sentiment_counts['Positive']}")
                    col_b.warning(f"😐 {sentiment_counts['Neutral']}")
                    col_c.error(f"😟 {sentiment_counts['Negative']}")
                
                with col2:
                    st.markdown("### 📊 Scores by Category")
                    
                    categories = ['Satisfaction', 'Clarity', 'Support', 'Resources', 'Workload', 'Culture Fit']
                    scores = [avg_satisfaction, avg_clarity, avg_support, avg_resources, avg_workload, avg_culture]
                    
                    fig = go.Figure(data=[
                        go.Bar(x=categories, y=scores,
                              marker_color='#667eea',
                              text=[f"{s:.1f}" for s in scores],
                              textposition='outside')
                    ])
                    fig.update_layout(
                        yaxis_title="Average Score",
                        yaxis_range=[0, 11],
                        height=300,
                        margin=dict(l=20, r=20, t=20, b=20)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Trend over time
                if len(surveys) > 1:
                    st.markdown("---")
                    st.markdown("### 📈 Sentiment Trend Over Time")
                    
                    dates = [s['date'].strftime('%m/%d') for s in surveys]
                    scores = [s['avg_score'] for s in surveys]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=dates, y=scores,
                        mode='lines+markers',
                        line=dict(color='#667eea', width=3),
                        marker=dict(size=10),
                        fill='tozeroy',
                        fillcolor='rgba(102, 126, 234, 0.1)'
                    ))
                    fig.update_layout(
                        yaxis_title="Average Score",
                        xaxis_title="Date",
                        yaxis_range=[0, 10],
                        height=300,
                        margin=dict(l=20, r=20, t=20, b=40)
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📊 No survey data available yet. Submit your first survey to see analytics!")
        
        with tab3:
            if emp_data['surveys']:
                st.markdown(f"### Survey History for **{emp_name}**")
                
                for idx, survey in enumerate(reversed(emp_data['surveys'])):
                    sentiment_colors = {
                        'Positive': '#34d399',
                        'Neutral': '#fbbf24',
                        'Negative': '#f87171'
                    }
                    sentiment_icons = {
                        'Positive': '😊',
                        'Neutral': '😐',
                        'Negative': '😟'
                    }
                    
                    color = sentiment_colors[survey['sentiment']]
                    icon = sentiment_icons[survey['sentiment']]
                    
                    with st.expander(
                        f"{icon} {survey['date'].strftime('%B %d, %Y')} - {survey['sentiment']} (Score: {survey['avg_score']:.1f}/10)",
                        expanded=(idx == 0)
                    ):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**📊 Ratings**")
                            st.write(f"• Overall Satisfaction: **{survey['satisfaction']}/10**")
                            st.write(f"• Onboarding Clarity: **{survey['onboarding_clarity']}/10**")
                            st.write(f"• Team Support: **{survey['support']}/10**")
                            st.write(f"• Resources: **{survey['resources']}/10**")
                            st.write(f"• Workload: **{survey['workload']}/10**")
                            st.write(f"• Culture Fit: **{survey['culture_fit']}/10**")
                        
                        with col2:
                            st.markdown("**💬 Feedback**")
                            if survey.get('wins'):
                                st.success(f"✅ **What's going well:** {survey['wins']}")
                            if survey.get('challenges'):
                                st.warning(f"⚠️ **Challenges:** {survey['challenges']}")
                            if survey.get('suggestions'):
                                st.info(f"💡 **Suggestions:** {survey['suggestions']}")
                            if survey.get('needs'):
                                st.error(f"🆘 **Needs help with:** {survey['needs']}")
            else:
                st.info("📝 No surveys submitted yet. Use the 'Submit Survey' tab to add your first check-in!")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🚀 Smart Onboarding Platform")
with col2:
    st.caption("v2.0 Professional Edition")
with col3:
    st.caption("© 2025 All Rights Reserved")