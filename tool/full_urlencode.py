def custom_url_encode(url):
    encoded_url = ''
    for char in url:
        encoded_url += '%' + '{:02X}'.format(ord(char))
    return encoded_url

# URL to encode
url = "https://example.com"

# Encoding the URL
encoded_url = custom_url_encode(url)

print("Encoded URL:", encoded_url)
