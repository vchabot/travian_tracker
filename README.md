# <p align="center">Travian Tracker</p>
  
Travian Tracker is a project helping you to get every tools you can find online, on your computer.


## 🧐 Features    
- Get data from your Travian server every night
- Compute data to give you fresh data from your Travian server
- Find my neighbour (not yet implemented)
- Inactive player (not yet implemented)
- Offensive operation creator (not yet implemented)
 

## 🛠️ Tech Stack
- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker](https://www.docker.com/)
- [Postgresql](https://www.postgresql.org/)
        
 
## 🚀 Installation

### Using Poetry
```bash
poetry install
```

You need to fill the `TRAVIAN_SERVER_URL` variable in the 
[docker-compose.yml file](docker-compose.yml) with your server url.

## 🧑🏻‍💻 Usage

Start the containers
```bash
docker-compose up --build
```

A scheduler (container) is created to retrieve data from your server everyday at 00:01.

If you don't want to wait, you can run the following command to retrieve data from your server:
```bash
docker-compose exec app python -m travian_tracker.scripts.download_and_ingest
```

Or you can access to it via the FastAPI interface at `http://localhost:8000/docs#/default/test_scheduler_action_test_scheduler_action_get`

## 🤝 Contributing
Contributions, issues and feature requests are welcome. Feel free to check [issues page](https://github.com/vchabot/travian_tracker/issues) if you want to contribute.

## 📝 License
This project is [MIT]()

## 👨‍💻 Author
- Vincent Chabot
  - [LinkedIn](https://www.linkedin.com/in/chabotvincent/)
  - [X / Twitter](https://x.com/vincentchabot)
  - [Github](https://github.com/vchabot)
  - [Website](https://vincent-chabot.com/)

           