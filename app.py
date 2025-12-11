from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
from spellchecker import SpellChecker
import random
import string
from flask.json.provider import DefaultJSONProvider

# ========================================================
# Custom JSON Provider: Fixes NumPy float serialization globally
# ========================================================
class CustomJSONProvider(DefaultJSONProvider):
    def default(self, o):
        try:
            if isinstance(o, (np.integer, np.floating)):
                return float(o)
            elif isinstance(o, np.ndarray):
                return o.tolist()
        except Exception:
            pass
        return super().default(o)
    

app = Flask(__name__)
app.json = CustomJSONProvider(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Realme6pro'
app.config['MYSQL_DB'] = 'job_matching_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


# Initialize spell checker and model
spell = SpellChecker()
model = SentenceTransformer('all-MiniLM-L6-v2')

# Setup common terms and degree/major spellings from your list (partial list here, add fully as needed)
common_resume_terms = [
    'python', 'java', 'c++', 'sql', 'javascript', 'html', 'css', 'aws', 'azure', 'docker', 'kubernetes',
    'machine learning', 'data analysis', 'figma', 'adobe', 'xpress' 'project management', 'agile', 'scrum', 'communication',
    'leadership', 'teamwork', 'problem solving', 'cloud computing', 'software development',
    'quality assurance', 'networking', 'linux', 'ui/ux', 'git', 'apis', 'big data', 'cybersecurity',
    'data mining', 'tableau', 'power bi', 'salesforce', 'devops', 'tensorflow', 'pytorch', 'react',
    'angular', 'node.js', 'express', 'mongodb', 'postgresql', 'mysql', 'nosql', 'html5', 'css3', 'bootstrap',
    'rest api', 'soap', 'microservices', 'analytics', 'data visualization', 'etl', 'spark', 'hadoop',
    'jenkins', 'jira', 'confluence', 'vpn', 'firewall', 'selenium', 'c', 'c#', 'perl', 'ruby', 'php',
    'swift', 'objective-c', 'matlab', 'r programming', 'scala', 'shell scripting', 'bash', 'powershell',
    'unix', 'windows server', 'active directory', 'ldap', 'vmware', 'virtualization', 'business analysis',
    'sales', 'marketing', 'customer service', 'finance', 'accounting', 'human resources', 'recruitment',
    'training', 'coaching', 'budgeting', 'strategic planning', 'risk management', 'compliance',
    'legal', 'operations', 'logistics', 'supply chain', 'procurement', 'quality control', 'continuous improvement',
    'iso', 'lean', 'six sigma', 'kanban', 'software testing', 'automation testing', 'manual testing',
    'unit testing', 'integration testing', 'regression testing', 'performance testing', 'selenium webdriver',
    'cucumber', 'jira software', 'agile methodology', 'scrum master', 'product owner', 'business intelligence',
    'sap', 'oracle', 'crm', 'erp', 'tableau desktop', 'microsoft office', 'excel', 'powerpoint',
    'word', 'outlook', 'email', 'social media', 'content management', 'seo', 'sem', 'digital marketing',
    'copywriting', 'graphic design', 'photoshop', 'illustrator', 'adobe xd', 'ux research', 'wireframing',
    'prototyping', 'java ee', 'spring framework', 'hibernate', 'microservices architecture',
    'restful services', 'json', 'xml', 'apache kafka', 'rabbitmq', 'grpc', 'grpc protocol',
    'blockchain', 'cryptocurrency', 'bitcoin', 'ethereum', 'machine learning algorithms', 'natural language processing',
    'deep learning', 'neural networks', 'computer vision', 'opencv', 'tensorflow keras', 'scikit-learn',
    'data science', 'bigquery', 'aws lambda', 'aws s3', 'google cloud platform', 'cloud functions',
    'cloud storage', 'azure functions', 'azure blob storage', 'terraform', 'ansible', 'chef', 'puppet',
    'container orchestration', 'docker swarm', 'ci/cd pipelines', 'automated deployment', 'version control',
    'gitlab', 'bitbucket', 'github', 'static code analysis', 'code review', 'pair programming',
    'agile development', 'software lifecycle', 'devsecops', 'penetration testing', 'vulnerability assessment',
    'incident response', 'forensics', 'compliance standards', 'pci-dss', 'hipaa', 'gdpr', 'iso 27001',
    'endpoint security', 'network security', 'identity management', 'multi-factor authentication', 'sso',
    'oauth', 'openID', 'security operations center', 'security audits', 'firewalls', 'intrusion detection',
    'intrusion prevention systems', 'endpoint detection and response', 'data governance', 'master data management',
    'change management', 'service management', 'itil', 'customer relationship management',
    'business process improvement', 'lean management', 'strategic sourcing', 'cost reduction',
    'inventory management', 'vendor management', 'contract negotiation', 'team leadership',
    'cross-functional team leadership', 'mentoring', 'performance management', 'employee relations',
    'talent acquisition', 'compensation and benefits', 'organizational development', 'training and development',
    'business analysis', 'requirements gathering', 'stakeholder management', 'user stories',
    'use cases', 'functional specifications', 'technical documentation', 'software development lifecycle',
    'waterfall methodology', 'continuous integration', 'continuous delivery', 'cloud architecture',
    'scalability', 'high availability', 'load balancing', 'database administration', 'backup and recovery',
    'disaster recovery', 'data warehousing', 'etl processes', 'data modeling', 'data governance',
    'data quality', 'business intelligence reporting', 'data visualization tools', 'kpi development',
    'balanced scorecard', 'dashboard creation', 'root cause analysis', 'problem resolution',
    'process mapping', 'process reengineering', 'workflow automation', 'compliance audits', 'risk assessment',
    'internal controls', 'financial analysis', 'budget analysis', 'forecasting', 'account reconciliation',
    'tax compliance', 'cost accounting', 'general ledger', 'payroll processing', 'accounts payable',
    'accounts receivable', 'vendor relations', 'customer billing', 'invoicing', 'collections',
    'cash flow management', 'financial reporting', 'gaap', 'ifrs', 'sox compliance', 'audit coordination',
    'market research', 'competitive analysis', 'product management', 'pricing strategy',
    'brand development', 'campaign management', 'event planning', 'public relations',
    'media relations', 'content marketing', 'email marketing', 'search engine optimization',
    'search engine marketing', 'social media marketing', 'pay-per-click advertising', 'lead generation',
    'customer segmentation', 'market segmentation', 'sales force automation', 'crm software',
    'sales training', 'territory management', 'account management', 'customer retention',
    'contract management', 'negotiation skills', 'presentation skills', 'proposal writing',
    'grant writing', 'budget management', 'resource allocation', 'project scheduling', 'risk mitigation',
    'vendor evaluation', 'quality management', 'health and safety', 'environmental compliance',
    'product lifecycle management', 'production planning', 'manufacturing processes', 'supply chain logistics',
    'inventory control', 'warehouse management', 'distribution management', 'transportation planning',
    'customer service management', 'help desk support', 'incident management', 'service desk',
    'technical support', 'application support', 'desktop support', 'network administration',
    'system administration', 'cloud computing platforms', 'virtualization technologies', 'server management',
    'storage management', 'backup solutions', 'disaster recovery planning', 'information security management',
    'identity and access management', 'penetration testing tools', 'firewall configuration',
    'intrusion detection systems', 'security information and event management', 'security policies',
    'security awareness training', 'compliance regulations', 'data privacy', 'encryption technologies',
    'fraud detection', 'incident response plan', 'digital forensics', 'ethical hacking', 'risk analysis',
    'business continuity planning', 'legal compliance', 'contract law', 'intellectual property',
    'corporate governance', 'policy development', 'process improvement', 'kaizen', 'six sigma black belt',
    'lean manufacturing', 'total quality management', 'continuous process improvement', 'statistical analysis',
    'experimental design', 'data collection', 'data cleaning', 'statistical software', 'research methodologies',
    'materials science',
    'architecture', 'urban planning', 'interior design', 'product design', 'graphic design',
    'fashion design', 'animation', 'film production', 'audio production', 'event management',
    'supply chain management', 'logistics management', 'operations management', 'customer relationship management',
    'public relations', 'marketing strategy', 'digital advertising', 'content creation', 'social media strategy',
    'financial planning', 'investment management', 'tax planning', 'auditing', 'accounting software',
    'human resource management', 'organizational behavior', 'labor relations', 'training and development',
    'leadership development', 'change management', 'business intelligence', 'data warehousing',
    'enterprise resource planning', 'customer analytics', 'sales forecasting', 'product lifecycle management',
    'brand management', 'market research', 'competitive analysis', 'creative writing', 'copywriting',
    'technical writing', 'editorial skills', 'translation', 'languages', 'customer support',
    'client management', 'negotiation', 'presentation', 'public speaking', 'time management',
    'critical thinking', 'decision making', 'problem solving', 'conflict resolution', 'adaptability',
    'team collaboration', 'emotional intelligence', 'work ethic', 'attention to detail', 'multitasking',
    'project coordination', 'budget management', 'vendor management', 'contract negotiation', 'risk management'
]
degree_major_spellings = [
    'b e', 'be', 'bachelors in engineering', 'bachelors of engineering',
    'm e', 'me', 'masters in engineering', 'masters of engineering',
    'm s', 'ms', 'masters in science', 'master of science', 'msc',
    'b tech', 'bachelors of technology', 'bachelors in technology',
    'm tech', 'masters of technology', 'masters in technology',
    'b s c', 'bsc', 'bachelors in science', 'bachelors of science', 'bachelor of science', 'bscs',
    'ph d', 'phd', 'doctor of philosophy', 'doctorate',
    'b a', 'ba', 'bachelors in arts', 'bachelors of arts',
    'b com', 'bcom', 'bachelors in commerce', 'bachelors of commerce',
    'b b a', 'bba', 'bachelors in business administration', 'bachelors of business administration',
    'm b a', 'mba', 'masters in business administration', 'masters of business administration',
    'cse', 'computer science', 'computer science and engineering', 'computer engineering', 'computer science & engineering',
    'cs', 'cyber security', 'cybersecurity', 'information security', 'network security', 'security engineering',
    'aiml', 'ai/ml', 'artificial intelligence and machine learning', 'artificial intelligence & machine learning', 'machine learning and ai', 'deep learning',
    'aids', 'ai/ds', 'artificial intelligence and data science', 'artificial intelligence & data science', 'machine learning and data science', 'data science and artificial intelligence',
    'ds', 'data science', 'data analytics', 'data analysis', 'big data', 'data mining',
    'ml', 'machine learning', 'deep learning', 'supervised learning', 'unsupervised learning',
    'rob', 'robotics', 'robotic engineering', 'robot automation', 'robotic systems engineering', 'robotics technology',
    'it', 'information technology', 'information tech', 'information systems', 'computer information systems',
    'csbs', 'computer science and business systems', 'computer science business systems', 'business systems and computer science', 'computer applications',
    'csd', 'computer science and design', 'computer science & design', 'computing and design', 'computer graphics and design',
    'ece', 'electrical and electronics engineering', 'electrical electronics', 'electrical and electronics', 'electrical & electronics', 'electronics and communication engineering',
    'eee', 'electrical engineering', 'electrical engg', 'electrical and electronics engineering', 'power engineering',
    'mech', 'mechanical engineering', 'mechanical engg', 'mechatronics', 'mechanical and automation engineering',
    'civil', 'civil engineering', 'civil engg', 'construction engineering', 'structural engineering',
    'automobile', 'automobile engineering', 'automobile engg', 'automotive engineering', 'automotive engg',
    'food tech', 'food technology', 'food science and technology', 'food science', 'nutrition science',
    'bio med', 'biomedical engineering', 'biomedical engg', 'medical engineering', 'biomedical sciences',
    'bio tech', 'biotechnology', 'biotech', 'molecular biology', 'genetic engineering',
    'aero', 'aerospace engineering', 'aeronautical engineering', 'aviation engineering', 'aerospace technology',
    'lit', 'literature', 'english literature', 'world literature', 'comparative literature', 'literary studies',
    'eng', 'english', 'english language', 'english literature', 'british english', 'american english',
    'eco', 'economics', 'economic studies', 'applied economics', 'macro economics', 'micro economics',
    'phy', 'physics', 'applied physics', 'theoretical physics', 'nuclear physics', 'quantum physics',
    'chem', 'chemistry', 'organic chemistry', 'inorganic chemistry', 'physical chemistry', 'analytical chemistry'
]

spell.word_frequency.load_words(common_resume_terms + degree_major_spellings)

# Degree normalization map
degree_normalization_map = {
    r'\b(b\.?e\.?|b\s*e\s*|bachelors? in engineering|bachelors? of engineering)\b': 'bachelors in engineering',
    r'\b(m\.?e\.?|m\s*e\s*|masters? in engineering|masters? of engineering|m\.?s\.?|masters? in science|master of science|msc|m\.?s)\b': 'masters in engineering',
    r'\b(b\.?tech\.?|b\s*tech\s*|bachelors? of technology|bachelors? in technology)\b': 'bachelors in technology',
    r'\b(m\.?tech\.?|m\s*tech\s*|masters? of technology|masters? in technology)\b': 'masters in technology',
    r'\b(b\.?s\.?c\.?|b\s*s\s*c\s*|bachelors? in science|bachelors? of science|bachelor of science|b\.?s\.?|bscs)\b': 'bachelor of science',
    r'\b(p\.?h\.?d\.?|p\s*h\s*d\s*|doctor of philosophy|doctorate)\b': 'phd',
    r'\b(b\.?a\.?|b\s*a\s*|bachelors? in arts|bachelors? of arts)\b': 'bachelor of arts',
    r'\b(b\.?com\.?|b\s*com\s*|bachelors? in commerce|bachelors? of commerce)\b': 'bachelor of commerce',
    r'\b(b\.?b\.?a\.?|b\s*b\s*a\s*|bachelors? in business administration|bachelors? of business administration)\b': 'bachelor of business administration',
    r'\b(m\.?b\.?a\.?|m\s*b\s*a\s*|masters? in business administration|masters? of business administration)\b': 'master of business administration',
}

# Major normalization map (partial)
major_normalization_map = {
    r'\b(cse|csee|computer science|computer science and engineering|computer engineering|computer science & engineering)\b': 'cse',
    r'\b(cs|cyber ?security|information security|network security|security engineering|cybersecurity)\b': 'cyber security',
    r'\b(aiml|ai/ml|artificial intelligence and machine learning|artificial intelligence & machine learning|machine learning and ai|deep learning)\b': 'ai/ml',
    r'\b(aids|ai/ds|artificial intelligence and data science|artificial intelligence & data science|machine learning and data science|data science and artificial intelligence)\b': 'ai/ds',
    r'\b(ds|data science|data analytics|data analysis|big data|data mining)\b': 'data science',
    r'\b(ml|machine learning|ml|deep learning|supervised learning|unsupervised learning)\b': 'machine learning',
    r'\b(rob|robotics|robotic engineering|robot automation|robotic systems engineering|robotics technology)\b': 'robotics',
    r'\b(it|information technology|information tech|information systems|computer information systems)\b': 'it',
    r'\b(csbs|computer science and business systems|computer science business systems|business systems and computer science|computer applications)\b': 'csbs',
    r'\b(csd|computer science and design|computer science & design|computing and design|computer graphics and design)\b': 'csd',
    r'\b(ece|electronics? engineering|electronics? communication|electronics? and communications?|electronics? & communications?|electronics and communications? engineering)\b': 'ece',
    r'\b(eee|electricals? engineering|electricals? engg|electricals? and electronics? engineering|power engineering)\b': 'eee',
    r'\b(mech|mechanicals?|mechanical engineering|mechanical engg|mechatronics|mechanical and automation engineering)\b': 'mech',
    r'\b(civil|civil engineering|civil engg|construction engineering|structural engineering)\b': 'civil',
    r'\b(automobile|automobile engineering|automobile engg|automotive engineering|automotive engg)\b': 'automobile',
    r'\b(food tech|food technology|food science and technology|food science|nutrition science)\b': 'food tech',
    r'\b(bio med|biomedical engineering|biomedical engg|medical engineering|biomedical sciences)\b': 'bio med',
    r'\b(bio tech|biotechnology|biotech|molecular biology|genetic engineering)\b': 'bio tech',
    r'\b(aero|aerospace engineering|aeronautical engineering|aviation engineering|aerospace technology)\b': 'aero',
    r'\b(lit|literature|english literature|world literature|comparative literature|literary studies)\b': 'literature',
    r'\b(eng|english|english language|english literature|british english|american english)\b': 'english',
    r'\b(eco|economics|economic studies|applied economics|macro economics|micro economics)\b': 'economics',
    r'\b(phy|physics|applied physics|theoretical physics|nuclear physics|quantum physics)\b': 'physics',
    r'\b(chem|chemistry|organic chemistry|inorganic chemistry|physical chemistry|analytical chemistry)\b': 'chemistry',
}

# Helper functions

def correct_spelling(text):
    corrected_words = []
    for word in text.split():
        if word.isalpha():
            corrected_word = spell.correction(word)
            corrected_words.append(corrected_word if corrected_word else word)
        else:
            corrected_words.append(word)
    return ' '.join(corrected_words)


def normalize_degree(text):
    text = text.lower().strip().replace('.', '')
    for pattern, normalized in degree_normalization_map.items():
        if re.search(pattern, text):
            return normalized
    return text

def normalize_major(text):
    text = text.lower().strip()
    for pattern, normalized in major_normalization_map.items():
        if re.search(pattern, text):
            return normalized
    return text

def normalize_qualifications(qualifications_list):
    normalized = []
    for deg, maj in qualifications_list:
        deg_corrected = correct_spelling(deg)
        maj_corrected = correct_spelling(maj)
        normalized.append((normalize_degree(deg_corrected), normalize_major(maj_corrected)))
    return normalized


def normalize_text_list(text_list):
    normalized_list = []
    for text in text_list:
        corrected = correct_spelling(text.lower().strip())
        normalized_list.append(corrected)
    return normalized_list

def semantic_similarity(list1, list2):
    # Sort both lists before joining
    text1 = ', '.join(sorted(x.strip().lower() for x in list1))
    text2 = ', '.join(sorted(x.strip().lower() for x in list2))
    embeddings = model.encode([text1, text2])
    sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return float(sim)


def qualifications_match(candidate_quals, job_quals):
    candidate_quals_norm = normalize_qualifications(candidate_quals)
    job_quals_norm = normalize_qualifications(job_quals)

    if not job_quals_norm:  # No requirements = full score
        return 1.0
    if not candidate_quals_norm:  # No candidate quals = no match
        return 0.0

    for j_deg, j_maj in job_quals_norm:
        for c_deg, c_maj in candidate_quals_norm:
            if j_maj == '' or j_maj is None:  # Major is empty in job quals, degree match enough
                if j_deg == c_deg:
                    return 1.0
            else:
                if j_deg == c_deg:
                    # Major match by empty or semantic similarity over threshold
                    if c_maj == '' or c_maj is None:
                        continue  # candidate major empty but job major required, skip
                    major_sim = semantic_similarity([c_maj], [j_maj])
                    if major_sim >= 0.7:
                        return 1.0
    # No matching degree-major pair found, no match
    return 0.0


def calculate_match_score(resume_dict, job_dict):
    WEIGHT_SKILLS = 0.5
    WEIGHT_QUALIFICATIONS = 0.2
    WEIGHT_EXPERIENCE = 0.3

    candidate_skills = resume_dict.get('skills', [])
    job_skills = job_dict.get('skills', [])
    skill_score = semantic_similarity(candidate_skills, job_skills)

    qualification_score = qualifications_match(
        resume_dict.get('qualifications', []),
        job_dict.get('qualifications', [])
    )
    required_experience = job_dict.get('experience', 0)
    candidate_experience = resume_dict.get('experience', 0)

    if required_experience == 0:
        experience_score = 1.0
    elif candidate_experience < required_experience:
        experience_score = 0.0
    else:
        experience_score = min(candidate_experience / required_experience, 1.0)

    total_score = (skill_score * WEIGHT_SKILLS) + \
                  (qualification_score * WEIGHT_QUALIFICATIONS) + \
                  (experience_score * WEIGHT_EXPERIENCE)

    return float(round(total_score, 4))


def categorize_score(score):
    if score >= 0.9:
        return 'Excellent'
    elif score >= 0.7:
        return 'Good'
    elif score >= 0.5:
        return 'Average'
    else:
        return 'Bad'


def validate_job_id_format(job_id):
    pattern = r'^[a-zA-Z]{2}\d{1,3}$'
    if not re.match(pattern, job_id):
        return False
    number_part = int(re.findall(r'\d+', job_id)[0])
    return 1 <= number_part <= 1000

def generate_candidate_id():
    attempts = 0
    max_attempts = 1000
    while attempts < max_attempts:
        letters_part = ''.join(random.choices(string.ascii_lowercase, k=2))
        number_part = str(random.randint(1, 1000))
        candidate_id = letters_part + number_part
        # Check database for uniqueness
        cur = mysql.connection.cursor()
        cur.execute("SELECT candidateid FROM candidates WHERE candidateid = %s", (candidate_id,))
        if not cur.fetchone():
            cur.close()
            return candidate_id
        cur.close()
        attempts += 1
    raise Exception("Failed to generate unique candidate ID after max attempts")



# Authentication routes
@app.errorhandler(500)
def handle_500(e):
    return jsonify({'status': 'fail', 'message': 'Internal server error.'}), 500


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
            user = cur.fetchone()
            cur.close()
            if user:
                session['user_email'] = email
                return redirect(url_for('home'))
            return render_template('login.html', error="Invalid email or password.")
        except Exception as e:
            return render_template('login.html', error=f"Database error: {str(e)}")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('login'))


