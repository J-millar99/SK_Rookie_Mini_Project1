import json
import pymysql
from sqlalchemy import create_engine, Column, Integer, String, Text, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL 데이터베이스 생성 및 초기 설정
def setup_database():
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='maria',
        charset='utf8mb4'
    )
    
    try:
        with connection.cursor() as cursor:
            # 데이터베이스 생성
            cursor.execute("CREATE DATABASE IF NOT EXISTS job_data CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("데이터베이스 생성 완료")
            
            # 새로 생성한 데이터베이스 사용
            cursor.execute("USE job_data")
            
            # 테이블 생성 (JSON 구조에 맞게 설계)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_postings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                company_name VARCHAR(100) NOT NULL COMMENT '회사명',
                job_title VARCHAR(200) NOT NULL COMMENT '채용공고',
                url VARCHAR(500) NOT NULL COMMENT 'URL',
                employment_type VARCHAR(50) COMMENT '고용형태',
                experience VARCHAR(50) COMMENT '경력',
                location VARCHAR(100) COMMENT '근무지역',
                education VARCHAR(50) COMMENT '학력',
                salary VARCHAR(100) COMMENT '급여조건',
                job_category VARCHAR(100) COMMENT '직군',
                job_subcategory VARCHAR(100) COMMENT '하위직군',
                probation_period VARCHAR(50) COMMENT '수습기간',
                region VARCHAR(50) COMMENT '지역',
                sub_region VARCHAR(50) COMMENT '하위지역',
                work_period VARCHAR(100) COMMENT '근무기간',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            print("테이블 생성 완료")
            
            # 검색 성능을 위한 인덱스 생성
            cursor.execute("CREATE INDEX idx_company ON job_postings(company_name)")
            cursor.execute("CREATE INDEX idx_region ON job_postings(region, sub_region)")
            cursor.execute("CREATE INDEX idx_job_category ON job_postings(job_category, job_subcategory)")
            print("인덱스 생성 완료")

        # 변경사항 커밋
        connection.commit()
        
    except Exception as e:
        print(f"오류 발생: {e}")
        
    finally:
        connection.close()
        
    print("데이터베이스 초기 설정 완료")

# SQLAlchemy를 이용한 테이블 매핑
def create_sqlalchemy_model():
    Base = declarative_base()
    
    class JobPosting(Base):
        __tablename__ = 'job_postings'
        
        id = Column(Integer, primary_key=True, autoincrement=True)
        company_name = Column(String(100), nullable=False)
        job_title = Column(String(200), nullable=False)
        url = Column(String(500), nullable=False)
        employment_type = Column(String(50))
        experience = Column(String(50))
        location = Column(String(100))
        education = Column(String(50))
        salary = Column(String(100))
        job_category = Column(String(100))
        job_subcategory = Column(String(100))
        probation_period = Column(String(50))
        region = Column(String(50))
        sub_region = Column(String(50))
        work_period = Column(String(100))
        
        def __repr__(self):
            return f"<JobPosting(id={self.id}, company='{self.company_name}', title='{self.job_title}')>"
    
    return Base, JobPosting

# JSON 파일 읽기 및 데이터베이스에 저장
def import_json_to_db(json_file_path):
    # JSON 파일 읽기
    with open(json_file_path, 'r', encoding='utf-8') as file:
        job_data = json.load(file)
    
    # SQLAlchemy 설정
    DATABASE_URL = "mysql+pymysql://root:maria@localhost:3306/job_data?charset=utf8mb4"
    engine = create_engine(DATABASE_URL)
    Base, JobPosting = create_sqlalchemy_model()
    
    # 테이블 생성 (이미 존재하는 경우 무시)
    Base.metadata.create_all(engine)
    
    # 세션 생성
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # JSON 데이터를 DB에 저장
        for job in job_data:
            posting = JobPosting(
                company_name=job.get("회사명", ""),
                job_title=job.get("채용공고", ""),
                url=job.get("URL", ""),
                employment_type=job.get("고용형태", ""),
                experience=job.get("경력", ""),
                location=job.get("근무지역", ""),
                education=job.get("학력", ""),
                salary=job.get("급여조건", ""),
                job_category=job.get("직군", ""),
                job_subcategory=job.get("하위직군", ""),
                probation_period=job.get("수습기간", ""),
                region=job.get("지역", ""),
                sub_region=job.get("하위지역", ""),
                work_period=job.get("근무기간", "")
            )
            session.add(posting)
        
        session.commit()
        print(f"{len(job_data)}개의 채용 정보가 성공적으로 저장되었습니다.")
        
    except Exception as e:
        session.rollback()
        print(f"데이터 저장 중 오류 발생: {e}")
        
    finally:
        session.close()

# 메인 실행 코드
if __name__ == "__main__":
    # 1. 데이터베이스 및 테이블 생성
    setup_database()
    
    # 2. JSON 파일 가져와서 DB에 저장
    json_file_path = "../data/cleaned_data.json"  # 실제 JSON 파일 경로로 변경하세요
    import_json_to_db(json_file_path)