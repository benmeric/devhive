# 🤖 DevHive – Programlama Asistanı

DevHive, Google Gemini 1.5 Flash API ile entegre çalışan, Streamlit tabanlı bir **programlama odaklı yapay zeka asistanıdır**. Kod yazarken, algoritmalar hakkında sorular sorarken veya teknik konularda yardım alırken DevHive yanınızda!

## 🚀 Özellikler

- 💬 Google Gemini 1.5 Flash API ile gerçek zamanlı sohbet
- 🌐 Türkçe ve İngilizce dil desteği (Dinamik seçim)
- 📥 Sohbet geçmişini `.txt` olarak indirme
- 🔄 Tek tıkla yeni sohbete başlama
- 📌 Sidebar’da geliştirici bilgileri

## 🔗 Demo
https://devhive.streamlit.app/

## ⚙️ Kurulum

1. Bu projeyi klonlayın:

```bash
git clone https://github.com/kullaniciadi/devhive.git
cd devhive
```

2. Gerekli bağımlılıkları yükleyin:

```bash
pip install -r requirements.txt
```

3. `.streamlit/secrets.toml` dosyasını oluşturun ve aşağıdaki gibi API anahtarınızı ekleyin:

```toml
GOOGLE_API_KEY = "your_google_gemini_api_key"
```

4. Uygulamayı başlatın:

```bash
streamlit run app.py
```

## 🧠 Kullanım

- Sohbet kutusuna sadece **programlama ile ilgili** sorular yazın.
- Sağ sidebar’dan dili seçin: **Türkçe** veya **English**
- Sohbeti istediğiniz zaman indirip sıfırlayabilirsiniz.

## 👨‍💻 Geliştirici

**Meriç Yüzaklı**

- 📧 benmericinfo@gmail.com  
- 📸 [Instagram](https://www.instagram.com/benmericig/)  
- ▶️ [YouTube](https://www.youtube.com/benmericyt)

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.

---

> “Kodlayan zihin, öğrenen bir zihin olmaya devam eder.” – </> DevHive
