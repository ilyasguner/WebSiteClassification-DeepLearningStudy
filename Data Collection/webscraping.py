import tarfile
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
#import time

# .tar dosyasının yolu
file_path = 'bl.tar'
domains_file = ''  # folder containing domain names path
output_file = 'website_features_shopping.csv'  # Sonuçların kaydedileceği dosya oluşturmaya gerek yok yoksa kod kendisi oluşturuyor

# .tar dosyasını açın ve domains dosyasını okuyun
with tarfile.open(file_path, 'r') as tar:
    # social_networking/domains dosyasını aç
    domain_member = tar.getmember(domains_file)
    with tar.extractfile(domain_member) as file:
        # Domain'leri oku ve byte'dan string'e çevir
        domains = [line.decode('utf-8').strip() for line in file.readlines()]

# İlk 250 domain
domains_to_check = domains[:]
sayac = 0
kategory=str(domains_file).split('/')[0]

# Dosya yoksa başlıkları yaz
if not os.path.exists(output_file):
    pd.DataFrame(columns=['Domain','Alan Uzantısı','Resim Sayısı','Video Sayısı','Multi Medya Kullanım Sayısı','Toplam Kelime Sayısı','Paragraf Sayısı','H1 Sayısı','H2 Sayısı','H3 Sayısı','Vurgulu Kelime Sayısı','Kalın Kelime Sayısı','Liste Sayısı','Bağlantı Sayısı','Dış Bağlantı Sayısı','İç Bağlantı Sayısı','Form Sayısı','Buton Sayısı','Girdi Sayısı','Responsive Tasarım Varlığı','Sosyal Medya Varlığı','Ödeme Sistemlerinin Varlığı','Çerezlerin Varlığı','Meta Tag Sayısı','Arama Fonksiyonu','Menü Sayısı','Kategory']).to_csv(output_file, index=False, mode='w')


