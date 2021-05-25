# Movies-Script-Helper
Acest repository contine un site de filme creat folosind django si separat un folder cu scrapere pentru aplicatii de filme.

**Sectiunea Site-ului**

**Documentatia codului**
Pentru a vedea logica din spatele site-ului creat acesati documentatia externa aici : https://movieapp.developerhub.io/movie-app

**Pentru a instala site-ul urmati urmatorii pasi**

1. Downloadati proiectul ![image](https://user-images.githubusercontent.com/35890341/114370131-ca308600-9b87-11eb-86ac-4bb8abb172da.png)
2. O sa dureze ceva dar dupa ce l-ati downloadat extrageti arhiva unde doriti. Numele folderului va fi "Movies-Script-Helper-master"
3. Deschideti un terminal pentru a instala dependentele. Cel mai usor faceti un felul urmator: 
Selectati bara de sus prin dublu click ![image](https://user-images.githubusercontent.com/35890341/114371255-fd274980-9b88-11eb-956b-dad47556e903.png)
Scrieti "cmd" in locul path-ului si apasati enter ![image](https://user-images.githubusercontent.com/35890341/114371465-2e077e80-9b89-11eb-857b-8451868c55ba.png) 
4. Ar trebui sa deschida un terminal cmd in directorul unde ati salvat proiectul
![image](https://user-images.githubusercontent.com/35890341/114371603-568f7880-9b89-11eb-8518-d549aee578ce.png)
5. Rulati comanda pentru a instala dependentele  `pip install -r requirements.txt`
6. Navigati in directorul unde se afla manage.py `cd djangoProject`
7. Rulati server-ul `python manage.py runserver`
8. Copiati link-ul acesta http://localhost:8000/movieapp/home/ in browser si ar trebui sa vedeti aplicatia
![image](https://user-images.githubusercontent.com/35890341/114372107-dcabbf00-9b89-11eb-9b23-48958b8e4d0a.png)



**For running Scrapers**
Collection of python scripts that help find subtitles change directory names 

The setup is quite easy


1.First clone the repo using `git clone https://github.com/nickk2002/Movies-Script-Helper`


2.Navigate to the created folder `cd Movies-Script-Helper`


3.Install requirements `pip install -r requirements.txt`

4.Navigate to the app folder where the code lives `cd app`


3.Run the movie handler with desired arguments `py -m Scripts.movie_handler -di -dir="directory" -tor`


Arguments: 


`-dir=directory_name` to set the directory of movies


`-di` to run diactritice replace


`-m` to run folder rename


`-tor` to run interactive download shell from filelist
