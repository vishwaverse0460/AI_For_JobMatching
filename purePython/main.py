from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import random
import string
import re
from tabulate import tabulate
from rich import print
from spellchecker import SpellChecker


# Initialize spell checker (English)
spell = SpellChecker()


common_resume_terms = [
    'python', 'java', 'c++', 'sql', 'javascript', 'html', 'css', 'aws', 'azure', 'docker', 'kubernetes',
    'machine learning', 'data analysis', 'project management', 'agile', 'scrum', 'communication',
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


def correct_spelling(text):
    corrected_words = []
    for word in text.split():
        if word.isalpha():
            corrected_word = spell.correction(word)
            corrected_words.append(corrected_word if corrected_word else word)
        else:
            corrected_words.append(word)
    return ' '.join(corrected_words)


jobdescriptions = []
candidateresumes = []
candidateidlist = []

model = SentenceTransformer('all-MiniLM-L6-v2')


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


def normalize_degree(text):
    text = text.lower().strip().replace('.', '')
    for pattern, normalized in degree_normalization_map.items():
        if re.search(pattern, text):
            return normalized
    return text


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


def qualifications_match(candidate_quals, job_quals):
    candidate_quals_norm = normalize_qualifications(candidate_quals)
    job_quals_norm = normalize_qualifications(job_quals)

    for j_deg, j_maj in job_quals_norm:
        for c_deg, c_maj in candidate_quals_norm:
            if j_deg == c_deg:
                if j_maj == '':
                    return 1
                if c_maj == '':
                    continue
                major_sim = semantic_similarity([c_maj], [j_maj])
                if major_sim >= 0.7:
                    return 1
    return 0


def semantic_similarity(list1, list2):
    text1 = ', '.join(x.strip().lower() for x in list1)
    text2 = ', '.join(x.strip().lower() for x in list2)
    embeddings = model.encode([text1, text2])
    sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return sim


def calculate_match_score(resume_dict, job_dict):
    WEIGHT_SKILLS = 0.5
    WEIGHT_QUALIFICATIONS = 0.2
    WEIGHT_EXPERIENCE = 0.3

    # Correct spelling of skills before comparison
    candidate_skills_corrected = [correct_spelling(skill) for skill in resume_dict.get('skills', [])]
    job_skills_corrected = [correct_spelling(skill) for skill in job_dict.get('skills', [])]

    skill_score = semantic_similarity(candidate_skills_corrected, job_skills_corrected)
    qualification_score = qualifications_match(resume_dict.get('qualifications', []), job_dict.get('qualifications', []))

    required_experience = job_dict.get('experience', 0)
    candidate_experience = resume_dict.get('experience', 0)

    if required_experience == 0:
        experience_score = 1.0
    else:
        experience_score = min(candidate_experience / required_experience, 1.0)
        if candidate_experience < required_experience:
            experience_score = 0

    total_score = (skill_score * WEIGHT_SKILLS) + (qualification_score * WEIGHT_QUALIFICATIONS) + (experience_score * WEIGHT_EXPERIENCE)
    return round(total_score, 4)


def categorize_score(score):
    if score >= 0.8:
        return 'Excellent'
    elif score >= 0.6:
        return 'Good'
    elif score >= 0.4:
        return 'Average'
    else:
        return 'Bad'


def validate_job_id_format(job_id):
    pattern = r'^[a-zA-Z]{2}\d{1,3}$'  # 2 letters + 1 to 3 digits
    if not re.match(pattern, job_id):
        return False
    # Check number part range
    number_part = int(re.findall(r'\d+', job_id)[0])
    if 1 <= number_part <= 1000:
        return True
    return False

def input_job_description():
    print("JOB DESCRIPTION - ")
    job = {}
    while True:
        job_id = input("Enter Job ID (format: 2 letters followed by number 1-1000, e.g., ab123): ").strip()
        if not validate_job_id_format(job_id):
            print("Invalid Job ID format. Must be 2 letters followed by a number 1 to 1000.")
            continue
        if any(j['jobid'] == job_id for j in jobdescriptions):
            print("This Job ID already exists. Please enter a unique Job ID.")
            continue
        break
    job['jobid'] = job_id

    job_role_raw = input("Enter the job role/title(s) (comma separated): ").strip().lower().split(',')
    job['role'] = [role.strip() for role in job_role_raw if role.strip()]

    job_skills_raw = input("Enter required skills (comma separated): ").strip().lower().split(',')
    job['skills'] = [skill.strip() for skill in job_skills_raw if skill.strip()]

    qualifications = []
    count = 1
    print("ENTER QUALIFICATION DETAILS:-\n")
    while True:
        print(f"\nQUALIFICATION {count}:")
        degree_input = input(" Enter degree: ").strip()
        major_input = input(" Enter major (leave blank if any domain field eligible): ").strip()
        qualifications.append((degree_input, major_input))
        more = input("Do you want to add another qualification? (y/n): ").strip().lower()
        if more != 'y':
            break
        count += 1
    job['qualifications'] = qualifications
    while True:
        try:
            job['experience'] = int(input("Enter minimum years of experience: ").strip())
            break
        except ValueError:
            print("Please enter a valid number.")
    return job


def generate_candidate_id(max_attempts=1000):
    attempts = 0
    while attempts < max_attempts:
        letters_part = ''.join(random.choices(string.ascii_lowercase, k=2))
        number_part = str(random.randint(1, 1000))
        candidate_id = letters_part + number_part
        if candidate_id not in candidateidlist:
            candidateidlist.append(candidate_id)
            return candidate_id
        attempts += 1
    raise Exception("Failed to generate unique candidate ID after max attempts")


def input_candidate_resume():
    print("CANDIDATE RESUME DETAILS - ")
    candidate = {}
    candidate['candidateid'] = generate_candidate_id()
    candidate_skills_raw = input("Enter candidate skills (comma separated): ").strip().lower().split(',')
    candidate['skills'] = [skill.strip() for skill in candidate_skills_raw if skill.strip()]
    qualifications = []
    count = 1
    print("ENTER QUALIFICATION DETAILS:-\n")
    while True:
        print(f"\nQUALIFICATION {count}:")
        degree_input = input(" Enter degree: ").strip()
        while True:
            major_input = input(" Enter major: ").strip()
            if major_input:
                break
            else:
                print("Major is mandatory. Please enter a value.")
        qualifications.append((degree_input, major_input))
        more = input("Do you want to add another qualification? (y/n): ").strip().lower()
        if more != 'y':
            break
        count += 1
    candidate['qualifications'] = qualifications
    while True:
        try:
            candidate['experience'] = int(input("Enter candidate years of experience: ").strip())
            break
        except ValueError:
            print("Please enter a valid number.")
    return candidate

#feature 1
def validate_resume_x_job(current_resume, current_job):
    score = calculate_match_score(current_resume, current_job)
    tag = categorize_score(score)

    roles = current_job.get('role', [])
    roles_str = ', '.join(roles) if roles else 'No role specified'

    print(f"Job role(s): {roles_str} | Resume matches Job with score {score*100:.2f}%, Remarks: {tag}")


#feature 2
def candidate_check_jobs_by_id():
    candidate_id = input("Enter Candidate ID to find matching jobs: ").strip()
    candidate = next((c for c in candidateresumes if c['candidateid'] == candidate_id), None)
    if not candidate:
        print("Candidate ID not found.")
        return
    matches = []
    for job in jobdescriptions:
        score = calculate_match_score(candidate, job)
        tag = categorize_score(score)

        roles = job.get('role', [])
        roles_str = ', '.join(roles) if roles else 'No role specified'

        print(f"Job role :- {roles_str} | Job id - {job.get('jobid')} | match score: {score*100:.2f}%, Remarks: {tag}")
        if score >= 0.6:
            matches.append((job.get('jobid'), roles_str, score * 100, tag))
    if matches:
        print(f"Suggested matching jobs for Candidate ID - {candidate_id}:")
        for match in matches:
            print(match)
    else:
        print("No matching jobs found.")



#feature 3
def hr_check_candidates_by_id():
    job_id = input("Enter Job ID to find matching candidates: ").strip()
    job = next((j for j in jobdescriptions if j['jobid'] == job_id), None)
    if not job:
        print("Job ID not found.")
        return
    
    matches = []
    for candidate in candidateresumes:
        score = calculate_match_score(candidate, job)
        tag = categorize_score(score)
        print(f"Candidate {candidate.get('candidateid')} match score: {score*100:.2f}%, Remarks: {tag}")
        if score >= 0.6:
            matches.append((candidate.get('candidateid'), score * 100, tag))
    if matches:
        print(f"Suggested matching candidates for Job ID - {job_id}:")
        for match in matches:
            print(match)
    else:
        print("No matching candidates found.")


def main():
    while True:
        print("\nOptions")
        print("1. Input new Job Description (HR)")
        print("2. Input Candidate Resume")
        print("3. Validate Current Resume against Current Job")
        print("4. Candidate Find matching jobs")
        print("5. HR Find matching candidates")
        print("6. View job descriptions")
        print("7. View candidate resumes")
        print("8. Exit")
        

        choice = input("Enter choice: ").strip()

        if choice == '1':
            job = input_job_description()
            jobdescriptions.append(job)

        elif choice == '2':
            candidate = input_candidate_resume()
            candidateresumes.append(candidate)

        elif choice == '3':
            if len(candidateresumes) == 0 or len(jobdescriptions) == 0:
                print("No candidate resume or job description present in the database.")
            else:
                validate_resume_x_job(candidateresumes[-1], jobdescriptions[-1])

        elif choice == '4':
            if len(jobdescriptions) == 0:
                print("No job descriptions available to check!")
            else:
                candidate_check_jobs_by_id()

        elif choice == '5':
            if len(candidateresumes) == 0:
                print("No candidate details available to check!")
            else:
                hr_check_candidates_by_id()

        elif choice == '6':
            if jobdescriptions:
                for i in jobdescriptions:
                    print(i)
            else:
                print("No job descriptions present.")

        elif choice == '7':
            if candidateresumes:
                for i in candidateresumes:
                    print(i)
            else:
                print("No candidate resumes present.")
        
        elif choice == '8':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == '__main__':
    main()