popular_payment_systems = ['paypal', 'visa', 'mastercard', 'stripe', 'apple pay', 'google pay','block chain','crypto']
class_names = ['payment', 'pay', 'checkout']
# Her bir domain'i ziyaret et ve özellikleri bul
for domain in domains_to_check:
    # Şema eksikse, varsayılan olarak 'https://' ekle
    

    if not domain.startswith(('http://', 'https://')):
        domain = 'http://' + domain
    sayac += 1

    if domain.endswith('Shopping'):
        domain=domain[:-len('Shopping')]  # 'remove_part' kadar karakteri sondan kes
    
    # Özellikler sözlüğünü başlangıçta tanımla
    features = {
        'Domain': domain,
        'Domain Uzantısı': 'null',
        'Resim Sayısı': 'null',
        'Video Sayısı': 'null',
        'Multi Medya Kullanım Sayısı': 'null',
        'Toplam Kelime Sayısı': 'null',
        'Paragaraf Sayısı': 'null',
        'Başlık Sayısı (H1)': 'null',
        'Başlık Sayısı (H2)': 'null',
        'Başlık Sayısı (H3)': 'null',
        'Vurgulu Kelime Sayısı': 'null',
        'Kalın Kelime Sayısı': 'null',
        'Liste Sayısı': 'null',
        'Bağlantı Sayısı': 'null',
        'Dış Bağlantı Sayısı': 'null',
        'İç Bağlantı Sayısı':'null',
        'Form Sayısı':'null',
        'Buton Sayısı':'null',
        'Girdi Sayısı':'null',
        'Responsive Tasarım Varlığı':'null',
        'Sosyal Medya Entegrasyonu':'null',
        'Ödeme Sistemleri Varlığı':'null',
        'Çerezlerin Varlığı':'null',
        'Meta Tag Sayısı':'null',
        'Arama Fonksiyonu':'null',
        'Menü Sayısı':'null',
        'Kategory':kategory
    }

    response = None
    print(sayac)
    try:

        response = requests.get(domain, timeout=20)  # Zaman aşımını ayarla
        response.raise_for_status() 

        # BeautifulSoup ile sayfayı analiz et
        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            features['Domain Uzantısı'] = domain.split('.')[-1]
        except Exception:
            features['Domain Uzantısı'] = 'null'

        try:
            features['Resim Sayısı'] = len(soup.find_all('img'))
        except Exception:
            features['Resim Sayısı'] = 'null'

        try:
            features['Video Sayısı'] = len(soup.find_all('video'))
        except Exception:
            features['Video Sayısı'] = 'null'


        try:
            audios=len(soup.find_all('audio'))
            embeds=len(soup.find_all('embed'))
            objects=len(soup.find_all('object'))
            iframes=len(soup.find_all('iframe'))

            features['Multi Medya Kullanım Sayısı']=features['Resim Sayısı']+features['Video Sayısı']+audios+embeds+objects+iframes
        except:
            features['Multi Medya Kullanım Sayısı']='null'


        try:
            features['Toplam Kelime Sayısı'] = len(soup.get_text().split())
        except Exception:
            features['Toplam Kelime Sayısı'] = 'null'


        try:
            features['Paragaraf Sayısı']=len(soup.find_all('p'))
        except:
            features['Paragaraf Sayısı']='null'


        try:
            features['Başlık Sayısı (H1)'] = len(soup.find_all('h1'))
        except Exception:
            features['Başlık Sayısı (H1)'] = 'null'

        try:
            features['Başlık Sayısı (H2)'] = len(soup.find_all('h2'))
        except Exception:
            features['Başlık Sayısı (H2)'] = 'null'


        try:
            features['Başlık Sayısı (H3)'] = len(soup.find_all('h3'))
        except Exception:
            features['Başlık Sayısı (H3)'] = 'null'

        try:
            bold_text = soup.find_all(['b', 'strong'])
            features['Kalın Kelime Sayısı']= sum([len(text.get_text().split()) for text in bold_text])
        except:
            features['Kalın Kelime Sayısı']='null'

        try:
            italic_text = soup.find_all(['i', 'em'])
            features['Vurgulu Kelime Sayısı'] = sum([len(text.get_text().split()) for text in italic_text])
        except:
            features['Vurgulu Kelime Sayısı']='null'

        try:
            
            features['Liste Sayısı']=len(soup.find_all('li'))
        except:
            features['Liste Sayısı']='null'

        try:
            features['Bağlantı Sayısı'] = len(soup.find_all('a'))
        except Exception:
            features['Bağlantı Sayısı'] = 'null'


        try:
            features['Dış Bağlantı Sayısı'] = len([a for a in soup.find_all('a') if a['href'].startswith('http')])
        except Exception:
            features['Dış Bağlantı Sayısı'] = 'null'
        
        try:
            features['İç Bağlantı Sayısı'] = len([a for a in soup.find_all('a') if not a['href'].startswith('http')])
        except Exception:
            features['İç Bağlantı Sayısı'] = 'null'

        try:
            features['Form Sayısı'] = len(soup.find_all('form'))
        except Exception:
            features['Form Sayısı'] = 'null'

        try:
            features['Buton Sayısı']=len(soup.find_all('button'))+len(soup.find_all('input', {'type': ['submit', 'button']}))+len(soup.find_all('a', class_='button'))+len(soup.find_all(class_='btn'))+len(soup.find_all(class_='button'))
        except:
            features['Buton Sayısı']='null'
            

        try:
            features['Girdi Sayısı']=len(soup.find_all('input'))+len(soup.find_all('select'))+len(soup.find_all('textarea'))
        except:
            features['Girdi Sayısı']='null'

        try:
            features['Responsive Tasarım Varlığı'] = 'Var' if soup.find('meta', attrs={'name': 'viewport'}) else 'Yok'
        except:
            features['Responsive Tasarım Varlığı']='null'

        try:
            features['Sosyal Medya Entegrasyonu']='var' if soup.find_all(class_='social') or soup.find_all(class_='social-media') or soup.find_all(class_='social_media') or soup.find_all(class_='share') or soup.find_all(class_='facebook') or soup.find_all(class_='instagram') or soup.find_all(class_='twitter') or soup.find_all(class_='linkedln') or soup.find_all(class_='tiktok') or soup.find_all(class_='telegram') or soup.find_all(class_='vk') or soup.find_all(class_='whatsapp') else 'yok'

        except:
            features['Sosyal Medya Entegrasyonu']='null'

        try:
            images = soup.find_all('img')
            payment_logos = []
            for img in images:
                if any(system in img.get('src', '').lower() for system in popular_payment_systems):
                    payment_logos.append(img)

            payment_elements = soup.find_all(class_='payment')

            if payment_logos or soup.find_all(class_='payment') or soup.find_all(class_='pay') or soup.find_all(class_='checkout') or soup.find_all(class_='secure_payment') or soup.find_all(class_='secure-payment')  :
                features['Ödeme Sistemleri Varlığı']='Var'

            else:
                features['Ödeme Sistemleri Varlığı']='Yok'
        except:
            features['Ödeme Sistemleri Varlığı']='null'

        try:
            features['Çerezlerin Varlığı']='Var' if response.cookies else 'Yok'

        except:
            features['Çerezlerin Varlığı']='null'

        try:
            features['Meta Tag Sayısı']=len(soup.find_all('meta'))
        except:
            features['Meta Tag Sayısı']='null'

        try:
            search_inputs = soup.find_all('input', {'type': 'search'})
            search_forms = soup.find_all('form', {'role': 'search'})
            features['Arama Fonksiyonu']='var' if search_forms or search_inputs else 'yok'
        except:
            features['Arama Fonksiyonu']='null'

        try:
            features['Menü Sayısı'] = len(soup.find_all('nav'))
        except Exception:
            features['Menü Sayısı'] = 'null'

    except requests.exceptions.RequestException:
        pass

    # Yeni veriyi CSV dosyasına ekle
    pd.DataFrame([features]).to_csv(output_file, mode='a', header=False, index=False, encoding='utf-8')

print(f"Özellikler {output_file} dosyasına kaydedildi.")