@app.route('/home')
def home():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

# REST APIs with improved error handling



@app.route('/add_job', methods=['POST'])
def add_job():
    if 'user_email' not in session:
        return jsonify({'status': 'fail', 'message': 'Unauthorized'}), 401
    try:
        data = request.json
        jobid = data.get('jobid', '').strip()
        if not validate_job_id_format(jobid):
            return jsonify({'status': 'fail', 'message': 'Invalid Job ID format.'}), 400
        cur = mysql.connection.cursor()
        cur.execute("SELECT jobid FROM jobs WHERE jobid = %s", (jobid,))
        if cur.fetchone():
            cur.close()
            return jsonify({'status': 'fail', 'message': 'Job ID already exists.'}), 400

        # Normalize skills and roles list
        original_skills = data.get('skills', [])
        original_roles = data.get('role', [])
        skills_normalized = normalize_text_list(original_skills)
        roles_normalized = normalize_text_list(original_roles)

        cur.execute("INSERT INTO jobs (jobid, roles, skills, experience) VALUES (%s, %s, %s, %s)",
                    (jobid, ','.join(roles_normalized), ','.join(skills_normalized), data.get('experience', 0)))

        # Normalize qualifications before inserting
        qualifications = data.get('qualifications', [])
        for deg, maj in qualifications:
            deg_corrected = correct_spelling(deg)
            maj_corrected = correct_spelling(maj)
            deg_norm = normalize_degree(deg_corrected)
            maj_norm = normalize_major(maj_corrected)
            if deg_norm or maj_norm:
                cur.execute("INSERT INTO job_qualifications (jobid, degree, major) VALUES (%s, %s, %s)",
                            (jobid, deg_norm, maj_norm))

        mysql.connection.commit()
        cur.close()
        return jsonify({'status': 'success', 'message': 'Job added successfully.'})
    except Exception as e:
        print("Error in add_job:", e)
        return jsonify({'status': 'fail', 'message': str(e)}), 500


