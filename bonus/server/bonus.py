import requests
from collections import Counter
import time
import json
import matplotlib.pyplot as plt
from datetime import datetime

def get_vacancies_by_page(page=0, per_page=100):
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": 'NAME:"Аналитик"',
        "area": 1,
        "page": page,
        "per_page": per_page,
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def collect_vacancies_data(max_vacancies=1000):
    raw_vacancies = []
    
    for page in range(0, 12):
        try:
            data = get_vacancies_by_page(page)
            vacancies = data.get("items", [])
            if not vacancies:
                break

            for vacancy in vacancies:
                if 'аналитик' not in vacancy['name'].lower():
                    continue

                try:
                    vacancy_data = requests.get(
                        f'https://api.hh.ru/vacancies/{vacancy["id"]}',
                        timeout=10
                    ).json()

                    raw_vacancy = {
                        "id": vacancy["id"],
                        "name": vacancy["name"],
                        "published_at": vacancy["published_at"],
                        "skills": [skill["name"] for skill in vacancy_data.get("key_skills", [])],
                        "experience": vacancy_data.get("experience", {}).get("name", "Не указан"),
                        "schedule": vacancy_data.get("schedule", {}).get("name", "Не указан"),
                        "salary": vacancy.get("salary"),
                        "employer": vacancy.get("employer", {}).get("name", "Не указан")
                    }
                    raw_vacancies.append(raw_vacancy)

                    if len(raw_vacancies) >= max_vacancies:
                        break

                    time.sleep(0.01)

                except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError):
                    continue

        except Exception:
            continue

        if len(raw_vacancies) >= max_vacancies:
            break

    return {
        "vacancies": raw_vacancies,
        "metadata": {
            "date_collected": datetime.now().isoformat(),
            "total_vacancies": len(raw_vacancies),
            "search_query": "Analyst",
            "area": "Moscow"
        }
    }

def normalize_skill(skill):
    skill = skill.lower().strip()
    skill_mapping = {
        "sql": "SQL",
        "excel": "Excel",
        "power bi": "Power BI",
        "python": "Python",
        "tableau": "Tableau",
        "ms excel": "Excel",
        "postgresql": "SQL",
        "mysql": "SQL",
        "1c": "1C",
        "1с": "1C",
        "data analysis": "Data Analysis",
    }
    return skill_mapping.get(skill, skill)

def prepare_visualization_data(vacancies):
    skills_counter = Counter()
    experience_counter = Counter()
    schedule_counter = Counter()
    
    for vacancy in vacancies:
        for skill in vacancy["skills"]:
            normalized_skill = normalize_skill(skill)
            skills_counter[normalized_skill] += 1
        
        experience_counter[vacancy["experience"]] += 1
        schedule_counter[vacancy["schedule"]] += 1
    
    return {
        "skills": skills_counter.most_common(15),
        "experience": experience_counter.most_common(),
        "schedule": schedule_counter.most_common()
    }

vacancies_data = collect_vacancies_data(max_vacancies=500)

if not vacancies_data["vacancies"]:
    raise Exception("Failed to collect vacancy data")

with open(f"server\data.json", "w", encoding="utf-8") as f:
    json.dump(vacancies_data, f, ensure_ascii=False, indent=2)

stats = prepare_visualization_data(vacancies_data["vacancies"])

plt.figure(figsize=(16, 12))
plt.subplot(2, 1, 1)
skills, counts = zip(*stats["skills"])
plt.barh(skills, counts, color='#4B8BBE')
plt.title("TOP 15 ANALYST SKILLS", fontsize=14)
plt.xlabel("Mentions count")
plt.gca().invert_yaxis()
plt.grid(axis='x', linestyle='--', alpha=0.6)

plt.subplot(2, 2, 3)
exp_labels, exp_counts = zip(*stats["experience"])
plt.pie(exp_counts, labels=exp_labels, autopct='%1.1f%%', 
        colors=['#4B8BBE', '#306998', '#FFD43B', '#646464'])
plt.title("WORK EXPERIENCE", fontsize=12)

plt.subplot(2, 2, 4)
schedule_labels, schedule_counts = zip(*stats["schedule"])
plt.bar(schedule_labels, schedule_counts, color='#306998')
plt.title("WORK SCHEDULE", fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig("analyst_stats.png")
plt.show()
