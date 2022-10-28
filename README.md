#  Profit Autumn Code 2022 Video Generator
Генарация видео по текстовому запросу в рамках участия в проекте [Autumn Code 2022](https://vk.com/vkcode).

Демо веб-приложения доступно [по ссылке](http://51.250.17.189:8501).

## About 

Было создано веб-приложение для генерации релевантного видео по запросу на естественном языке. Целью работы является увеличения уровня счастья пользователя от просмотра таргетированных развлекательных видео. Другим важным сценарией использования является увеличение конверсии рекламных предложений с помощью генерации персональных превью роликов, генерация нарезок из длительных роликов для создания трейлеров.

Основная задача - обучить модель распознавать широкий спектр визуальных концепций в фрагментах видео и связывать их с именованиями на естественном языке. 

Для обучения был использован маркированный набор Youtube видео. 

![image](https://user-images.githubusercontent.com/20246799/198581755-ac1bf3c4-6c37-4ef4-bfec-8be5902ce9d0.png)

## The target audience

Потенциально неограниченная целевая аудитория

## Structure
*  `cut_frames_and_calculate_embs.ipynb` – ipython notebook for data preparation;
* 	`indexer.ipynb` — ipython notebook for video indexing


## Models
* [CLIP](https://github.com/openai/CLIP) - neural network for calculating text-video relevance


## Libraries 

* [pandas](https://github.com/pandas-dev/pandas) — software library in Python for data processing and analysis. 
* [numpy](https://github.com/numpy/numpy) — software library in Python that adds support for large multidimensional arrays and matrices. 
* [nmslib](https://github.com/nmslib/nmslib) - software library for similarity searching


## Data:
Set of videos downloaded from Youtube