@app.route('/add_candidate', methods=['POST'])
def add_candidate():
    if 'user_email' not in session:
        return jsonify({'status': 'fail', 'message': 'Unauthorized'}), 401
    try:
        data = request.json
        candidateid = generate_candidate_id()
        cur = mysql.connection.cursor()

        # Normalize skills list
        original_skills = data.get('skills', [])
        skills_normalized = normalize_text_list(original_skills)

        cur.execute("INSERT INTO candidates (candidateid, skills, experience) VALUES (%s, %s, %s)",
                    (candidateid, ','.join(skills_normalized), data.get('experience', 0)))

        # Normalize qualifications before inserting
        qualifications = data.get('qualifications', [])
        normalized_qualifications = []
        for deg, maj in qualifications:
            deg_corrected = correct_spelling(deg)
            maj_corrected = correct_spelling(maj)
            deg_norm = normalize_degree(deg_corrected)
            maj_norm = normalize_major(maj_corrected)
            normalized_qualifications.append((deg_norm, maj_norm))
            if deg_norm or maj_norm:
                cur.execute("INSERT INTO candidate_qualifications (candidateid, degree, major) VALUES (%s, %s, %s)",
                            (candidateid, deg_norm, maj_norm))

        mysql.connection.commit()
        cur.close()
        return jsonify({'status': 'success', 'candidateid': candidateid})
    except Exception as e:
        print("Error in add_candidate:", e)
        return jsonify({'status': 'fail', 'message': str(e)}), 500


