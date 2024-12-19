import spacy
from spacy.pipeline import EntityRuler
from spacy import displacy
import json
import streamlit as st
import base64

# GiNZAモデルの読み込み
nlp = spacy.load("ja_ginza")

# EntityRulerの作成
ruler = nlp.add_pipe("entity_ruler", before="ner")

# 読み込むJSONファイル名のリスト
pattern_files = ["ginza_patterns_clinic_matsumoto-oomachi-kiso.json", "ginza_patterns_clinic_matsumoto-shi.json", "ginza_patterns_hospital.json", "ginza_patterns_houkan.json", "patterns_trinity_facility.json"]

# 各ファイルからパターンを読み込む
for file in pattern_files:
    with open(file, encoding="utf-8") as f:
        patterns = json.load(f)
        ruler.add_patterns(patterns)

# 抽出するラベルのリスト
target_labels = ["Person", "Country", "City", "Gpe_Other", "Occasion_Other", "Location", "Location_Other", "Domestic_Region", "Province", "Station", "Continental_Region", "Theater", "Facility", "Organization", "Company", "School", "International_Organization", "Goe_Other", "Show_Organization", "Corporation_Other"]

# Streamlitの設定
st.title("カスタムGiNZAでNER抽出")
st.write("テキストを入力して、NERエンティティを抽出します。")

# テキスト入力欄
input_text = st.text_area("テキストを入力してください：")

# 変換ボタン
if st.button("解析開始"):
    # テキストの解析
    doc = nlp(input_text)
    # 特定のラベルを持つエンティティのみを抽出
    entities = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in target_labels]

    # displacyで表示する内容をHTMLとして保存
    html = displacy.render(doc, style="ent", jupyter=False)

    # HTMLをファイルに書き込む
    output_filename = "output_entities.html"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html)

    # HTMLファイルのダウンロードリンクを作成
    def download_link(html_content, download_filename, download_link_text):
        b64 = base64.b64encode(html_content.encode()).decode()
        return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

    download_html = download_link(html, output_filename, "解析結果をダウンロード")
    st.markdown(download_html, unsafe_allow_html=True)

    st.write("エンティティの情報が解析されました。以下のリンクからダウンロードできます。")

