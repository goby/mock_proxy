local key=ngx.var.domain
local redis= require "resty.redis"
local red = redis:new()
red:set_timeout(1000)
local ok, err = red:connect("127.0.0.1", 6379)
if not ok then
    ngx.log(ngx.ERR, "Failed to redet to redis :", err)
    return ngx.exit(500)
end

local host, err = red:hmget(key, "backend", "start_ip", "end_ip")
if not host then
    ngx.log(ngx.ERR, "failed to get redis key: ", err)
    return ngx.exit(500)
end

if host == ngx.null then
    ngx.log(ngx.ERR, "no host found for key ", key)
    return ngx.exit(400)
end

--ngx.log(ngx.ERR,host)
--ngx.log(ngx.ERR,host[1])
--ngx.log(ngx.ERR,host[2])
--ngx.log(ngx.ERR,host[3])

function ip_from_int(i)
    local tmp = i % 256
    i = math.floor(i / 256)
    while i > 0 do
        tmp = (i % 256).."."..tmp
        i = math.floor(i/256)
    end
    return tmp
end
local randomkey = host[2]
if host[2] ~= nil then
    randomkey = math.random(host[2], host[3])
end
ngx.var.client_ip = ip_from_int(randomkey)
ngx.var.target = host[1]
