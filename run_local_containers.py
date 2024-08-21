import os
from jinja2 import Template

# docker-compose.yml 템플릿
docker_compose_template = """
services:
  framework:
    image: valid-framework-image
    ports:
      - "{{ framework_port }}:{{ framework_port }}"
    environment:
      - FRAMEWORK_ENV=production
    networks:
      - rag_network

  {% for i in range(llm_count) %}
  llm{{ i+1 }}:
    image: valid-llm-image
    ports:
      - "{{ llm_base_port + i }}:{{ llm_base_port + i }}"
    networks:
      - rag_network
  {% endfor %}

  {% for i in range(db_count) %}
  vector_db{{ i+1 }}:
    image: valid-db-image
    ports:
      - "{{ db_base_port + i }}:{{ db_base_port + i }}"
    networks:
      - rag_network
  {% endfor %}

networks:
  rag_network:
    driver: bridge
"""

# 설정 변수 (로컬 환경)
framework_image = "valid-framework-image"  # 프레임워크 도커 이미지
llm_image = "valid-llm-image"              # LLM 도커 이미지
db_image = "valid-db-image"                # 벡터 DB 도커 이미지

framework_port = 8000                     # 프레임워크 포트
llm_count = 2                             # LLM 컨테이너 개수
llm_base_port = 8500                      # LLM 포트 시작 번호
db_count = 2                              # DB 컨테이너 개수
db_base_port = 8600                       # DB 포트 시작 번호

# Jinja2를 사용하여 docker-compose.yml 파일 생성
template = Template(docker_compose_template)
docker_compose_content = template.render(
    framework_image=framework_image,
    framework_port=framework_port,
    llm_image=llm_image,
    llm_count=llm_count,
    llm_base_port=llm_base_port,
    db_image=db_image,
    db_count=db_count,
    db_base_port=db_base_port
)

# docker-compose.yml 파일 쓰기
with open("docker-compose.yml", "w") as f:
    f.write(docker_compose_content)

print("docker-compose.yml 생성 완료")

# 도커 컨테이너 실행
os.system("docker-compose up -d")

print("모든 컨테이너가 로컬에서 실행 중입니다.")
