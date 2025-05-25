from mcp.server.fastmcp import FastMCP
import requests
import pycountry

mcp = FastMCP("nationality-predictor-mcp")

def get_country_name(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return code

@mcp.tool()
async def get_nationality(name: str) -> dict:
    """
    Verilen isme göre kişinin en olası milliyetlerini tahmin eder.
    """
    url = f"https://api.nationalize.io/?name={name}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "API isteği başarısız oldu."}

    data = response.json()
    countries = data.get("country", [])
    
    result = []
    for c in countries:
        code = c["country_id"]
        country = get_country_name(code)
        probability = round(c["probability"] * 100, 2)
        result.append({
            "ülke": country,
            "olasılık (%)": probability
        })

    return {
        "isim": data["name"],
        "tahminler": result
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
