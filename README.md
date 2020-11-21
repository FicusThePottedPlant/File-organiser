Пояснительная записка к проекту 'Сортировщик файлов'
Автор проекта: Асадуллин Тагир Айратович
Руководитель проекта: А.Г. Гильдин

Задание проекта - предоставить удобный интерфейс для автоматической организации файлов по их типу

Взаимодействие с пользователем.



![Главное окно](https://i.postimg.cc/8zCwBcn6/main-ui1.png)

Краткое описание проекта.
Проект состоит из 7 python файлов и 4 файла для UI/UX
main.py - файл с главным интерфейсом добавлений директорий для их дальнейшей сортировкой
main_window.py - UI файл для дизайна окна Main в main.py
settings_for_bd.py - гибкие настройки для сортировки по файлам. Класс SecondForm предоставляет интерфейс доступа к files.sqlite с помощью которого вы можете добавлять новые типы и расширения, а также редактировать их.
Также в файле содержатся два класса AddForm1 и AddForm2, которые нужны для интерфейса добавления и редактирования расширений и типов соответственно
second_ui.py - UI файл для дизайна окна SecondForm 
add_extension.py - UI файл для дизайна окна AddForm1
add_type.py - UI файл для дизайна окна AddForm2
fs_script - скрипт для самой сортировки директорий в котором содержится класс OrganiseByFiles методы которых сортируют файлы и папки по критериям.

В папке data лежит следующий файл:
files.sqlite - база данных файлов и их типов.

В папке ui лежат следующие файлы:
logo.png, plus.png, minus.png, settings.png - фото для UI

Использованы модули: os, shutil для работы с директориями (копирование файлов, просмотра файлов в директории и тд), pyqt5(для создания GUI), sqlite3 (для работы с базой данных files.sqlite), sys

Использованы такие технологии: 
Отлов ошибок, работа c sql данными, подключение ui, изображения(pixmap), таблицы в pyqt, модальные окна, диалоговые окна, окна выборов
