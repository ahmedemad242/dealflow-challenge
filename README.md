# dealflow

A simple api used to fetch freelancers data.

## Installation

### Virtual environments

```
$ ./initialize_project.sh
$ poetry shell
```

### Environment variables

Add environment varaibles to .env file

### Running

```
$ flask db upgrade
$ flask fake freelancers 100
$ flask run
```

## Application Structure

```
app/
├── run.py
├── pyproject.toml
├── tests
└── src/dealflow
    ├── config.py
    ├── models
    ├── util
    └── api
        └── freelancers
```

## API documentation

The API is documented using Swagger UI. Run server and navigate to `/docs`
![image](https://github.com/ahmedemad242/dealflow-challenge/assets/50369848/ce1c5386-053f-4c4c-84bf-facf17d66e48)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
