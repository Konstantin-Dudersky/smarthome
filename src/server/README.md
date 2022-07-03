
Перенаправление портов на локальной машине:

```sh
sudo iptables -t nat -A OUTPUT -o lo -p tcp --dport 80 -j REDIRECT --to-port 8000
```