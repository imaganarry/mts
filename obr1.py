import random
def random_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl({}, {}%, {}%)".format(random.randint(0, 360), random.randint(70, 100), random.randint(40, 80))

def process_texts(texts):
    from multi_rake import Rake
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from pymorphy3 import MorphAnalyzer
    import re
    from collections import Counter
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    import numpy as np
    from PIL import Image

    stop_words_en = set(stopwords.words("english"))
    stop_words_ru = set(stopwords.words("russian"))
    stop_words = stop_words_en.union(stop_words_ru)
    lemmatizer = WordNetLemmatizer()
    morph = MorphAnalyzer()

    with open('bad_words_en.txt', 'r', encoding='utf-8') as f:
        bad_words_en = set(f.read().split())
    with open('bad_words_ru.txt', 'r', encoding='utf-8') as f:
        bad_words_ru = set(f.read().split())

    bad_words = bad_words_en.union(bad_words_ru)
    cleaned_texts = []
    normal_words = []
    for text in texts:
        new_text = re.sub(r'[^a-zA-Zа-яА-Я]', ' ', text)
        words = new_text.split()
        cleaned_words = [word.lower() for word in words if word.lower() not in bad_words]
        cleaned_text = ' '.join(cleaned_words)
        cleaned_texts.append(cleaned_text)
        cleaned_words = [word for word in cleaned_words if word not in stop_words]
        for i in range(len(cleaned_words)):
            if ord(cleaned_words[i][0]) >= ord('a') and ord(cleaned_words[i][0]) <= ord('z') or ord(
                    cleaned_words[i][0]) >= ord('A') and ord(cleaned_words[i][0]) <= ord('Z'):
                cleaned_words[i] = lemmatizer.lemmatize(cleaned_words[i])
            else:
                cleaned_words[i] = morph.parse(cleaned_words[i])[0].normal_form
        normal_words += cleaned_words
    full_text = ' '.join(cleaned_texts)
    r = Rake()
    keywords = r.apply(full_text)
    key_phrases = [kw[0] for kw in keywords]
    words_count_list = []
    count_dict = {}
    for i in normal_words:
        if i in count_dict.keys():
            count_dict[i] += 1
        else:
            count_dict[i] = 1
    for i in count_dict.keys():
        words_count_list.append((i, count_dict[i]))
    words_count_list.sort(key=lambda x: x[1], reverse=True)
    words_importance_list = keywords
    word_freq_count = dict(words_count_list)
    word_freq_importance = {kw[0]: kw[1] for kw in words_importance_list}

    mask = np.array(Image.open('cloud_shape2.png'))
    mask2 = np.array(Image.open('cloud_shape.png'))

    wordcloud_counts = WordCloud(
        width=1200, height=800,
        background_color="white",
        colormap="rainbow",  # Яркая палитра
        prefer_horizontal=0.7,  # 70% слов горизонтально, 30% вертикально
        color_func=random_color_func,  # Используем функцию для случайных цветов
        max_font_size=300,  # Максимальный размер шрифта
        min_font_size=10,  # Минимальный размер шрифта
        random_state=42,  # Для повторяемости результатов
        contour_color="black",  # Добавление контура
        contour_width=1,  # Толщина контура
        relative_scaling=0.5,  # Контроль за расстоянием между словами
        collocations=False,  # Отключение автоматических пар слов
        mask=mask  # Применяем маску для формы облака
    ).generate_from_frequencies(word_freq_count)


    wordcloud_importance = WordCloud(
        width=1200, height=800,
        background_color="white",
        colormap="rainbow",  # Яркая палитра
        prefer_horizontal=0.7,  # 70% слов горизонтально, 30% вертикально
        color_func=random_color_func,  # Используем функцию для случайных цветов
        max_font_size=300,  # Максимальный размер шрифта
        min_font_size=10,  # Минимальный размер шрифта
        random_state=42,  # Для повторяемости результатов
        contour_color="black",  # Добавление контура
        contour_width=1,  # Толщина контура
        relative_scaling=0.5,  # Контроль за расстоянием между словами
        collocations=False,  # Отключение автоматических пар слов
        mask=mask2  # Применяем маску для формы облака
    ).generate_from_frequencies(word_freq_importance)

    wordcloud_counts.to_file('wordcloud_counts.png')
    wordcloud_importance.to_file('wordcloud_importance.png')
    return words_count_list, words_importance_list, 'wordcloud_counts.png', 'wordcloud_importance.png'

if __name__ == '__main__':
    test_texts = [
        "Меня мотивирует работать зарплата и удобные условия работы",
        "I am motivated by salary and comfortable working conditions",
        "Работа должна быть интересной и хорошо оплачиваться",
        "Оскорбление плохое слово",
        "This sentence contains a badword"
    ]

    words_count_list, words_importance_list, wc_counts, wc_importance = process_texts(test_texts)
    print("Words Count List:")
    print(words_count_list)

    print("\nWords Importance List:")
    print(words_importance_list)

    print("\nWord cloud images saved as:")
    print(wc_counts)
    print(wc_importance)
