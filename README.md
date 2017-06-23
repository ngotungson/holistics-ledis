# holistics-ledis
Very small, light-weight caching server like Redis

## Dependences
```pip install schedule```

## How to run on local machine?
  1. Run server: ```python server/server.py.```
  2. Open connection to port 8888 on localhost. Example: ```telnet localhost 8888.```

That's it. Now we can start making command on terminal.

```set foo bar```

```get foo```

```rpush 1 2 3 4```
