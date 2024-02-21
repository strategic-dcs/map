# specify the VCL syntax version to use
vcl 4.1;

import std;

backend default {
      .host = "backend";
      .port = "8000";
}


sub vcl_recv {

		# Strip leading /api/
		if (req.url ~ "^/api/") {
			set req.url = regsub(req.url, "/api/", "/");
		}

    # Sitrep has no caching
    if (req.url ~ "^/sitrep($|/.*)") {
        return (pass);
    }
}

sub vcl_backend_response {
    # Everything else for now, we set 15 mins
    set beresp.ttl = 15m;

    # This is very unlikely to be a problem, so we keep it
    # really short, we send http cache control to clients
    set beresp.grace = 1m;

    # Tell client browsers to cache it for 15 minutes (our ttl)
		# set beresp.cacheable = true;
    set beresp.http.Cache-Control = "public, max-age=900";
		set beresp.http.cachable = "1";

		# And also set Expiry
		# set beresp.http.Expires = "" + (now + std.duration(900s));
}
