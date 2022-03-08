import re


class CalcIPV4:
    def __init__(self, ip, cidr=None, mascara=None):
        self.ip = ip
        self.cidr = cidr
        self.mascara = mascara

        self.set_broadcast()
        self.set_rede()

    @property
    def ip(self):
        return self._ip

    @property
    def cidr(self):
        return self._cidr

    @property
    def mascara(self):
        return self._mascara

    @ip.setter
    def ip(self, value):
        if not self._valida_ip(value):
            raise ValueError("IP invalido")
        self._ip = value
        self.ip_bin = self.ip_to_bin(self._ip)

    @cidr.setter
    def cidr(self, value):
        if not value:
            return
        if not isinstance(value, int):
            raise TypeError("Prefixo precisa ser inteiro")
        if value > 32:
            raise TypeError("Prefixo precisa ter 32 bits")
        self._cidr = value
        self._mascara_bin = (value * '1').ljust(32, '0')
        self.mascara = self.bin_to_ip(self._mascara_bin)

    @mascara.setter
    def mascara(self, value):
        if not value:
            return
        if not self._valida_ip(value):
            raise ValueError("Mascara invalida")

        self._mascara = value
        self._mascara_bin = self.ip_to_bin(self._mascara)

    @staticmethod
    def _valida_ip(ip):
        regexp = re.compile(r'^([0-9]{1,3}).([0-9]{1,3}).([0-9]{1,3}).([0-9]{1,3})$')

        if regexp.search(ip):
            return True

    @staticmethod
    def ip_to_bin(ip):
        blocos = ip.split(".")
        blocos_binarios = [bin(int(x))[2:].zfill(8) for x in blocos]
        return ''.join(blocos_binarios)

    @staticmethod
    def bin_to_ip(ip):
        n = 8
        blocos = [str(int(ip[i:n + i], 2)) for i in range(0, 32, n)]
        return '.'.join(blocos)

    def set_broadcast(self):
        host_bits = 32 - self.cidr
        self._broadcast_bin = self.ip_bin[:self.cidr] + (host_bits * '1')
        self._broadcast = self.bin_to_ip(self._broadcast_bin)
        return self._broadcast

    def set_rede(self):
        host_bits = 32 - self.cidr
        self._rede_bin = self.ip_bin[:self.cidr] + (host_bits * '0')
        self._rede = self.bin_to_ip(self._rede_bin)
        return self._rede

    def get_numero_ips(self):
        return 2 ** (32 - self.cidr)

    @property
    def rede(self):
        return self._rede

    @property
    def broadcast(self):
        return self._broadcast

    @property
    def numero_ips(self):
        return self.get_numero_ips()


def main():
    calc_ipv4_1 = CalcIPV4(ip='192.168.0.128', cidr=30)

    print(f'IP: {calc_ipv4_1.ip}')
    print(f'Máscara: {calc_ipv4_1.mascara}')
    print(f'Rede: {calc_ipv4_1.rede}')
    print(f'Broadcast: {calc_ipv4_1.broadcast}')
    print(f'Prefixo: {calc_ipv4_1.cidr}')
    print(f'Número de IPs da rede: {calc_ipv4_1.numero_ips}')


if __name__ == '__main__':
    main()
