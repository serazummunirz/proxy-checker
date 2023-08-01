from django.shortcuts import render, redirect
from .models import CheckList, CheckSingle, OutputFile
from .forms import CheckListForm, SingleCheckForm
from django.contrib import messages


import requests
import socks
import socket
from ipwhois import ipwhois
import json
import os


def ip_whois_lookup(ip_address):
    try:
        # Perform the WHOIS lookup
        j_result = ipwhois(ip_address)
        result = json.loads(j_result)
        
        # Print the results
        # print("IP Address:", result['ip'])
        # print("Country:", result['country'])
        # print("City:", result['city'])
        # print("Region:", result['region'])
        # print("ISP:", result['isp'])

        ip_info = {
            'ip': result['ip'],
            'country': result['country'],
            'city': result['city'],
            'region': result['region'],
            'isp': result['isp']
        }

        return ip_info

    except Exception as e:
        print("Error:", str(e))


def get_public_ip_with_proxy(proxy_host, proxy_port, proxy_username, proxy_password):
    try:
        # Set up the SOCKS proxy with authentication
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy_host, proxy_port, True, proxy_username, proxy_password)
        socket.socket = socks.socksocket

        # Make a GET request to the ipify API
        response = requests.get('https://api.ipify.org?format=json', verify=False)

        # Parse the JSON response to get the IP address
        ip_address = response.json()['ip']
        return ip_address
    except Exception as e:
        print("Error:", str(e))
        return None


def check_list(request):
    if request.method == "POST":
        form = CheckListForm(request.POST)
        proxy_list = request.POST['proxy_list']
        lines = proxy_list.split("\n")
        try:
            os.remove('media/proxy_geoip.csv')
        except:
            pass
        for line in lines:
            # print(line)
            ip_addr = line.split("@")[1].split(":")[0]
            port = line.split("@")[1].split(":")[1]
            username = line.split("@")[0].split(":")[0]
            password = line.split("@")[0].split(":")[1]

            public_ip = get_public_ip_with_proxy(ip_addr, int(port), username, password)
            if public_ip:
                # print(f'Public IP: {public_ip}:{port}')
                whois_info = ip_whois_lookup(public_ip)
                with open('media/proxy_geoip.csv', 'a') as f:
                    data = f"{ip_addr}:{port.strip()},{whois_info['country']},{whois_info['city']},{whois_info['region']},{whois_info['isp']},{whois_info['ip']}"
                    f.write(data + "\n")
                # print(whois_info['ip'] + ":" + port.strip() + "," + whois_info['country'])
            else:
                print(f'Error connecting to SOCKS5 proxy {ip_addr}:{port}')


    else:
        form = CheckListForm()
    
    filepath = OutputFile.objects.first().output.url
    status = OutputFile.objects.first().status

    context = {
        'form': form,
        'filepath': filepath,
        'status': status
    }
    return render(request, "check_list.html", context)


def single_check(request):

    if request.method == "POST":
        form = SingleCheckForm(request.POST)

        ip_addr = request.POST['ip_addr']
        port = request.POST['port']
        username = request.POST['username']
        password = request.POST['password']

        print(ip_addr, port, username, password)

        public_ip = get_public_ip_with_proxy(ip_addr, int(port), username, password)
        if public_ip:
            messages.success(request, f'Public IP: {public_ip}')
        else:
            messages.error(request, f'Error connecting to SOCKS5 proxy {ip_addr}:{port}')
        return redirect('single_check')

    else:
        form = SingleCheckForm()
    
    context = {
        'form': form
    }
    return render(request, "single_check.html", context)