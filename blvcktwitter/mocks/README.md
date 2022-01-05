# Here i am going to learn about mock testing and push everything here

* So first thing i did was to install the library as 

* ```pip install nose requests```

* Secondly i had to check if i was getting a response from twitter notification with the command

```#curl -X GET 'https://twitter.com/notifications```

> results for this is the file ```test_notifications.html```

### Now the basic code is like this

``` 
from nose.tools import assert_true
import requests


def test_request_response():
    # Send a request to the API server and store the response.
    response = requests.get('https://twitter.com/messages')

    # Confirm that the request-response cycle completed successfully.
    assert_true(response.ok) 

 ```


> To run this file use 
```nosetests --verbosity=2 mocks```
> And you get this result

```
mocks.test-msg.test_request_response ... ok

----------------------------------------------------------------------
Ran 1 test in 1.765s

OK
```

> Note that mocks is folder which containts tgw files we are running. In this case it's a module and running the command above will produce an error if you don't refrence this folder as a module. And to do that just add a empty py file in the directory.
```__init__.py```


##### From here i made a few adjustments to the code and the results still the same

##### There's still quite an extensive content i still need to delve into ,but for now this should suffice. I will keep adding new stuff and examples to this project