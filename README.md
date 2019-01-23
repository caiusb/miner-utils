# GitHub and Travis mining utility 

## Installation

Run `pip install "git+https://github.com/caiusb/miner-utils"`

## Usage

### Instantiating a miner

To instantiate a GitHub miner, simply call the constructor:

```
gh = GitHub();
```

The contructor takes 2 optional arguments, a username and a token. It is recommended that you use them, in order to greatly reduce the time it takes to collect the data:

```
gh = GitHub(username, token)
```

To instantiate a Travis miner, simply call the constructor: 

```
tr = Travis()
```

The constructor also takes 1 optional authentication token:

```
tr = Travis(token)
```

### Calling the API

Both miners have a similar API. To perfom a get request, use:

```
gh.get("/repos/scala/scala/pulls", params={'state': 'all'})
```

The example above, gets all the pull requests for the specified project. Consult the documentation of the service that you are using to determine what resources are available. If you need to pass a parameter, or a query, use the `params` argument. It takes a map (key, value pairs) of the arguments that you want to pass. Alternatively, you can pass the parameters in the url directly, like this:

```
gh.get("/repos/scala/scala/pulls?state=all")
```

## License

This project is licensed under the MIT License - see the LICENSE.md file for details