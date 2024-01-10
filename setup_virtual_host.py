#!/usr/bin/env python3

# Simple Python script to create a new virtual host for Apache2 on Linux systems (Ubuntu, Debian, etc.)
# Usage: python3 setup_virtual_host.py [domain] [reverse proxy port]
# Author: Saku (saku.lol)
# 28.2.2023

import os
import sys


def create_vhost(domain, document_root, proxy=False, proxy_port=None):
    vhost_config = f"""
    <VirtualHost *:80>
        ServerName {domain}
        DocumentRoot {document_root}
    """

    if proxy and proxy_port:
        vhost_config += f"""
        ProxyRequests Off
        ProxyPreserveHost On
        ProxyPass / http://127.0.0.1:{proxy_port}/
        ProxyPassReverse / http://127.0.0.1:{proxy_port}/
        """

    vhost_config += """
    </VirtualHost>
    """

    vhost_filename = f"{domain}.conf"
    vhost_filepath = os.path.join("/etc/apache2/sites-available", vhost_filename)
    with open(vhost_filepath, "w") as vhost_file:
        vhost_file.write(vhost_config)

    os.system(f"sudo a2ensite {vhost_filename}")
    os.system("sudo service apache2 reload")


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 2:
        print("Usage: python3 script_name.py <domain> <document_root> [proxy_port]")
        sys.exit(1)

    domain = args[0]
    document_root = args[1]
    proxy_port = None
    if len(args) > 2:
        proxy = True
        proxy_port = args[2]
    else:
        proxy = False

    create_vhost(domain, document_root, proxy=proxy, proxy_port=proxy_port)