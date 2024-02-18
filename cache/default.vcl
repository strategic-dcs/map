# specify the VCL syntax version to use
vcl 4.1;

backend default {
      .host = "backend";
      .port = "8000";
}


sub vcl_recv {
    # Sitrep has no caching
    if (req.url ~ "^/sitrep($|/.*)") {
        return (pass);
    }
}

sub vcl_fetch {
    # Everything else for now, we set 15 mins
    set beresp.ttl = 15m;

    # This is very unlikely to be a problem, so we keep it
    # really short, we send http cache control to clients
    set beresp.grace = 1m;

    # Tell client browsers to cache it for 15 minutes (our ttl)
    set beresp.http.Cache-Control = "public, max-age=900";
}