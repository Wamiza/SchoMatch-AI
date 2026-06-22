"""
Seed the database with sample opportunity data for demo purposes.
Run: python -m app.db.seed
"""

from __future__ import annotations

import asyncio
import logging

from app.db.database import async_session, init_db
from app.db.models import Opportunity

logger = logging.getLogger(__name__)

SEED_OPPORTUNITIES = [
    {
        "name": "Fulbright Foreign Student Program",
        "organization": "U.S. Department of State",
        "country": "United States",
        "deadline": "2026-10-15",
        "funding_status": "Fully Funded",
        "application_link": "https://foreign.fulbrightonline.org/",
        "opportunity_type": "scholarship",
        "description": "The Fulbright Program offers grants for graduate students, young professionals and artists to study, conduct research, and/or teach English abroad.",
        "eligibility_summary": "Open to citizens of participating countries. Must hold a bachelor's degree. Strong academic record and leadership potential required.",
        "degree_levels": ["master", "phd"],
        "fields_of_study": ["all"],
        "min_gpa": 3.0,
        "requirements": {"language": "English proficiency (TOEFL/IELTS)", "citizenship": "Non-US citizens", "degree": "Bachelor's degree minimum"},
        "tags": ["prestigious", "fully-funded", "usa", "graduate"],
    },
    {
        "name": "DAAD Scholarship",
        "organization": "German Academic Exchange Service",
        "country": "Germany",
        "deadline": "2026-11-15",
        "funding_status": "Fully Funded",
        "application_link": "https://www.daad.de/en/study-and-research-in-germany/scholarships/",
        "opportunity_type": "scholarship",
        "description": "DAAD offers scholarships for international students to pursue Master's and PhD programs at German universities.",
        "eligibility_summary": "Bachelor's degree completed with good grades. Some programs require German language skills.",
        "degree_levels": ["master", "phd"],
        "fields_of_study": ["engineering", "sciences", "arts", "social sciences"],
        "min_gpa": 3.0,
        "requirements": {"language": "German or English proficiency", "degree": "Bachelor's degree", "experience": "Relevant academic background"},
        "tags": ["germany", "europe", "fully-funded", "graduate"],
    },
    {
        "name": "Chevening Scholarships",
        "organization": "UK Government",
        "country": "United Kingdom",
        "deadline": "2026-11-01",
        "funding_status": "Fully Funded",
        "application_link": "https://www.chevening.org/scholarships/",
        "opportunity_type": "scholarship",
        "description": "Chevening Scholarships are the UK government's global scholarship programme, funded by the Foreign, Commonwealth and Development Office.",
        "eligibility_summary": "Must have at least 2 years of work experience. Leadership potential. Return to home country for 2 years after completion.",
        "degree_levels": ["master"],
        "fields_of_study": ["all"],
        "min_gpa": 2.8,
        "requirements": {"experience": "2+ years work experience", "language": "English proficiency", "commitment": "Return to home country"},
        "tags": ["uk", "prestigious", "fully-funded", "masters-only"],
    },
    {
        "name": "Erasmus Mundus Joint Master Degrees",
        "organization": "European Commission",
        "country": "Europe (Multiple)",
        "deadline": "2027-01-15",
        "funding_status": "Fully Funded",
        "application_link": "https://erasmus-plus.ec.europa.eu/opportunities/individuals/students/erasmus-mundus-joint-masters",
        "opportunity_type": "scholarship",
        "description": "Erasmus Mundus Joint Master Degrees are prestigious, integrated, international study programmes, jointly delivered by an international consortium of higher education institutions.",
        "eligibility_summary": "Open to students worldwide. Must hold a bachelor's degree. Selection based on academic excellence.",
        "degree_levels": ["master"],
        "fields_of_study": ["all"],
        "min_gpa": 3.0,
        "requirements": {"degree": "Bachelor's degree", "language": "English proficiency"},
        "tags": ["europe", "multi-country", "fully-funded", "prestigious"],
    },
    {
        "name": "Google Summer of Code",
        "organization": "Google",
        "country": "Remote / Global",
        "deadline": "2027-04-02",
        "funding_status": "Stipend Provided",
        "application_link": "https://summerofcode.withgoogle.com/",
        "opportunity_type": "internship",
        "description": "Google Summer of Code is a global, online program focused on bringing new contributors into open source software development.",
        "eligibility_summary": "Must be 18+ and eligible to work. Open to beginners and students. Must be new or beginner contributors to open source.",
        "degree_levels": ["bachelor", "master", "phd"],
        "fields_of_study": ["computer science", "software engineering", "information technology"],
        "min_gpa": None,
        "requirements": {"skills": "Programming proficiency", "age": "18+"},
        "tags": ["remote", "tech", "open-source", "stipend", "global"],
    },
    {
        "name": "CERN Summer Student Programme",
        "organization": "CERN",
        "country": "Switzerland",
        "deadline": "2027-01-31",
        "funding_status": "Fully Funded",
        "application_link": "https://home.cern/summer-student-programme",
        "opportunity_type": "summer_school",
        "description": "Spend the summer at CERN working with leading researchers in physics, computing, and engineering.",
        "eligibility_summary": "Undergraduate students in physics, computing, mathematics, or engineering. Must have completed at least 3 years of study.",
        "degree_levels": ["bachelor", "master"],
        "fields_of_study": ["physics", "computer science", "engineering", "mathematics"],
        "min_gpa": 3.2,
        "requirements": {"year": "3+ years completed", "field": "STEM fields", "language": "English proficiency"},
        "tags": ["switzerland", "physics", "research", "summer", "prestigious"],
    },
    {
        "name": "MIT MISTI Global Teaching Labs",
        "organization": "Massachusetts Institute of Technology",
        "country": "Multiple Countries",
        "deadline": "2026-09-30",
        "funding_status": "Partially Funded",
        "application_link": "https://misti.mit.edu/global-teaching-labs",
        "opportunity_type": "exchange",
        "description": "MIT students teach STEM subjects in high schools around the world during January term.",
        "eligibility_summary": "MIT students with strong STEM background. Teaching experience preferred.",
        "degree_levels": ["bachelor", "master"],
        "fields_of_study": ["all"],
        "min_gpa": 3.0,
        "requirements": {"enrollment": "MIT student", "skills": "Teaching ability"},
        "tags": ["teaching", "exchange", "global", "stem"],
    },
    {
        "name": "Rhodes Scholarship",
        "organization": "Rhodes Trust",
        "country": "United Kingdom",
        "deadline": "2026-10-01",
        "funding_status": "Fully Funded",
        "application_link": "https://www.rhodeshouse.ox.ac.uk/scholarships/",
        "opportunity_type": "fellowship",
        "description": "The Rhodes Scholarship is the oldest and most prestigious international scholarship, enabling outstanding young people to study at the University of Oxford.",
        "eligibility_summary": "Age 19-25 at time of application. Outstanding academic achievement. Leadership and commitment to service.",
        "degree_levels": ["master", "phd"],
        "fields_of_study": ["all"],
        "min_gpa": 3.7,
        "requirements": {"age": "19-25", "academics": "Outstanding record", "leadership": "Demonstrated leadership"},
        "tags": ["oxford", "uk", "prestigious", "fully-funded", "fellowship"],
    },
    {
        "name": "MITACS Globalink Research Internship",
        "organization": "MITACS",
        "country": "Canada",
        "deadline": "2026-09-15",
        "funding_status": "Fully Funded",
        "application_link": "https://www.mitacs.ca/en/programs/globalink/globalink-research-internship",
        "opportunity_type": "research",
        "description": "A competitive initiative for international undergraduates to participate in 12-week research internships at Canadian universities.",
        "eligibility_summary": "Undergraduate students from eligible countries with strong academic records in STEM or social sciences.",
        "degree_levels": ["bachelor"],
        "fields_of_study": ["sciences", "engineering", "social sciences", "humanities"],
        "min_gpa": 3.2,
        "requirements": {"level": "Undergraduate", "country": "Eligible partner countries", "gpa": "Above average"},
        "tags": ["canada", "research", "undergraduate", "summer", "fully-funded"],
    },
    {
        "name": "Schwarzman Scholars Program",
        "organization": "Schwarzman Scholars",
        "country": "China",
        "deadline": "2026-09-15",
        "funding_status": "Fully Funded",
        "application_link": "https://www.schwarzmanscholars.org/",
        "opportunity_type": "fellowship",
        "description": "A highly selective master's program at Tsinghua University in Beijing designed to prepare future leaders for a world in which China plays a major role.",
        "eligibility_summary": "Age 18-28. Bachelor's degree required. Strong leadership record and global perspective.",
        "degree_levels": ["master"],
        "fields_of_study": ["public policy", "economics", "business", "international relations"],
        "min_gpa": 3.5,
        "requirements": {"age": "18-28", "degree": "Bachelor's", "language": "English proficiency"},
        "tags": ["china", "leadership", "fully-funded", "prestigious", "masters"],
    },
    {
        "name": "Japanese Government (MEXT) Scholarship",
        "organization": "Ministry of Education, Japan",
        "country": "Japan",
        "deadline": "2027-04-30",
        "funding_status": "Fully Funded",
        "application_link": "https://www.studyinjapan.go.jp/en/smap-stopj-applications-702.html",
        "opportunity_type": "scholarship",
        "description": "The Japanese Government (MEXT) Scholarship offers international students the opportunity to study at Japanese universities with full financial support.",
        "eligibility_summary": "Under 35 years old for research students. Strong academic record. Willingness to learn Japanese.",
        "degree_levels": ["bachelor", "master", "phd"],
        "fields_of_study": ["all"],
        "min_gpa": 2.8,
        "requirements": {"age": "Under 35 for research", "nationality": "Non-Japanese", "health": "Good health"},
        "tags": ["japan", "asia", "fully-funded", "all-levels"],
    },
    {
        "name": "Australian Government Research Training Program",
        "organization": "Australian Government",
        "country": "Australia",
        "deadline": "2026-08-31",
        "funding_status": "Fully Funded",
        "application_link": "https://www.education.gov.au/research-training-program",
        "opportunity_type": "research",
        "description": "The RTP provides block grants to higher education providers to support both domestic and overseas students undertaking research doctorate and research master's degrees.",
        "eligibility_summary": "Enrolled or enrolling in a research higher degree. Strong academic and research track record.",
        "degree_levels": ["master", "phd"],
        "fields_of_study": ["all"],
        "min_gpa": 3.3,
        "requirements": {"degree": "Research degree enrollment", "research": "Demonstrated research capability"},
        "tags": ["australia", "research", "phd", "fully-funded"],
    },
    {
        "name": "Swiss Government Excellence Scholarships",
        "organization": "Swiss Confederation",
        "country": "Switzerland",
        "deadline": "2026-12-01",
        "funding_status": "Fully Funded",
        "application_link": "https://www.sbfi.admin.ch/sbfi/en/home/education/scholarships-and-grants/swiss-government-excellence-scholarships.html",
        "opportunity_type": "scholarship",
        "description": "The Swiss Government Excellence Scholarships provide postgraduate researchers with the opportunity to pursue research or further studies at a Swiss university.",
        "eligibility_summary": "Master's degree holders for PhD. PhD holders for postdoc. Under 35 years old.",
        "degree_levels": ["phd"],
        "fields_of_study": ["all"],
        "min_gpa": 3.5,
        "requirements": {"degree": "Master's minimum", "age": "Under 35", "research": "Research proposal required"},
        "tags": ["switzerland", "europe", "research", "fully-funded", "phd"],
    },
    {
        "name": "Microsoft Research Internship",
        "organization": "Microsoft",
        "country": "United States",
        "deadline": "Rolling",
        "funding_status": "Paid",
        "application_link": "https://www.microsoft.com/en-us/research/academic-program/research-internship/",
        "opportunity_type": "internship",
        "description": "Research internships at Microsoft Research for PhD students and exceptional Master's students in computer science and related fields.",
        "eligibility_summary": "Currently enrolled in PhD or exceptional Master's program in CS, AI, ML, or related fields.",
        "degree_levels": ["master", "phd"],
        "fields_of_study": ["computer science", "artificial intelligence", "machine learning"],
        "min_gpa": 3.5,
        "requirements": {"enrollment": "Graduate student", "field": "CS/AI/ML", "skills": "Research publications preferred"},
        "tags": ["usa", "tech", "research", "paid", "ai-ml"],
    },
    {
        "name": "Korea Foundation Global e-School Program",
        "organization": "Korea Foundation",
        "country": "South Korea",
        "deadline": "2027-03-01",
        "funding_status": "Fully Funded",
        "application_link": "https://www.kf.or.kr/",
        "opportunity_type": "exchange",
        "description": "An online education program providing Korean studies courses taught by professors from leading Korean universities to students worldwide.",
        "eligibility_summary": "University students interested in Korean studies. No Korean language requirement for most courses.",
        "degree_levels": ["bachelor", "master"],
        "fields_of_study": ["korean studies", "international relations", "asian studies", "humanities"],
        "min_gpa": 2.5,
        "requirements": {"enrollment": "University student", "interest": "Korean studies"},
        "tags": ["korea", "online", "exchange", "cultural-studies"],
    },
]


async def seed_database():
    """Insert seed opportunities into the database."""
    await init_db()
    
    async with async_session() as session:
        # Check if data already exists
        from sqlalchemy import select, func
        result = await session.execute(select(func.count(Opportunity.id)))
        count = result.scalar()
        
        if count > 0:
            logger.info(f"Database already has {count} opportunities. Skipping seed.")
            return

        for data in SEED_OPPORTUNITIES:
            opp = Opportunity(**data)
            session.add(opp)
        
        await session.commit()
        logger.info(f"✅ Seeded {len(SEED_OPPORTUNITIES)} opportunities into the database.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(seed_database())
