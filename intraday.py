import blpapi

if __name__ == "__main__":
    print "SimpleHistory"

    opts = blpapi.SessionOptions()
    opts.setServerHost("http-api.openbloomberg.com")
    opts.setServerPort(443)

    session = blpapi.Session(opts)
    assert session.start()

    refdata = session.getService("//blp/refdata")

    req = refdata.createRequest("IntradayBarRequest")
    request.set("eventType", "TRADE")
    request.set("security", "IBM")

    request.set("startDateTime", "20150302")
    request.set("endDateTime", "20150702")
    request.set("interval", 60)

    print "sending request", request
    session.sendRequest(request)

    try:
        while True:
            ev = session.nextEvent(500)
            for msg in ev:
                print msg

            if ev.eventType() == blpapi.Event.RESPONSE:
                break

    finally:
        session.stop()