@app.route('/get_all_jobs')
def get_all_jobs():
    print("DEBUG /get_all_jobs called")
    if 'user_email' not in session:
        print("DEBUG Unauthorized access to /get_all_jobs")
        return jsonify({'status': 'fail', 'message': 'Unauthorized'}), 401
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM jobs")
        jobs = cur.fetchall()
        print(f"DEBUG found {len(jobs)} jobs")
        for job in jobs:
            cur.execute("SELECT degree, major FROM job_qualifications WHERE jobid = %s", (job['jobid'],))
            quals = cur.fetchall()
            job['qualifications'] = quals
        cur.close()
        return jsonify(jobs)
    except Exception as ex:
        print("ERROR in /get_all_jobs:", ex)
        return jsonify({'status': 'fail', 'message': 'Server error'}), 500



@app.route('/get_all_candidates')
def get_all_candidates():
    if 'user_email' not in session:
        return jsonify({'status': 'fail', 'message': 'Unauthorized'}), 401
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM candidates")
    candidates = cur.fetchall()
    for cand in candidates:
        cur.execute("SELECT degree, major FROM candidate_qualifications WHERE candidateid = %s", (cand['candidateid'],))
        quals = cur.fetchall()
        cand['qualifications'] = quals
    cur.close()
    return jsonify(candidates)

