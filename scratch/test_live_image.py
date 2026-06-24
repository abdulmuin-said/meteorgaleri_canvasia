import urllib.request

def main():
    # Append a random query param to bypass Cloudflare cache
    url = "https://www.canvasia.com.tr/img/products/urgup-ucan-balon--1.webp?v=123456"
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response:
            print("Status Code:", response.status)
            print("Headers:", response.headers.items())
    except urllib.error.HTTPError as e:
        print("HTTP Error Code:", e.code)
        print("Headers:", e.headers.items())
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
