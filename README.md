

_theano_

```
docker run --name theano -dit -v /Users/markwang/github/iGEM2016:/root/iGEM2016 kaixhin/theano
docker exec -it theano /bin/bash
```

_persistent data volume container_

```
docker create -v /var/lib/mysql --name dbdata mysql
```

_mysql container_

```
docker run --volumes-from dbdata --name ml_mysql -e MYSQL_ROOT_PASSWORD=1122 -d mysql
docker cp /Users/markwang/github/iGEM2016/dota2DL/collectData/dbinit.sql ml_mysql:/dbinit.sql
docker exec -it ml_mysql bash

# interactive shell
docker run -it --link ml_mysql:mysql --rm mysql sh -c 'exec mysql -h"$MYSQL_PORT_3306_TCP_ADDR" -P"$MYSQL_PORT_3306_TCP_PORT" -uroot -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD"'
```

_application container_

```
docker run --name igem2016 --link ml_mysql:mysql -dit -v /Users/markwang/github/iGEM2016:/root/iGEM2016 tt6746690/igem2016:test /bin/bash
```



__Resources__


[_Official theano tutorial_](http://deeplearning.net/software/theano/tutorial/)
[_Neural network demystified_](https://github.com/stephencwelch/Neural-Networks-Demystified)
[_Dockerfile digitalocean tutorial_](https://docs.docker.com/engine/reference/builder/)
[_dota2 cp blog summary_](http://kevintechnology.com/post/71621133663/using-machine-learning-to-recommend-heroes-for)