# Helper to build dict from job record for score calculation
def build_job_dict(job):
    # Fetch qualification records from DB dynamically if not already provided
    cur = mysql.connection.cursor()
    cur.execute("SELECT degree, major FROM job_qualifications WHERE jobid = %s", (job['jobid'],))
    quals = [(q['degree'], q['major']) for q in cur.fetchall()]
    cur.close()

    skills = job['skills'].split(',') if job['skills'] else []
    experience = int(job['experience']) if job.get('experience') else 0
    roles = job['roles'].split(',') if job['roles'] else []
    return {'qualifications': quals, 'skills': skills, 'experience': experience, 'role': roles}

# Helper to build dict from candidate record
def build_candidate_dict(candidate):
    cur = mysql.connection.cursor()
    cur.execute("SELECT degree, major FROM candidate_qualifications WHERE candidateid = %s", (candidate['candidateid'],))
    quals = [(q['degree'], q['major']) for q in cur.fetchall()]
    cur.close()

    skills = candidate['skills'].split(',') if candidate['skills'] else []
    experience = int(candidate['experience']) if candidate.get('experience') else 0
    return {'qualifications': quals, 'skills': skills, 'experience': experience}

# API to check score given jobid and candidateid
@app.route('/check_score', methods=['POST'])
def check_score():
    if 'user_email' not in session:
        return jsonify({'status': 'fail', 'message': 'Unauthorized'}), 401
    data = request.json
    jobid = data.get('jobid', '').strip()
    candidateid = data.get('candidateid', '').strip()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jobs WHERE jobid = %s", (jobid,))
    job = cur.fetchone()
    cur.execute("SELECT * FROM candidates WHERE candidateid = %s", (candidateid,))
    candidate = cur.fetchone()
    cur.close()
    if not job or not candidate:
        return jsonify({'status': 'fail', 'message': 'Job or Candidate ID not found.'}), 404
    score = calculate_match_score(build_candidate_dict(candidate), build_job_dict(job))
    tag = categorize_score(score)
    roundscore = float(round(score,4))
    return jsonify({'status': 'success', 'score': roundscore * 100, 'tag': tag})


