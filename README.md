# 🤖 AI for Job Matching

This project is a scalable Flask-based job matching system using basic NLP, cosine similarity on text embeddings, regex-based normalization, and rule-based logic to align candidates with suitable job roles. It exposes RESTful APIs and uses a MySQL backend to support matching, search, and explainable scoring.

## ✨ Features

### Core Functionality
- **Candidate–Job Match Check**: Determines whether a given candidate’s resume matches a specific job description and returns a numeric match score.
- **Job Recommendations for Candidates**: Lists all jobs that a given candidate matches above a threshold (default ≥70%).
- **Candidate Recommendations for Jobs**: Lists all candidates that satisfy the requirements of a given job description (default ≥70%).
***
- **Semantic Job Matching**: Uses SentenceTransformer embeddings and cosine similarity to compare candidate and job skills/qualifications.
- **Normalization & Cleaning**: Regex-based normalization and spell correction for degrees, majors, and skills to handle noisy text.
- **Explainable Scoring**: Weighted scoring model (Skills 50%, Qualifications 20%, Experience 30%) with clear categories.

**Match Categories**
- **Excellent**: ≥90%  
- **Good**: ≥70%  
- **Average**: ≥50%  
- **Bad**: <50%  

**Authentication**
- Session-based login system for authorized access to the web UI and APIs.

---

## 📁 Project Structure
```
project-root/
├── app.py
├── static/
│ └── login_design.jpg
├── templates/
  └── home.html
  └── login.html
```

---

## 📱 Screenshots


---

## 🛠️ Tech Stack
- **Frontend** : HTML templates (login, home)
- **Backend** : Flask, Flask-MySQLdb
- **Database** : MySQL (job_matching_db)
- **NLP** : SentenceTransformers (all-MiniLM-L6-v2), scikit-learn (cosine_similarity), regex, pyspellchecker
- **Others** : NumPy, RESTful JSON APIs

---

## 📊 Database Structure

### Database: `job_matching_db`

#### Table: `users`

| Field    | Type         | Null | Key | Extra          |
|----------|--------------|------|-----|----------------|
| id       | int          | NO   | PRI | auto_increment |
| email    | varchar(255) | NO   | UNI |                |
| password | varchar(255) | NO   |     |                |

#### Table: `jobs`

| Field      | Type        | Null | Key | Extra |
|------------|-------------|------|-----|-------|
| jobid      | varchar(10) | NO   | PRI |       |
| roles      | text        | YES  |     |       |
| skills     | text        | YES  |     |       |
| experience | int         | YES  |     |       |

#### Table: `job_qualifications`

| Field  | Type         | Null | Key | Extra          |
|--------|--------------|------|-----|----------------|
| id     | int          | NO   | PRI | auto_increment |
| jobid  | varchar(10)  | YES  | MUL |                |
| degree | varchar(100) | YES  |     |                |
| major  | varchar(100) | YES  |     |                |

#### Table: `candidates`

| Field       | Type        | Null | Key | Extra |
|-------------|-------------|------|-----|-------|
| candidateid | varchar(10) | NO   | PRI |       |
| skills      | text        | YES  |     |       |
| experience  | int         | YES  |     |       |

#### Table: `candidate_qualifications`

| Field       | Type         | Null | Key | Extra          |
|-------------|--------------|------|-----|----------------|
| id          | int          | NO   | PRI | auto_increment |
| candidateid | varchar(10)  | YES  | MUL |                |
| degree      | varchar(100) | YES  |     |                |
| major       | varchar(100) | YES  |     |                |

---

## 🚀 API Endpoints


POST /add_job
- Add a job with roles, skills, experience, and qualifications.

POST /add_candidate
- Add a candidate profile; generates a unique candidate ID.

GET /get_all_jobs
- Retrieve all jobs with their qualifications.

GET /get_all_candidates
- Retrieve all candidates with their qualifications.

POST /check_score
- Compute match score and label for a single job–candidate pair.

POST /find_matching_jobs
- Return all jobs where the candidate’s match score ≥70%.

POST /find_matching_candidates
- Return all candidates where the job’s match score ≥70%.
---

## 🏗️ Setup and Run

### Install dependencies

```
pip install flask flask-mysqldb sentence-transformers scikit-learn pyspellchecker numpy
```

### Configure MySQL

Ensure MySQL is running, then in `app.py`:

-Update config: MYSQL_HOST, USER, PASSWORD, DB=job_matching_db
```
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_mysql_user'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'job_matching_db'
```

The database and tables can be auto-created on first run using the initialization code:

-Uncomment the `init_db()` call in `app.py` for the first run, then comment it out again after the schema is created.

### Run the application

```
python app.py
```

### Access the web UI

```
http://localhost:5000
```

-Login credentials can be managed via the `users` table.
***
