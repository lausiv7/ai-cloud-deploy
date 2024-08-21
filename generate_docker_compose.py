import os
from jinja2 import Template

docker_compose_template = """
version: '3'
services:
  framework:
    image: {{ framework_image }}
    ports:
      - "{{ framework_port }}:{{ framework_port }}"
    environment:
      - FRAMEWORK_ENV=production
    networks:
      - rag_network

  {% for i in range(llm_count) %}
  llm{{ i+1 }}:
    image: {{ llm_image }}
    ports:
      - "{{ llm_base_port + i }}:{{ llm_base_port + i }}"
    networks:
      - rag_network
  {% endfor %}

  {% for i in range(db_count) %}
  vector_db{{ i+1 }}:
    image: {{ db_image }}
    ports:
      - "{{ db_base_port + i }}:{{ db_base_port + i }}"
    networks:
      - rag_network
  {% endfor %}

networks:
  rag_network:
    driver: bridge
"""

# 설정 변수
framework_image = "your-framework-image"
llm_image = "your-llm-image"
db_image = "your-db-image"

framework_port = 8000
llm_count = 2
llm_base_port = 8500
db_count = 2
db_base_port = 8600

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

# 각 서버로 도커 소스코드 배포 (예시 코드)
servers = ["server1", "server2", "server3"]
source_dir = "/path/to/source/code"

for server in servers:
    os.system(f"scp -r {source_dir} user@{server}:/path/to/destination/")
    print(f"코드 배포 완료: {server}")