@app.route('/find_matching_jobs', methods=['POST'])
def find_matching_jobs():
    if 'user_email' not in session:
        return jsonify({'status': 'fail', 'message': 'Unauthorized'}), 401
    candidateid = request.json.get('candidateid', '').strip()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM candidates WHERE candidateid = %s", (candidateid,))
    candidate = cur.fetchone()
    if not candidate:
        return jsonify({'status': 'fail', 'message': 'Candidate ID not found.'}), 404
    cur.execute("SELECT * FROM jobs")
    jobs = cur.fetchall()
    results = []
    for job in jobs:
        score = calculate_match_score(build_candidate_dict(candidate), build_job_dict(job))
        if score >= 0.7:
            results.append({
                'jobid': job['jobid'],
                'roles': job['roles'],
                'score': score * 100,
                'tag': categorize_score(score)
            })
    cur.close()
    return jsonify({'status': 'success', 'matches': results})


@app.route('/find_matching_candidates', methods=['POST'])
def find_matching_candidates():
    if 'user_email' not in session:
        return jsonify({'status': 'fail', 'message': 'Unauthorized'}), 401
    jobid = request.json.get('jobid', '').strip()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jobs WHERE jobid = %s", (jobid,))
    job = cur.fetchone()
    if not job:
        return jsonify({'status': 'fail', 'message': 'Job ID not found.'}), 404
    cur.execute("SELECT * FROM candidates")
    candidates = cur.fetchall()
    results = []
    for candidate in candidates:
        score = calculate_match_score(build_candidate_dict(candidate), build_job_dict(job))
        if score >= 0.7:
            results.append({
                'candidateid': candidate['candidateid'],
                'score': score * 100,
                'tag': categorize_score(score)
            })
    cur.close()
    return jsonify({'status': 'success', 'matches': results})


