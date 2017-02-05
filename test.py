# Демонстрация запроса
import json
import main

if __name__ == "__main__":
    god_name = "Example"
    print(json.dumps(main.api_request(god_name), intend=2, ensure_ascii=False))