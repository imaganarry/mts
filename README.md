# Проект «ИИ для анализа пользовательских ответов»
# Ссылка на тг-бота https://t.me/LychMTSBot
## Инструкция по использованию тг-бота LychMTSBot
1.	Нажимаем /start.
2.	Скидываем ответы пользователей/текст, который хотим проанализировать одним сообщением.
3.	Выбираем фильтр по количеству или по важности.
4.	Пишем /done.
5.	Получаем результат от бота: облако слов – картинка и текстовое описание с количественными показателями.
6.	Далее можем снова ввести текст.


## Состав команды "Луч":
- Рябов Игорь Алексеевич
- Гущин Александр Вячеславович
- Суббот Диана Сергеевна
- Бовт Анна Константиновна

## Задача: анализ пользовательских ответов

## 1.	ПРОБЛЕМА

Желание проанализировать ответы большого числа сотрудников на конкретный вопрос.


## 2.	ПРЕДЛОЖЕННОЕ РЕШЕНИЕ
Разработка алгоритма, который принимает несколько запросов, анализирует список пользовательских ответов, чистит входные данные от лишнего и возвращает понятное и интерпретируемое облако слов.



## 3. Состав репозитория 

### Осноной файл с алгоритмом програмного продукта основа, здесь расположен код бота
main.py 

### Основные функции, которые позволяют обрабатывать слова
obr1.py

### Список нецензурных слов: 
bad_words_en.txt
bad_words_ru.txt

### Маски для формирования облака:
cloud_shape.png
cloud_shape2.png 

### Результаты тестирования:
wordcloud_counts.png
wordcloud_importance.png

## 4. Краткое описание функционала в файле obr1.py
ПО КОЛИЧЕСТВУ:
1. С помощью регулярных выражений фильтруем текст от знаков препинания, оставляя только буквы. 
2. Токинезация слов, получаем их список. 
3. Фильтр нецензурной лексики. 
4. Фильтр стоп-слов. 
5. Определение языка каждого слова. 
6. Леммизация (для русских и английских слов разная). 
7. Считаем слова.

ПО ВАЖНОСТИ:
1. С помощью регулярных выражений фильтруем текст от знаков препинания, оставляя только буквы. 
2. Токинезация слов, получаем их список. 
3. Фильтр нецензурной лексики. 
4. Выставление весов по важности с помощью библиотеки multi-rake.


## 5.	ЭТАПЫ ПРОЕКТА И ОТВЕТСТВЕННЫЕ
1. Определение плана работ, распределение ролей. (отв. Гущин Александр)
2. Поиск DataSet. (отв. Бовт Анна, Гущин Александр)
3. Сбор тестовых данных со студентов на вопрос «Что меня мотивирует учиться?» (отв. Суббот Диана)
4. Разработка алгоритма, обрабатывающего поток входных данных. (отв. Рябов Игорь)
5. Создание интерфейса взаимодействия с алгоритмом. (отв. Гущин Александр, Суббот Диана)
6. Тестирование конечного продукта. (отв. Гущин Александр, Бовт Анна, Суббот Диана)
7. Исправление недочетов. (отв. Рябов Игорь, Гущин Александр)
8. Подготовка отчетности и документации. (отв. Суббот Диана, Бовт Анна)



