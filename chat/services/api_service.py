# services/api_service.py
import httpx

API_BASE_URL = "https://ian-as-bigdata-gca5hxdng8e8fdhu.centralus-01.azurewebsites.net/api"

class ApiService:
    @staticmethod
    async def create_student(nome: str, email: str, curso: str) -> dict:
        async with httpx.AsyncClient() as client:
            r = await client.post(f"{API_BASE_URL}/matriculas/", json={"nome": nome, "email": email, "curso": curso})
            if r.status_code in (200, 201):
                result = r.json()
                return {
                    "nome": nome,
                    "email": email,
                    "curso": curso,
                    "matricula": result.get("matricula"),
                }
            return None

    @staticmethod
    async def get_all_students() -> list:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{API_BASE_URL}/matriculas")
            return r.json() if r.status_code == 200 else []

    @staticmethod
    async def get_student_by_matricula(matricula: str) -> dict:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{API_BASE_URL}/matriculas/{matricula}")
            return r.json() if r.status_code == 200 else None
