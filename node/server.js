require.paths.push(process.cwd());

var http = require('http'),
    io = require('socket.io-node'),
    url = require('url'),
    sys = require('sys'),
    socket;

var server = http.createServer(function(req, resp) {
    var parsed = url.parse(req.url, true),
        query = parsed.query;

    if(/^\/$/(parsed.pathname)) {
        sys.log("received data: "+JSON.stringify(query));
        socket.broadcast(JSON.stringify(query));

        resp.writeHead(200, {'Content-Type':'text/html'});
        resp.write(JSON.stringify({'status':'OK'}));
        resp.end();
    } else {
        resp.writeHead(404, {'Content-Type':'text/html'});
        resp.write(JSON.stringify({'status':'NOT FOUND'}));
        resp.end();
    }
});

server.listen(8124);
socket = io.listen(server);

socket.on('connection', function(client) {
    sys.puts('got client');
    client.on('message', function() {
        sys.puts(arguments);
    });
});
