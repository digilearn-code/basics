import chevron

NGINX_CONFIGURATION = """
server {
        listen 443 ssl;
        listen [::]:443 ssl;
        ssl_certificate /etc/letsencrypt/live/{{domain}}/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/{{domain}}/privkey.pem;
        include /etc/letsencrypt/options-ssl-nginx.conf;
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

        root /var/www/html;

        server_name {{domain}};

        location / {
                proxy_pass http://127.0.0.1:{{port}}/;
                include proxy_params;
        }
}


server {
        if ($host = {{domain}}) {
                return 301 https://$host$request_uri;
        }
        server_name {{domain}};
        listen 80;
        return 404;
}
"""


if __name__ == "__main__":
    print(chevron.render(NGINX_CONFIGURATION, {
        "domain": "basics.digilearn.be",
        "port": 5002
    }))
