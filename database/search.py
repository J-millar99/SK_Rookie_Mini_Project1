import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from setting import create_sqlalchemy_model

# 기본 연결 설정
DATABASE_URL = "mysql+pymysql://root:maria@localhost:3306/job_data?charset=utf8mb4"
engine = create_engine(DATABASE_URL)
Base, JobPosting = create_sqlalchemy_model()
Session = sessionmaker(bind=engine)
session = Session()

# 예제 1: 전체 채용 정보 조회 (최근 10개)
def get_recent_jobs():
    jobs = session.query(JobPosting).order_by(JobPosting.id.desc()).limit(10).all()
    for job in jobs:
        print(f"ID: {job.id}, 회사: {job.company_name}, 공고: {job.job_title}, 지역: {job.region}")
    return jobs

# 예제 2: 특정 회사의 채용 정보 조회
def search_by_company(company_name):
    jobs = session.query(JobPosting).filter(JobPosting.company_name.like(f"%{company_name}%")).all()
    print(f"{company_name} 검색 결과: {len(jobs)}개 채용 정보 발견")
    for job in jobs:
        print(f"ID: {job.id}, 공고: {job.job_title}, 고용형태: {job.employment_type}, 경력: {job.experience}")
    return jobs

# 예제 3: 지역별 채용 정보 검색
def search_by_region(region):
    jobs = session.query(JobPosting).filter(JobPosting.region == region).all()
    print(f"{region} 지역 채용 정보: {len(jobs)}개")
    for job in jobs:
        print(f"회사: {job.company_name}, 공고: {job.job_title}, 하위지역: {job.sub_region}")
    return jobs

# 예제 4: 경력 조건에 따른 채용 정보 검색
def search_by_experience(exp_keyword):
    jobs = session.query(JobPosting).filter(JobPosting.experience.like(f"%{exp_keyword}%")).all()
    print(f"경력 조건 '{exp_keyword}' 관련 채용 정보: {len(jobs)}개")
    for job in jobs:
        print(f"회사: {job.company_name}, 공고: {job.job_title}, 경력: {job.experience}")
    return jobs

# 예제 5: 직군 및 고용형태별 검색
def search_by_category_and_type(category, emp_type):
    jobs = session.query(JobPosting).filter(
        JobPosting.job_category == category,
        JobPosting.employment_type == emp_type
    ).all()
    print(f"{category} 직군, {emp_type} 고용형태 채용 정보: {len(jobs)}개")
    for job in jobs:
        print(f"회사: {job.company_name}, 공고: {job.job_title}")
    return jobs

# 예제 6: 복합 조건 검색 (Raw SQL 사용) - 수정된 버전
def complex_search(region, keyword):
    sql = text("""
    SELECT company_name, job_title, url, experience, education
    FROM job_postings
    WHERE region = :region
    AND (job_title LIKE :keyword OR job_category LIKE :keyword)
    ORDER BY id DESC
    LIMIT 20
    """)
    
    with engine.connect() as conn:
        result = conn.execute(sql, {"region": region, "keyword": f"%{keyword}%"})
        
        print(f"{region} 지역, '{keyword}' 키워드 검색 결과:")
        for row in result:
            print(f"회사: {row.company_name}, 공고: {row.job_title}, 경력: {row.experience}, 학력: {row.education}")
            print(f"URL: {row.url}")
            print("-" * 50)

# 예제 7: 통계 정보 (지역별 채용 공고 수) - 수정된 버전
def get_job_stats_by_region():
    sql = text("""
    SELECT region, COUNT(*) as job_count
    FROM job_postings
    GROUP BY region
    ORDER BY job_count DESC
    """)
    
    with engine.connect() as conn:
        result = conn.execute(sql)
        
        print("지역별 채용 공고 통계:")
        for row in result:
            print(f"{row.region}: {row.job_count}개")

# 예제 8: 특정 ID의 채용 공고 상세 정보
def get_job_detail(job_id):
    job = session.query(JobPosting).filter(JobPosting.id == job_id).first()
    
    if job:
        print(f"===== 채용 공고 상세 정보 (ID: {job.id}) =====")
        print(f"회사명: {job.company_name}")
        print(f"공고명: {job.job_title}")
        print(f"고용형태: {job.employment_type}")
        print(f"경력: {job.experience}")
        print(f"학력: {job.education}")
        print(f"근무지역: {job.location} ({job.region} > {job.sub_region})")
        print(f"직군: {job.job_category} > {job.job_subcategory}")
        print(f"급여: {job.salary}")
        print(f"URL: {job.url}")
    else:
        print(f"ID {job_id}에 해당하는 채용 공고를 찾을 수 없습니다.")
    
    return job

# 메인 실행 코드
if __name__ == "__main__":
    try:
        print("\n=== 최근 채용 정보 ===")
        get_recent_jobs()
        
        print("\n=== 회사명으로 검색 ===")
        search_by_company("삼성")
        
        print("\n=== 지역으로 검색 ===")
        search_by_region("서울")
        
        print("\n=== 경력 조건으로 검색 ===")
        search_by_experience("신입")
        
        print("\n=== 직군 및 고용형태로 검색 ===")
        search_by_category_and_type("전문직·법률·인문사회·임원", "정규직")
        
        print("\n=== 복합 조건 검색 ===")
        complex_search("서울", "개발자")
        
        print("\n=== 지역별 통계 ===")
        get_job_stats_by_region()
        
        print("\n=== 채용 공고 상세 정보 ===")
        # 첫 번째 레코드의 ID를 가져와서 상세 정보 조회
        first_job_id = session.query(JobPosting.id).first()[0]
        get_job_detail(first_job_id)
        
    finally:
        session.close()