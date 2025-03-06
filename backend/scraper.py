import requests
from bs4 import BeautifulSoup

STEAM_URL = "https://steamcommunity.com/market/search"

def get_cheapest_knives():
    """ Obtiene el cuchillo más barato en Steam """
    url = f"{STEAM_URL}?q=&category_730_Type%5B%5D=tag_CSGO_Type_Knife&appid=730&sort_column=price&sort_dir=asc"
    items = scrape_steam(url)
    return min(items, key=lambda x: x["price"]) if items else None

def get_cheapest_gloves():
    """ Obtiene los guantes más baratos en Steam """
    url = f"{STEAM_URL}?q=&category_730_Type%5B%5D=tag_Type_Hands&appid=730&sort_column=price&sort_dir=asc"
    items = scrape_steam(url)
    print(items)
    return min(items, key=lambda x: x["price"]) if items else None

def get_skin_price(name):
    """ Busca el precio de una skin específica en Steam """
    formatted_name = name.replace(" ", "%20").replace("|", "%7C")
    url = f"{STEAM_URL}?q={formatted_name}&appid=730"

    items = scrape_steam(url)
    print(items)
    return min(items, key=lambda x: x["price"]) if items else {"error": "Precio no encontrado"}


def scrape_steam(url):
        """Función genérica para obtener cuchillos, guantes o skins específicas"""

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"❌ Error {response.status_code} al acceder a {url}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        listings = soup.find_all("a", class_="market_listing_row_link")  # Extrae los ítems desde los <a>

        if not listings:
            print("⚠️ No se encontraron listados en Steam.")
            return []

        items = []
        for listing in listings:
            try:
                # Extraer el nombre del ítem
                name_element = listing.select_one("span.market_listing_item_name")
                name = name_element.text.strip() if name_element else "Desconocido"

                # Extraer el precio (el menor entre normal_price y sale_price)
                normal_price_element = listing.select_one("span.normal_price")
                sale_price_element = listing.select_one("span.sale_price")

                # Limpiar y convertir el precio
                def clean_price(price_element):
                    if price_element:
                        price_text = price_element.text.replace("$", "").replace(",", "").replace("USD", "").strip()
                        return float(price_text) if price_text.replace(".", "").isdigit() else None
                    return None

                normal_price = clean_price(normal_price_element)
                sale_price = clean_price(sale_price_element)

                price = min(filter(None, [normal_price, sale_price]))  # Tomar el menor precio disponible

                # Extraer enlace
                link = listing["href"]

                # Extraer imagen
                img_element = listing.select_one("img.market_listing_item_img")
                image = img_element["src"] if img_element else None

                if name and price:
                    items.append({"name": name, "price": price, "link": link, "image": image})

            except Exception as e:
                print(f"⚠️ Error procesando un artículo: {e}")

        return items
