import chevron

NGINX_CONFIGURATION = """
server {
        listen 443 ssl;
        listen [::]:443 ssl;
        ssl_certificate /etc/letsencrypt/live/{{project}}.digilearn.be/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/{{project}}.digilearn.be/privkey.pem;
        include /etc/letsencrypt/options-ssl-nginx.conf;
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

        root /var/www/html;

        server_name {{project}}.digilearn.be;

        location / {
                proxy_pass http://127.0.0.1:{{port}}/;
                include proxy_params;
        }
}


server {
        if ($host = {{project}}.digilearn.be) {
                return 301 https://$host$request_uri;
        }
        server_name {{project}}.digilearn.be;
        listen 80;
        return 404;
}
"""

SYSTEMD_CONFIGURATION = """
[Unit]
Description={{project}}
After=syslog.target

[Service]
User=teamcity
WorkingDirectory=/home/teamcity/{{project}}
ExecStart=/home/teamcity/{{project}}/venv/bin/gunicorn --bind :{{port}} --workers 2 --timeout 7200 --worker-tmp-dir /dev/shm server:app

[Install]
WantedBy=multi-user.target
"""


if __name__ == "__main__":
    for data in ['basics:5002']:
        colon = data.index(':')
        parameters = {
            'project': data[:colon],
            'port': int(data[colon + 1:])
        }
        print("# NGINX configuration")
        print(chevron.render(NGINX_CONFIGURATION, parameters))
        print("# SYSTEMD configuration")
        print(chevron.render(SYSTEMD_CONFIGURATION, parameters))
