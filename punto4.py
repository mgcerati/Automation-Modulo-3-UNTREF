import logging
import requests

BASE_URL = "https://pokeapi.co/api/v2"

logger = logging.getLogger(__name__)


# ─── Caso 1 ───────────────────────────────────────────────────────────────────
class TestCaso1:
    def test_berry_1(self):
        logger.info("GET %s/berry/1", BASE_URL)
        response = requests.get(f"{BASE_URL}/berry/1")
        logger.info("Status code: %d", response.status_code)
        assert response.status_code == 200, f"Status inesperado: {response.status_code}"
        data = response.json()

        logger.info("Verificando size == 20 (actual: %s)", data["size"])
        assert data["size"] == 20, (
            f"Se esperaba size=20, se obtuvo: {data['size']}"
        )
        logger.info("OK: size es 20")

        logger.info("Verificando soil_dryness == 15 (actual: %s)", data["soil_dryness"])
        assert data["soil_dryness"] == 15, (
            f"Se esperaba soil_dryness=15, se obtuvo: {data['soil_dryness']}"
        )
        logger.info("OK: soil_dryness es 15")

        logger.info("Verificando firmness.name == 'soft' (actual: %s)", data["firmness"]["name"])
        assert data["firmness"]["name"] == "soft", (
            f"Se esperaba firmness.name='soft', se obtuvo: '{data['firmness']['name']}'"
        )
        logger.info("OK: firmness.name es 'soft'")


# ─── Caso 2 ───────────────────────────────────────────────────────────────────
class TestCaso2:
    def test_berry_2(self):
        logger.info("GET %s/berry/1 (referencia)", BASE_URL)
        berry1 = requests.get(f"{BASE_URL}/berry/1").json()
        logger.info("Berry/1 - size: %s, soil_dryness: %s", berry1["size"], berry1["soil_dryness"])

        logger.info("GET %s/berry/2", BASE_URL)
        response = requests.get(f"{BASE_URL}/berry/2")
        logger.info("Status code: %d", response.status_code)
        assert response.status_code == 200, f"Status inesperado: {response.status_code}"
        data = response.json()
        logger.info("Berry/2 - size: %s, soil_dryness: %s, firmness: %s",
                    data["size"], data["soil_dryness"], data["firmness"]["name"])

        logger.info("Verificando firmness.name == 'super-hard' (actual: %s)", data["firmness"]["name"])
        assert data["firmness"]["name"] == "super-hard", (
            f"Se esperaba firmness.name='super-hard', se obtuvo: '{data['firmness']['name']}'"
        )
        logger.info("OK: firmness.name es 'super-hard'")

        logger.info("Verificando que berry/2 size (%s) > berry/1 size (%s)", data["size"], berry1["size"])
        assert data["size"] > berry1["size"], (
            f"Se esperaba que berry/2 size ({data['size']}) sea mayor a berry/1 size ({berry1['size']})"
        )
        logger.info("OK: berry/2 size es mayor")

        logger.info("Verificando que soil_dryness sea igual: berry/1=%s, berry/2=%s",
                    berry1["soil_dryness"], data["soil_dryness"])
        assert data["soil_dryness"] == berry1["soil_dryness"], (
            f"Se esperaba soil_dryness igual: berry/1={berry1['soil_dryness']}, berry/2={data['soil_dryness']}"
        )
        logger.info("OK: soil_dryness es igual en ambas berries")


# ─── Caso 3 ───────────────────────────────────────────────────────────────────
class TestCaso3:
    def test_pikachu(self):
        logger.info("GET %s/pokemon/pikachu/", BASE_URL)
        response = requests.get(f"{BASE_URL}/pokemon/pikachu/")
        logger.info("Status code: %d", response.status_code)
        assert response.status_code == 200, f"Status inesperado: {response.status_code}"
        data = response.json()

        exp = data["base_experience"]
        logger.info("Verificando que base_experience (%s) esté entre 10 y 1000", exp)
        assert 10 < exp < 1000, (
            f"Se esperaba base_experience entre 10 y 1000, se obtuvo: {exp}"
        )
        logger.info("OK: base_experience es %d", exp)

        tipos = [t["type"]["name"] for t in data["types"]]
        logger.info("Verificando que el tipo 'electric' esté en %s", tipos)
        assert "electric" in tipos, (
            f"Se esperaba tipo 'electric', tipos encontrados: {tipos}"
        )
        logger.info("OK: tipo 'electric' confirmado")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "--html=reporte_punto4.html", "--self-contained-html", "--log-cli-level=INFO"])