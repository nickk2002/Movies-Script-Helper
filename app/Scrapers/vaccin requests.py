from requests_html import HTMLSession
session = HTMLSession()
content = session.get('https://programare.vaccinare-covid.gov.ro/auth/login')
print(content.content)