def init_db():
    # Connect to MySQL server without selecting a database
    import MySQLdb
    db_config = app.config
    # Create a separate connection to MySQL server without specifying database
    conn = MySQLdb.connect(
        host=db_config['MYSQL_HOST'],
        user=db_config['MYSQL_USER'],
        passwd=db_config['MYSQL_PASSWORD']
    )
    cursor = conn.cursor()
    # Create database if it does not exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['MYSQL_DB']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    conn.commit()
    cursor.close()
    conn.close()

    # Now connect using Flask-MySQLdb with the database set, create tables
    cur = mysql.connection.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    )''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        jobid VARCHAR(10) PRIMARY KEY,
        roles TEXT,
        skills TEXT,
        experience INT
    )''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS job_qualifications (
        id INT AUTO_INCREMENT PRIMARY KEY,
        jobid VARCHAR(10),
        degree VARCHAR(100),
        major VARCHAR(100),
        FOREIGN KEY (jobid) REFERENCES jobs(jobid) ON DELETE CASCADE
    )''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS candidates (
        candidateid VARCHAR(10) PRIMARY KEY,
        skills TEXT,
        experience INT
    )''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS candidate_qualifications (
        id INT AUTO_INCREMENT PRIMARY KEY,
        candidateid VARCHAR(10),
        degree VARCHAR(100),
        major VARCHAR(100),
        FOREIGN KEY (candidateid) REFERENCES candidates(candidateid) ON DELETE CASCADE
    )''')
    mysql.connection.commit()
    cur.close()

# Uncomment the line below to run init_db() on app start (run once, then comment out)

'''
with app.app_context():
    init_db()
'''

if __name__ == '__main__':
    app.run(debug=True)
