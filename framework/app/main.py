from flask import Flask, render_template
import requests

app = Flask(__name__)

# 동적으로 서비스 주소 생성
def generate_docker_services(llm_count, llm_base_port, db_count, db_base_port):
    docker_services = {}
    
    # LLM 서비스 추가
    for i in range(llm_count):
        service_name = f"llm{i+1}"
        service_url = f"http://{service_name}:{llm_base_port + i}/status"
        docker_services[service_name] = service_url

    # 벡터 DB 서비스 추가
    for i in range(db_count):
        service_name = f"vector_db{i+1}"
        service_url = f"http://{service_name}:{db_base_port + i}/status"
        docker_services[service_name] = service_url
    
    return docker_services

# 예시 값: 실제로는 이 값을 외부 설정 파일이나 환경 변수에서 가져올 수 있음
llm_count = 2
llm_base_port = 8500
db_count = 2
db_base_port = 8600

DOCKER_SERVICES = generate_docker_services(llm_count, llm_base_port, db_count, db_base_port)

@app.route('/')
def home():
    statuses = {name: check_docker_status(url) for name, url in DOCKER_SERVICES.items()}
    return render_template('status.html', statuses=statuses)

def check_docker_status(url):
    try:
        response = requests.get(url)
        return response.json()
    except requests.exceptions.RequestException:
        return {"status": "unreachable"}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
