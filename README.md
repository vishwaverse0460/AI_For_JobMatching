# 🤖 AI for Job Matching (ML-Powered)

This project is a **scalable Flask-based job matching system enhanced with Machine Learning and NLP** to intelligently match candidates with job roles. It leverages semantic similarity, structured data processing, and ML-based scoring to provide realistic and dynamic recommendations.

Built with a clean modular architecture, the system supports **multi-user environments**, **ML-driven decision making**, and **realistic hiring simulations**.

---

## ✨ Features

### 🧠 ML-Powered Matching (NEW 🔥)

- **Machine Learning-Based Scoring**: Replaces fixed weights with a **Random Forest regression model** trained on structured synthetic data.
- **Feature-Based Prediction**:
  - Skill similarity (NLP-based)
  - Experience match (normalized)
  - Qualification match
- Produces **dynamic and realistic match scores**

---

### 🎯 Core Functionality

- **Candidate–Job Match Check**: Computes ML-based match score for a given candidate and job.
- **Job Recommendations for Candidates**: Lists jobs matching a candidate above threshold (≥70%).
- **Candidate Recommendations for Jobs**: Lists candidates matching job requirements.
- **End-to-End Matching Pipeline**:

Candidate + Job → Feature Extraction → ML Model → Match Score → Recommendation

---

### 🔍 NLP & Data Processing

- **Semantic Matching**: Uses SentenceTransformer embeddings + cosine similarity for skill comparison.
- **Normalization & Cleaning**:
- Spell correction (pyspellchecker)
- Regex-based normalization for skills, degrees, majors
- Handles **noisy real-world input data**

---

### ⚙️ Improved Scoring Logic (NEW)

- **Smooth Experience Normalization**:
- Replaces hard cutoffs with proportional scoring
- **Realistic Dataset Simulation**:
- Structured synthetic data (strong / medium / weak matches)
- Noise added for better ML generalization

---

### 🔐 Multi-User System (NEW)

- Session-based authentication
- Data isolation using `user_email`
- Users can:
- Add their own jobs
- Add their own candidates
- View only their own data

---

### 🗄️ Database Enhancements (NEW)

- Auto-increment primary key (`id`)
- Composite uniqueness:

(jobid, user_email)

- Eliminates cross-user conflicts
- Clean relational structure with foreign keys

---

### 📊 Match Categories

- **Excellent**: ≥90%
- **Good**: ≥70%
- **Average**: ≥50%
- **Bad**: <50%

_(Now derived from ML-based scoring instead of fixed logic)_

---

## 📁 Project Structure

project-root/
├── app.py
├── purePython/
│ └── ml_score_model.py # ML model (Random Forest)
├── templates/
│ ├── home.html
│ └── login.html
├── static/
│ └── login_design.jpg

---

## 📱 Screenshots

![img](https://github.com/user-attachments/assets/da9a573e-2427-4a8d-980d-21c0a0c78e1f)

![img](https://github.com/user-attachments/assets/d70b1c95-a5bb-41f7-b855-bed65591f1b4)

![img](https://github.com/user-attachments/assets/f3b2f8eb-dd0d-4c6f-8424-255248c30607)

![img](https://github.com/user-attachments/assets/03c0a06e-8412-4743-bbb8-e8a5563b254e)

![img](https://github.com/user-attachments/assets/eefaf40b-019e-4282-ae83-a44544d39986)

![img](https://github.com/user-attachments/assets/4a4da646-da1c-4576-966e-d7eafa9f2235)

![img](https://github.com/user-attachments/assets/b5a1e353-4025-497c-9ded-3c01fa4d61b0)

![img](https://github.com/user-attachments/assets/1db635e7-5c16-4318-bb8e-85f4aac07234)

![img](https://github.com/user-attachments/assets/f33cd51a-ccfe-42d0-9e94-e64720382800)

---

## 🛠️ Tech Stack

- **Frontend** : HTML templates
- **Backend** : Flask, Flask-MySQLdb
- **Database** : MySQL (job_matching_db)
- **Machine Learning** : Random Forest (scikit-learn)
- **NLP** : SentenceTransformers, cosine similarity
- **Text Processing** : regex, pyspellchecker
- **Others** : NumPy, REST APIs

---

## 📊 Database Structure

### Database: `job_matching_db`

#### Table: `users`

| Field    | Type         | Null | Key | Extra          |
| -------- | ------------ | ---- | --- | -------------- |
| id       | int          | NO   | PRI | auto_increment |
| email    | varchar(255) | NO   | UNI |                |
| password | varchar(255) | NO   |     |                |

### Table: `jobs`

| Field      | Type         | Key | Extra          |
| ---------- | ------------ | --- | -------------- |
| id         | int          | PRI | auto_increment |
| jobid      | varchar(10)  | UNI |                |
| roles      | text         |     |                |
| skills     | text         |     |                |
| experience | int          |     |                |
| user_email | varchar(255) | UNI |                |

👉 Unique Constraint:

(jobid, user_email)

#### Table: `job_qualifications`

| Field  | Type         | Null | Key | Extra          |
| ------ | ------------ | ---- | --- | -------------- |
| id     | int          | NO   | PRI | auto_increment |
| jobid  | varchar(10)  | YES  | MUL |                |
| degree | varchar(100) | YES  |     |                |
| major  | varchar(100) | YES  |     |                |

### Table: `candidates`

| Field       | Type         | Key |
| ----------- | ------------ | --- |
| candidateid | varchar(10)  | PRI |
| skills      | text         |     |
| experience  | int          |     |
| user_email  | varchar(255) |     |

#### Table: `candidate_qualifications`

| Field       | Type         | Null | Key | Extra          |
| ----------- | ------------ | ---- | --- | -------------- |
| id          | int          | NO   | PRI | auto_increment |
| candidateid | varchar(10)  | YES  | MUL |                |
| degree      | varchar(100) | YES  |     |                |
| major       | varchar(100) | YES  |     |                |

---

## 🚀 API Endpoints

- **POST /add_job**  
  Add a job with ML-ready normalized data (user-specific)

- **POST /add_candidate**  
  Add candidate profile with normalization and ML integration

- **GET /get_all_jobs**  
  Retrieve jobs filtered by logged-in user

- **GET /get_all_candidates**  
  Retrieve candidates filtered by user

- **POST /check_score**  
  Compute ML-based match score + category

- **POST /find_matching_jobs**  
  Return jobs with high ML match score

- **POST /find_matching_candidates**  
  Return candidates matching a job

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

---
